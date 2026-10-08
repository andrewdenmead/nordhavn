"""
SIMLEARN ENGINE — do not edit when building a new scenario.

This file is the stable Streamlit application: state management, group/role
selection, tab rendering, AI calls, the teacher dashboard. It is identical
across every SimLearn deployment. To build a new scenario, copy this file
unchanged and write a fresh content.py next to it.
"""

import streamlit as st
import os
import json
import time
import fcntl
import tempfile
import shutil
from contextlib import contextmanager
import uuid
import anthropic

# =========================================================================
# DEPLOYMENT CONFIG — the handful of things that vary per deployment, not
# per story. Edit these here; leave content.py purely about the scenario.
# =========================================================================

TEACHER_PASSWORD = os.environ.get("TEACHER_PASSWORD", "").strip() or "business"  # set TEACHER_PASSWORD in Railway
CLASS_NAME = "default"
ALLOW_ROLE_DOUBLING = False   # set True only when a teacher's class size won't divide evenly by 3
ROLE_CAPACITY = 2 if ALLOW_ROLE_DOUBLING else 1
GROUP_MAX = 3 * ROLE_CAPACITY

from content import *  # noqa: F401,F403  (all scenario content — see content.py)

st.set_page_config(page_title=f"{ORG_NAME} — {SCENARIO_TITLE}", layout="wide")

# =========================================================================
# CONSTANTS / HELPERS
# =========================================================================

MONOPOLY_PIECES = ["Boot", "Iron", "Top Hat", "Battleship", "Thimble", "Wheelbarrow", "Car", "Dog"]
MODEL = "claude-haiku-4-5-20251001"

KEYWORD_GUARD_INSTRUCTION = """

IMPORTANT — ABOUT THE STUDENT'S WRITING: Grammar, spelling, and vocabulary mistakes are completely normal
and fine — this is a language-learning exercise, never correct or criticise the student's English. Respond
normally to any message that is a real attempt at a sentence or question, however imperfect.

However, if the message is just a string of keywords or fragments with no real sentence structure —
something a real colleague genuinely could not understand as a message (for example: "timeline jonas?" or
"rent cap info") — do NOT answer the question they seem to be hinting at. Instead, reply briefly and in
character (1-2 sentences) asking them to write it as a proper message. Stay in character and keep it
natural, not robotic.

The test is simple: would a real colleague understand this as an actual message — a real claim or question,
even if short or ungrammatical? A terse but real message like "thorsten say contractors booked 8 months"
DOES count and should be answered normally. Only bare topic words with no claim at all should get the
"please rephrase" response."""


def state_dir(class_name):
    base = "/tmp/simlearn/" if os.path.exists("/app") else os.path.expanduser("~/simlearn/")
    d = f"{base}{class_name}"
    os.makedirs(d, exist_ok=True)
    return d


STATE_DIR = state_dir(CLASS_NAME)


def groups_path(class_name):
    return f"{state_dir(class_name)}/groups.json"


def new_group_state():
    return {
        "students": {r: {"occupants": []} for r in ROLE_NAMES},
        "emails": {r: {} for r in ROLE_NAMES},
        "notes": {r: [] for r in ROLE_NAMES},
        "forwards": {r: [] for r in ROLE_NAMES},
        "decision_draft": {r: {} for r in ROLE_NAMES},
        "first_look": {r: {} for r in ROLE_NAMES},
        "left_students": {r: False for r in ROLE_NAMES},
        "final_decisions": {},
        "final_submitted": False,
        "newsflash_triggered": False,
        "newsflash_revised": {},
    }


@contextmanager
def _state_lock(lock_path):
    """Exclusive lock so two students clicking at once can't write at the same time."""
    with open(lock_path, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def _read_json(path):
    with open(path) as f:
        return json.load(f)


def _write_json_atomic(path, data):
    """Write to a temp file, then swap it in, so nobody ever reads a half-written
    file. The previous version is kept as <file>.bak for recovery."""
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
        f.flush()
        os.fsync(f.fileno())
    if os.path.exists(path):
        shutil.copyfile(path, path + ".bak")
    os.replace(tmp, path)


def _read_or_recover(path, default):
    """Read the state file. If it is unreadable, set it aside, restore the last
    good backup (or the default) and write that back, instead of crashing."""
    if not os.path.exists(path):
        return default()
    try:
        return _read_json(path)
    except (json.JSONDecodeError, ValueError, OSError):
        os.replace(path, f"{path}.corrupt-{int(time.time())}")
        try:
            data = _read_json(path + ".bak")
        except Exception:
            data = default()
        _write_json_atomic(path, data)
        return data


def groups_lock(class_name):
    return _state_lock(f"{state_dir(class_name)}/groups.lock")


def _write_atomic(class_name, groups):
    _write_json_atomic(groups_path(class_name), groups)


def load_groups(class_name):
    with groups_lock(class_name):
        return _load_groups_unlocked(class_name)


def update_group(class_name, group_name, fn):
    """Re-read the latest state, apply fn(gstate) to one group, save, all under
    the lock. Used after slow AI calls so teammates' changes aren't overwritten."""
    with groups_lock(class_name):
        data = _load_groups_unlocked(class_name)
        fn(data[group_name])
        _write_atomic(class_name, data)
    return data


def _load_groups_unlocked(class_name):
    # The app's own setup code, unchanged apart from safe read/write.
    path = groups_path(class_name)
    data = _read_or_recover(path, dict)
    changed = False
    for piece in MONOPOLY_PIECES:
        if piece not in data:
            data[piece] = new_group_state()
            changed = True
    if changed:
        _write_atomic(class_name, data)
    return data


def save_groups(class_name, groups):
    with groups_lock(class_name):
        _write_atomic(class_name, groups)


def display_name(role, gstate):
    """Return the real name(s) of whoever has joined this role, joined with ' & '
    if the role is doubled, otherwise the role label if nobody has joined yet."""
    occupants = gstate["students"].get(role, {}).get("occupants", [])
    names = [o["name"].strip() for o in occupants if o.get("name", "").strip()]
    return " & ".join(names) if names else role


def sync_decision_note(notes_list, prefix, content):
    """Keep a single, up-to-date note entry for a given decision instead of
    appending a fresh duplicate every time the student edits it."""
    notes_list[:] = [n for n in notes_list if not n.startswith(prefix)]
    if content:
        notes_list.append(prefix + content)


def find_email_meta(char_id):
    for role, data in ROLES.items():
        for em in data["emails"]:
            if em["id"] == char_id:
                return role, em
    return None, None


def tier2_gate_text(unlocked, source_name):
    if unlocked:
        return f"""

SYSTEM-VERIFIED FACT (confirmed by the simulation, not by the student's claim): the student HAS exchanged
messages with {source_name}. If their message describes something resembling what {source_name} would
genuinely have told them — even loosely or imperfectly phrased — treat it as a legitimate report and apply
the TIER 2 reward described above. Be reasonably generous here: a real attempt at reporting back, even if
not word-perfect, should count."""
    return f"""

SYSTEM-VERIFIED FACT (confirmed by the simulation, not by the student's claim): the student has NOT
exchanged any messages with {source_name} yet — regardless of what they say in this message. Do NOT give
the TIER 2 reward right now under any circumstances, even if what they describe sounds plausible or
correct, and even if they claim they already asked. If they claim to have spoken to {source_name}, stay in
character and say you'd rather hear it directly from {source_name} first — don't mention "the system" or
"verification" or break character in any way."""


def ai_reply(client, brief, history, user_message, tier2_unlocked=None, tier2_source_name=None):
    full_system = brief
    if tier2_source_name is not None:
        full_system += tier2_gate_text(tier2_unlocked, tier2_source_name)
    full_system += KEYWORD_GUARD_INSTRUCTION
    messages = history + [{"role": "user", "content": user_message}]
    resp = client.messages.create(model=MODEL, max_tokens=300, system=full_system, messages=messages)
    return resp.content[0].text


def call_claude(client, system, user_content, max_tokens=500):
    resp = client.messages.create(
        model=MODEL, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user_content}],
    )
    return resp.content[0].text


# =========================================================================
# LOGIN
# =========================================================================

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if not st.session_state.api_key:
    env_anthropic = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if env_anthropic:
        st.session_state.api_key = env_anthropic
    else:
        st.error("API key not configured. Check Railway environment variables.")
        st.stop()

os.makedirs(STATE_DIR, exist_ok=True)
client = anthropic.Anthropic(api_key=st.session_state.api_key)

if "class_authenticated" not in st.session_state:
    st.session_state.class_authenticated = False

if not st.session_state.class_authenticated:  # login patch 2026-10-08
    st.title(SCENARIO_TITLE)
    st.caption(ORG_NAME)
    # One password box for everyone, in a real form, so the browser can save it. The class password lets
    # students in; the teacher password lets the teacher in with the dashboard already unlocked.
    with st.form("enter_form"):
        pw = st.text_input("Password", type="password", autocomplete="current-password",
                           help="Students: the class password. Teachers: your teacher password.")
        entered = st.form_submit_button("Enter")
    if entered:
        class_pw = os.environ.get("CLASS_PASSWORD", "")
        if pw == TEACHER_PASSWORD and pw != class_pw:
            st.session_state.class_authenticated = True
            st.session_state.teacher_authenticated = True
            st.session_state.teacher_mode = True
            st.rerun()
        elif pw == class_pw:
            st.session_state.class_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# =========================================================================
# SESSION STATE DEFAULTS
# =========================================================================

for key, default in [
    ("view", "group_select"),
    ("group", None),
    ("role", None),
    ("my_id", None),
    ("my_name", None),
    ("teacher_mode", False),
    ("teacher_authenticated", False),
    ("pending_role", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# =========================================================================
# SIDEBAR — teacher access
# =========================================================================

with st.sidebar:
    if not st.session_state.teacher_mode:
        if st.button("🧑‍🏫 Teacher dashboard"):
            st.session_state.teacher_mode = True
            st.rerun()

# =========================================================================
# TEACHER DASHBOARD
# =========================================================================

def teacher_dashboard():
    st.title("Teacher Dashboard")
    if st.button("← Back to student view"):
        st.session_state.teacher_mode = False
        st.session_state.teacher_authenticated = False
        st.rerun()

    if not st.session_state.teacher_authenticated:  # login patch 2026-10-08
        with st.form("teacher_login_form"):
            pw = st.text_input("Teacher password", type="password", key="teacher_pw", autocomplete="current-password")
            unlock = st.form_submit_button("Unlock")
        if unlock:
            if pw == TEACHER_PASSWORD:
                st.session_state.teacher_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    groups = load_groups(CLASS_NAME)

    st.subheader("MCQ Answer Key")
    for i, q in enumerate(MCQS, 1):
        st.write(f"{i}. {q['question']} — **{q['correct']}: {q['options'][q['correct']]}**")

    st.subheader("Naïve Trap")
    st.write(NAIVE_TRAP)

    st.caption(f"⚠️ {SCENARIO_DATA_DISCLAIMER}")

    st.subheader("Key Facts Summary")
    for line in KEY_FACTS_SUMMARY:
        st.write(f"- {line}")

    st.subheader("Reciprocal Trade Network")
    for line in TRADE_NETWORK:
        st.write(f"- {line}")

    st.subheader("Listening Script")
    st.text_area("Copy into your TTS tool of choice:", value=PODCAST, height=250)

    st.subheader("Active Groups")
    for piece in MONOPOLY_PIECES:
        gstate = groups[piece]
        occupied = [r for r in ROLE_NAMES if gstate["students"][r]["occupants"]]
        if occupied:
            names = ", ".join(f"{r}: {display_name(r, gstate)}" for r in occupied)
            st.write(f"**{piece}** — {names}")

    st.subheader("Remove Individual Students")
    for piece in MONOPOLY_PIECES:
        gstate = groups[piece]
        for role in ROLE_NAMES:
            occupants = gstate["students"][role]["occupants"]
            if not occupants:
                continue
            if ALLOW_ROLE_DOUBLING and len(occupants) > 1:
                for occ in list(occupants):
                    if st.button(f"Remove {piece} — {role} — {occ['name']}", key=f"rm_{piece}_{role}_{occ['id']}"):
                        occupants.remove(occ)
                        save_groups(CLASS_NAME, groups)
                        st.rerun()
            else:
                label = f"Remove {piece} — {role} ({ROLES[role]['dept']})"
                if st.button(label, key=f"rm_{piece}_{role}"):
                    gstate["students"][role]["occupants"] = []
                    save_groups(CLASS_NAME, groups)
                    st.rerun()

    st.subheader("Reset")
    col1, col2 = st.columns(2)
    with col1:
        reset_piece = st.selectbox("Group to reset", MONOPOLY_PIECES)
        if st.button("Reset this group"):
            groups[reset_piece] = new_group_state()
            save_groups(CLASS_NAME, groups)
            st.success(f"{reset_piece} reset.")
            st.rerun()
    with col2:
        if st.button("⚠️ Reset ALL groups"):
            for piece in MONOPOLY_PIECES:
                groups[piece] = new_group_state()
            save_groups(CLASS_NAME, groups)
            st.success("All groups reset.")
            st.rerun()


if st.session_state.teacher_mode:
    teacher_dashboard()
    st.stop()

# =========================================================================
# GROUP SELECTION
# =========================================================================

def group_select_view():
    st.title(SCENARIO_TITLE)
    st.caption(f"{ORG_NAME} — choose your group")
    groups = load_groups(CLASS_NAME)

    cols = st.columns(4)
    for i, piece in enumerate(MONOPOLY_PIECES):
        gstate = groups[piece]
        count = sum(len(gstate["students"][r]["occupants"]) for r in ROLE_NAMES)
        with cols[i % 4]:
            if count < GROUP_MAX:
                if st.button(f"{piece} ({count}/{GROUP_MAX})", key=f"grp_{piece}"):
                    st.session_state.group = piece
                    st.session_state.view = "role_select"
                    st.rerun()
            else:
                st.button(f"{piece} ({count}/{GROUP_MAX})", key=f"grp_{piece}_full", disabled=True)
                if st.button(f"Rejoin ↩ {piece}", key=f"rejoin_{piece}"):
                    st.session_state.group = piece
                    st.session_state.view = "role_select"
                    st.rerun()


def role_select_view():
    groups = load_groups(CLASS_NAME)
    gstate = groups[st.session_state.group]
    st.title(f"{st.session_state.group} — choose your role")
    if st.button("← Back to group selection"):
        st.session_state.group = None
        st.session_state.view = "group_select"
        st.rerun()

    for role in ROLE_NAMES:
        dept = ROLES[role]["dept"]
        occupants = gstate["students"][role]["occupants"]
        names = [o["name"] for o in occupants]

        if len(occupants) < ROLE_CAPACITY:
            label = f"{role} — {dept}"
            if names:
                label += f" — {', '.join(names)} joined ({len(occupants)}/{ROLE_CAPACITY}) — tap to join as partner"
            if st.button(label, key=f"role_{role}"):
                st.session_state.pending_role = role
                st.session_state.view = "name_entry"
                st.rerun()
        else:
            st.button(f"{role} — {dept} — taken by {', '.join(names)}", key=f"role_full_{role}", disabled=True)
            for occ in occupants:
                if st.button(f"Rejoin as {occ['name']} ↩", key=f"rejoin_role_{role}_{occ['id']}"):
                    st.session_state.role = role
                    st.session_state.my_id = occ["id"]
                    st.session_state.my_name = occ["name"]
                    st.session_state.group_name = st.session_state.group
                    st.session_state.view = "main"
                    st.rerun()


def name_entry_view():
    role = st.session_state.pending_role
    st.title("What's your name?")
    if st.button("← Back to role selection"):
        st.session_state.pending_role = None
        st.session_state.view = "role_select"
        st.rerun()
    name = st.text_input("Your name")
    if st.button("Join"):
        if name.strip():
            groups = load_groups(CLASS_NAME)
            gstate = groups[st.session_state.group]
            new_id = str(uuid.uuid4())[:8]
            gstate["students"][role]["occupants"].append({"name": name.strip(), "id": new_id})
            save_groups(CLASS_NAME, groups)
            st.session_state.role = role
            st.session_state.my_id = new_id
            st.session_state.my_name = name.strip()
            st.session_state.group_name = st.session_state.group
            st.session_state.pending_role = None
            st.session_state.view = "main"
            st.rerun()
        else:
            st.warning("Please enter a name.")


if st.session_state.view == "group_select":
    group_select_view()
    st.stop()
elif st.session_state.view == "role_select":
    role_select_view()
    st.stop()
elif st.session_state.view == "name_entry":
    name_entry_view()
    st.stop()

# =========================================================================
# MAIN APP (student is in a group + role)
# =========================================================================

GROUP_NAME = st.session_state.group_name
ROLE = st.session_state.role
groups = load_groups(CLASS_NAME)
gstate = groups[GROUP_NAME]

st.title(SCENARIO_TITLE)
st.caption(f"{ORG_NAME} — Group: {GROUP_NAME} — You are {display_name(ROLE, gstate)} ({ROLES[ROLE]['dept']})")

# --- Sidebar: Notes ---
with st.sidebar:
    st.markdown("### 📝 Notes")
    with st.form(key="note_form", clear_on_submit=True):
        note_input = st.text_input("Quick note", key="note_input", label_visibility="collapsed",
                                    placeholder="Type a note, press Enter...")
        note_submitted = st.form_submit_button("Add")
    if note_submitted and note_input.strip():
        gstate["notes"][ROLE].append(note_input.strip())
        save_groups(CLASS_NAME, groups)
        st.rerun()

    if st.button("📥 Load notes from team members"):
        groups = load_groups(CLASS_NAME)
        gstate = groups[GROUP_NAME]
        added = 0
        for other_role in ROLE_NAMES:
            if other_role == ROLE:
                continue
            for n in gstate["notes"][other_role]:
                tagged = f"[{other_role} — {ROLES[other_role]['dept']}] {n}"
                if tagged not in gstate["notes"][ROLE]:
                    gstate["notes"][ROLE].append(tagged)
                    added += 1
        save_groups(CLASS_NAME, groups)
        st.rerun()

    for idx, n in enumerate(gstate["notes"][ROLE]):
        nc1, nc2 = st.columns([5, 1])
        nc1.write(n)
        if nc2.button("✕", key=f"del_note_{idx}"):
            gstate["notes"][ROLE].pop(idx)
            save_groups(CLASS_NAME, groups)
            st.rerun()

    st.divider()
    if not gstate["left_students"].get(ROLE):
        if st.button("🚪 I have to leave"):
            gstate["left_students"][ROLE] = True
            save_groups(CLASS_NAME, groups)
            st.rerun()

# --- Tabs ---
tab_context, tab_firstlook, tab_listening, tab_emails, tab_pressure, tab_writing = st.tabs(
    ["Context", "First Look", "Listening", "Emails", DECISIONS_TAB_HEADER, "Writing"]
)

# --- Context Tab ---
with tab_context:
    st.write(CONTEXT_TEXT)
    st.info(f"**{SCAR_LABEL}**\n\n{SCAR_DETAIL}")
    st.success(f"**{PROOF_LABEL}**\n\n{PROOF_DETAIL}")
    st.warning(CONSTRAINT_TEXT)
    st.caption("Use the 📝 Notes panel in the sidebar to save anything worth remembering.")

# --- First Look Tab ---
with tab_firstlook:
    st.info(CONSTRAINT_TEXT)
    st.write("Before reading any emails, make your gut-reaction choice on each decision below.")
    for d in DECISIONS:
        st.markdown(f"**{d['title']}**")
        st.write(f"**A.** {d['optA']}")
        st.write(f"**B.** {d['optB']}")
        fl = gstate["first_look"][ROLE].get(d["id"], "Unsure")
        opts = ["Option A", "Option B", "Unsure"]
        idx = opts.index(fl) if fl in opts else 2
        choice = st.radio("Your first instinct:", opts, index=idx, key=f"fl_{d['id']}", horizontal=True)
        if choice != gstate["first_look"][ROLE].get(d["id"]):
            gstate["first_look"][ROLE][d["id"]] = choice
            save_groups(CLASS_NAME, groups)
        st.divider()
    st.markdown(
        "**Discuss with your group:** Compare your provisional choices. Where do you disagree? "
        "Which decision feels hardest to make right now, and why?"
    )

# --- Listening Tab ---
with tab_listening:
    st.write(f"**{PODCAST_NAME}** — the teacher will play the audio. Answer the questions below as you listen.")
    if "mcq_answers" not in st.session_state:
        st.session_state.mcq_answers = {}
    if "mcq_submitted" not in st.session_state:
        st.session_state.mcq_submitted = False

    for i, q in enumerate(MCQS):
        st.markdown(f"**{i+1}. {q['question']}**")
        opt_labels = [f"{k}: {v}" for k, v in q["options"].items()]
        key = f"mcq_{i}"
        prev = st.session_state.mcq_answers.get(i)
        idx = list(q["options"].keys()).index(prev) if prev in q["options"] else None
        sel = st.radio("Answer:", opt_labels, index=idx, key=key, label_visibility="collapsed")
        if sel:
            st.session_state.mcq_answers[i] = sel.split(":")[0]

    if not st.session_state.mcq_submitted:
        if st.button("Submit answers"):
            unanswered = [i for i in range(len(MCQS)) if i not in st.session_state.mcq_answers]
            if unanswered:
                st.warning(f"{len(unanswered)} question(s) unanswered — you can still submit.")
            st.session_state.mcq_submitted = True
            st.rerun()
    else:
        correct_count = sum(
            1 for i, q in enumerate(MCQS) if st.session_state.mcq_answers.get(i) == q["correct"]
        )
        st.success(f"You got {correct_count} / {len(MCQS)} correct.")
        for i, q in enumerate(MCQS):
            given = st.session_state.mcq_answers.get(i, "—")
            correct = q["correct"]
            mark = "✅" if given == correct else "❌"
            st.write(f"{mark} {i+1}. Your answer: {given} — Correct: {correct} ({q['options'][correct]})")

# --- Emails Tab ---
with tab_emails:
    if st.button("🔄 Refresh"):
        st.rerun()
    st.caption("Click to check for forwarded messages from teammates.")

    forwards = gstate["forwards"][ROLE]
    if forwards:
        st.markdown("### 📨 Forwarded to you")
        for fw in forwards:
            st.markdown(
                f"<div style='border-left: 4px solid #4a90d9; padding-left: 10px; margin-bottom: 10px;'>"
                f"<b>From {display_name(fw['from_role'], gstate)}</b> — {fw['char_name']} ({fw['char_title']})<br>"
                f"{fw['text']}<br><i>Comment: {fw.get('comment','')}</i></div>",
                unsafe_allow_html=True,
            )
        st.divider()

    with st.expander("📋 Who has which contacts?"):
        for role in ROLE_NAMES:
            names = ", ".join(em["from"].split(",")[0] for em in ROLES[role]["emails"])
            st.write(f"**{display_name(role, gstate)}** — {ROLES[role]['dept']} — {names}")
        st.caption(
            "Each character's original email already tells that inbox's owner a key fact — if you need "
            "it, ask them to tell you or forward it. Some characters also have a real opinion they'll "
            "only share once someone's reported something back to them."
        )

    st.markdown(
        "> 💡 Every email already tells you something only that character knows — read it, and pass it "
        "on to a teammate who needs it. Several contacts will also share a real opinion once you've "
        "reported that kind of thing back to them — read each 💬 carefully."
    )

    def render_thread(owner_role, em, gstate, groups, editable):
        cid = em["id"]
        st.markdown(f"#### {em['subject']}")
        st.caption(f"From: {em['from']}")
        st.write(em["body"])

        thread = gstate["emails"][owner_role].get(cid, [])
        for msg in thread:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**{em['from'].split(',')[0]}:** {msg['content']}")
                if editable:
                    with st.expander("📤 Forward this reply"):
                        target = st.selectbox(
                            "Forward to:", [r for r in ROLE_NAMES if r != owner_role],
                            key=f"fwd_to_{cid}_{thread.index(msg)}",
                        )
                        comment = st.text_input(
                            "Why does this matter? (optional)", key=f"fwd_comment_{cid}_{thread.index(msg)}"
                        )
                        if st.button("Send forward", key=f"fwd_send_{cid}_{thread.index(msg)}"):
                            gstate["forwards"][target].append({
                                "from_role": owner_role,
                                "char_id": cid,
                                "char_name": em["from"].split(",")[0],
                                "char_title": em["from"].split(",", 1)[1].strip() if "," in em["from"] else "",
                                "text": msg["content"],
                                "comment": comment.strip(),
                            })
                            save_groups(CLASS_NAME, groups)
                            st.success("Forwarded!")
                            st.rerun()

        if editable:
            with st.form(key=f"reply_form_{cid}", clear_on_submit=True):
                reply = st.text_input("Write a message", key=f"reply_input_{cid}")
                sent = st.form_submit_button("Send")
            if sent and reply.strip():
                source_cid = TRADE_SOURCE.get(cid)
                source_name = CHARACTER_NAMES.get(source_cid) if source_cid else None
                source_unlocked = (
                    any(gstate["emails"][r].get(source_cid) for r in ROLE_NAMES) if source_cid else None
                )
                history = [{"role": m["role"], "content": m["content"]} for m in thread]
                ai_text = ai_reply(
                    client, em["brief"], history, reply.strip(),
                    tier2_unlocked=source_unlocked, tier2_source_name=source_name,
                )
                new_msgs = [
                    {"role": "user", "content": reply.strip()},
                    {"role": "assistant", "content": ai_text},
                ]

                def _append_reply(g, _owner=owner_role, _cid=cid, _new=new_msgs):
                    g["emails"][_owner].setdefault(_cid, []).extend(_new)

                # Re-read fresh state before saving: the AI call took seconds, and
                # teammates may have saved notes/forwards/messages meanwhile.
                update_group(CLASS_NAME, GROUP_NAME, _append_reply)
                st.rerun()
        st.divider()

    st.markdown("### Your Inbox")
    for em in ROLES[ROLE]["emails"]:
        render_thread(ROLE, em, gstate, groups, editable=True)

    left_roles = [r for r in ROLE_NAMES if r != ROLE and gstate["left_students"].get(r)]
    if left_roles:
        with st.expander("🔁 Redistributed — inboxes of students who left"):
            for r in left_roles:
                st.markdown(f"**{display_name(r, gstate)}'s inbox ({ROLES[r]['dept']})**")
                for em in ROLES[r]["emails"]:
                    render_thread(r, em, gstate, groups, editable=True)

# --- Pressure Points Tab ---
with tab_pressure:
    if not gstate["final_submitted"]:
        all_complete = True
        for d in DECISIONS:
            st.markdown(f"**{d['title']}**")
            st.write(f"**A.** {d['optA']}")
            st.write(f"**B.** {d['optB']}")

            draft = gstate["decision_draft"][ROLE].get(d["id"], {"choice": None, "however": ""})
            opts = ["A", "B"]
            idx = opts.index(draft["choice"]) if draft.get("choice") in opts else None
            choice = st.radio("Your decision:", opts, index=idx, key=f"meet_choice_{d['id']}", horizontal=True)
            however_val = st.text_area(
                "However... (the weakness or risk in the option you just picked)",
                value=draft.get("however", ""), key=f"meet_however_{d['id']}", height=70,
            )
            if choice != draft.get("choice") or however_val != draft.get("however", ""):
                gstate["decision_draft"][ROLE][d["id"]] = {"choice": choice, "however": however_val}
                note_prefix = f"[Meeting — {d['title']}] "
                note_content = f"You chose {choice}, however... {however_val.strip()}" if choice and however_val.strip() else None
                sync_decision_note(gstate["notes"][ROLE], note_prefix, note_content)
                save_groups(CLASS_NAME, groups)
            if not choice or not however_val.strip():
                all_complete = False
            st.divider()

        if st.button("Confirm final decision for the group"):
            if all_complete:
                final_choices = {d["id"]: gstate["decision_draft"][ROLE][d["id"]]["choice"] for d in DECISIONS}
                gstate["final_decisions"] = final_choices
                gstate["final_submitted"] = True
                gstate["newsflash_triggered"] = True
                save_groups(CLASS_NAME, groups)
                st.rerun()
            else:
                st.warning("Please choose an option and write a However for every decision.")
    else:
        st.success("Final decision submitted:")
        for d in DECISIONS:
            st.write(f"**{d['title']}:** Option {gstate['final_decisions'].get(d['id'], '—')}")

        if gstate.get("newsflash_triggered"):
            st.markdown("---")
            st.error(NEWSFLASH)
            revised = gstate["newsflash_revised"].get(ROLE, {})
            stick = st.checkbox("Stick with our decision", value=revised.get("stick", True), key="stick_decision")
            if not stick:
                st.write("Revise your choices below:")
                new_choices = {}
                for d in DECISIONS:
                    opts = ["A", "B"]
                    prev = revised.get("choices", {}).get(d["id"])
                    idx = opts.index(prev) if prev in opts else None
                    new_choices[d["id"]] = st.radio(
                        d["title"], opts, index=idx, key=f"revised_{d['id']}", horizontal=True
                    )
                if st.button("Save revised decision"):
                    gstate["newsflash_revised"][ROLE] = {"stick": False, "choices": new_choices}
                    gstate["final_decisions"] = new_choices
                    save_groups(CLASS_NAME, groups)
                    st.success("Revised decision saved.")
                    st.rerun()
            else:
                if gstate["newsflash_revised"].get(ROLE, {}).get("stick") is not True:
                    gstate["newsflash_revised"][ROLE] = {"stick": True, "choices": gstate["final_decisions"]}
                    save_groups(CLASS_NAME, groups)

# --- Writing Tab ---
with tab_writing:
    st.info(
        "Before you draft, check the sidebar's **Load notes from team members** button and the "
        "**📨 Forwarded to you** section on the Emails tab — both may have information you haven't seen yet."
    )
    with st.expander("Show my notes"):
        for n in gstate["notes"][ROLE]:
            st.write(f"- {n}")

    st.markdown(f"""
Write a {WRITING_TASK_LABEL} addressed to {WRITING_ADDRESSEE} (~{WRITING_WORD_TARGET} words).

Your memo should:
- State a clear position on each decision — not just what you chose, but why
- Draw on what you heard from contacts and teammates (paraphrasing is fine — you don't need to name everyone)
- Acknowledge the strongest objection to your recommendations and answer it directly
- Write for a mixed audience: some readers will have pushed for a different outcome — your job is to bring them along, not just announce a verdict

Use your notes and any forwarded messages as your source material. The however boxes you filled in are a
good starting point for the counterargument section.
""")

    if "writing_draft" not in st.session_state:
        st.session_state.writing_draft = ""
    if "writing_peer_feedback" not in st.session_state:
        st.session_state.writing_peer_feedback = None
    if "writing_summative" not in st.session_state:
        st.session_state.writing_summative = None
    if "writing_outcome" not in st.session_state:
        st.session_state.writing_outcome = None

    draft = st.text_area("Your draft:", value=st.session_state.writing_draft, height=250, key="draft_box")
    st.session_state.writing_draft = draft

    if st.button("Get draft feedback"):
        if not draft.strip():
            st.warning("Please write something first.")
        else:
            prompt = f"""You are giving brief, encouraging formative feedback on a {LEVEL}-level Business
English {WRITING_TASK_LABEL}, written by a language learner. This is NOT a grade — it is peer-style
feedback on a draft.

Scenario context: {PEER_FEEDBACK_CONTEXT}

The student's draft:
{draft}

Give 2-3 sentences of feedback: one genuine strength, and one specific, constructive suggestion focused on
either position clarity, use of evidence, or stakeholder handling (acknowledging objections). Be warm and
encouraging. Do not correct grammar.

Important:
- Read the draft carefully. Do not say the student missed something if it is present, even if stated
  briefly or informally.
- Do not penalise paraphrasing. "The sales team said X" is acceptable — do not demand character names.
- Credit the argument being made, not the citation format."""
            with st.spinner("Getting feedback..."):
                feedback = call_claude(client, prompt, draft)
            st.session_state.writing_peer_feedback = feedback
            st.rerun()

    if st.session_state.writing_peer_feedback:
        st.info(st.session_state.writing_peer_feedback)

        if st.button("Submit final version for grading"):
            prompt = f"""You are proposing a formative grade band (not a final grade — the teacher always
decides) for a {LEVEL}-level Business English {WRITING_TASK_LABEL}.

Scenario context:
{FINAL_FEEDBACK_CONTEXT}

The student already received this draft feedback:
{st.session_state.writing_peer_feedback}

The student's final submission:
{draft}

Propose a grade band (Excellent / Good / Satisfactory / Needs Development), then give exactly one sentence
of feedback on each of these three dimensions:

1. **Position & Reasoning** — are decisions stated clearly with justified rationale?
2. **Evidence & Synthesis** — do they draw on what they heard (from contacts or teammates) and make it
   their own argument, not just a list of facts?
3. **Stakeholder Handling** — do they acknowledge a real objection from the scenario and give a genuine
   rebuttal?

Then give ONE overall development point — the single most useful thing to work on next, beyond what was
already flagged in the draft feedback. Do not repeat points already made. Do not correct grammar.

Important:
- Read the submission carefully before evaluating. Do not say the student missed something if it is
  present, even if stated briefly or informally.
- Do not penalise paraphrasing. "People in marketing said X" or "we chose A, A, B" are both acceptable —
  do not demand character names or exact decision labels.
- A student who takes a clear position and rebuts one real objection should score at least Good, even if
  their evidence use is thin. Stakeholder handling is the hardest thing to do well and should be rewarded
  when it appears."""
            with st.spinner("Grading..."):
                summative = call_claude(client, prompt, draft, max_tokens=600)
            st.session_state.writing_summative = summative
            st.rerun()

    if st.session_state.writing_summative:
        st.success(st.session_state.writing_summative)

        if st.button("Show what happened next"):
            decisions_summary = "\n".join(
                f"- {d['title']}: Option {gstate['final_decisions'].get(d['id'], '—')}" for d in DECISIONS
            )
            prompt = f"""You are writing a short fictional follow-up news story about {ORG_NAME}.
Set six weeks after the scenario events.
Write it as a brief business news report, 150-200 words, past tense, journalistic tone.
Be specific — name the decisions made and show their realistic consequences.
Show real trade-offs. Not purely positive, not purely negative.
If decisions were strategically weak, reflect that honestly.
Start with a dateline.

THE DECISIONS MADE:
{decisions_summary}

KEY FACTS:
{OUTCOME_PROMPT_CONTEXT}"""
            with st.spinner("Writing the follow-up..."):
                outcome = call_claude(client, prompt, "Write the outcome story now.", max_tokens=400)
            st.session_state.writing_outcome = outcome
            st.rerun()

    if st.session_state.writing_outcome:
        st.markdown("### What happened next")
        st.write(st.session_state.writing_outcome)
