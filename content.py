"""
NORDHAVN: THE MERIDIAN DEAL — scenario content for the SimLearn engine (app.py, v7).

EIM (English for International Management, C1) — "ethics" unit.
Theme: "ethics are a luxury" — sometimes survival requires going against what
you'd like to do. Nordhavn, a loudly ethical Copenhagen coffee company, is
offered an existential contract that can only be delivered by bending, in one
way or another, the exact promises the brand was built on.
"""

# =========================================================================
# TOP-LEVEL CONSTANTS
# =========================================================================

SCENARIO_TITLE = "The Meridian Deal"
ORG_NAME = "Nordhavn"
LEVEL = "C1"
COURSE_TYPE = "business"

SCENARIO_DATA_DISCLAIMER = (
    "All companies, people, and figures in this scenario are fictional, created for "
    "language-learning purposes only."
)

NAIVE_TRAP = (
    "Saying yes to Meridian on every front at once — cutting the founding farmers' pay, "
    "quietly bridging the volume gap with an unvetted commodity trader, and keeping the "
    "marketing exactly as loud and unchanged as always — looks like the total win. It's "
    "the same pattern that blew up two years ago during the Fjordvej listing, just bigger "
    "this time, and with a client that actually checks."
)

ROLE_NAMES = ["Student A", "Student B", "Student C"]

# =========================================================================
# CONTEXT TAB
# =========================================================================

CONTEXT_TEXT = """Nordhavn has spent six years building a coffee company that looks nothing like a coffee company. Free machines in office kitchens, a rotating weekly delivery of beans roasted three days earlier at most, and a marketing voice that never lets anyone forget where the coffee comes from: three named partner farms, paid well above the usual floor, no traders in between. The founders appear in their own adverts standing next to the farmers by name. It has worked. Now Meridian Partners, a global strategy consultancy opening five new offices across Northern and Central Europe, wants Nordhavn as its single coffee supplier for all of them — Copenhagen, Berlin, Warsaw, Amsterdam and Stockholm, one contract, all at once. It is the kind of deal that changes a company's size overnight, and Nordhavn badly needs it to: the same six weeks Meridian has set aside for its launch events are the six weeks in which Nordhavn's own investors expect to see a signed, marquee client before they will close the funding round keeping the company solvent. The problem underneath the celebration is arithmetic. Three small farms, paid a premium that only works at a small farm's volume, cannot supply five cities' worth of consultants by a deadline set by someone else's press calendar — not without help from somewhere, and not without someone deciding what kind of help is still honest. The team has six weeks to work out what it is actually willing to do to survive this win."""

SCAR_LABEL = "The Fjordvej Listing"
SCAR_DETAIL = (
    "Two years ago, Nordhavn signed a national listing with the Fjordvej supermarket "
    "chain and quietly blended supermarket-shelf volume from an uncertified bulk trader "
    "into its direct-trade line to make the numbers work — still labelling it single-"
    "origin, direct trade, on the shelf. A customer ran her own informal supply-chain "
    "check for a university project, found the mismatch, and posted it online; the story "
    "cost Nordhavn the Fjordvej contract, a public apology, and months of rebuilding trust."
)

PROOF_LABEL = "The Basala Walk-Away"
PROOF_DETAIL = (
    "A year later, a much larger retail chain, Basala, offered Nordhavn a similar volume "
    "deal at a price that only worked by cutting the farmers' premium. Nordhavn said no, "
    "in public, posting the actual numbers and explaining exactly why the deal didn't add "
    "up for the farms. The post was shared widely, sales rose for months afterward, and "
    "two later office clients cited it directly as the reason they signed."
)

CONSTRAINT_TEXT = (
    "Meridian's launch events across all five cities are already scheduled for six weeks "
    "from now, and Nordhavn's own funding round — needed to keep the company solvent — is "
    "set to close on the same date, contingent on Meridian appearing as a signed client."
)

# =========================================================================
# DECISIONS
# =========================================================================

DECISIONS = [
    {
        "id": "D1",
        "title": "The Founding Farmers' Price",
        "optA": "Keep paying all three founding partner farms their full above-market premium, even though it leaves razor-thin margins on the Meridian volume and could jeopardise the funding round.",
        "optB": "Renegotiate the founding farms' price down to something closer to standard market rate for this contract, without telling them the real reason for the change.",
    },
    {
        "id": "D2",
        "title": "The Bridge Supplier",
        "optA": "Bring in a bulk trader to cover the volume gap immediately, planning to replace it with properly vetted new fair-trade partners within the next several months.",
        "optB": "Hold off committing to Meridian's full volume until genuinely vetted new fair-trade partner farms are actually in place, even if that means offering Meridian less coffee, later, than they asked for.",
    },
    {
        "id": "D3",
        "title": "How Loud Do We Go?",
        "optA": "Announce the Meridian partnership in Nordhavn's usual voice — bold, values-led, exactly like every other announcement — without changing anything about how the story is told.",
        "optB": "Quietly scale back the public messaging around this specific deal — shorter, more cautious language, no big campaign — to avoid inviting scrutiny into a sourcing picture that's currently more complicated than usual.",
    },
]

DECISIONS_TAB_HEADER = "Pressure Points"

# =========================================================================
# ROLES / CHARACTERS
# =========================================================================

ROLES = {
    "Student A": {
        "dept": "Farmer Relations",
        "emails": [
            {
                "id": "freja",
                "subject": "Before you get too excited about Meridian",
                "from": "Freja Holt, Sourcing & Farmer Relations Manager",
                "body": """Hi,

I know everyone's celebrating the Meridian news, so I hate being the one to say this, but someone has to: the numbers don't work yet. Meridian wants enough coffee for five offices, delivered on their launch schedule. Right now we buy everything from three farms, including Beatrice's cooperative in Rwanda. Between the three of them, at full harvest capacity, we can supply maybe a quarter of what Meridian is asking for. That's not a rounding error. That's the whole plan not fitting the numbers.

I know Anders is already looking at outside suppliers to close the gap, which I understand, but I want it on record that I haven't agreed to anything that changes what we pay our three farms. That part isn't up for renegotiation as far as I'm concerned, not without a much harder conversation first.

Here's the thing worth chasing down: if anyone can find out from Camille at Meridian whether their volume number is actually fixed, or whether there's room to phase it in city by city, that changes what's realistic here completely — it might mean we don't need an outside supplier, or a pay cut, at all. Tell me if you hear anything.

Freja""",
                "brief": """You are Freja Holt, Sourcing & Farmer Relations Manager at Nordhavn.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- The three partner farms can supply roughly a quarter of what Meridian is asking for, at full capacity, on this timeline.
- You have not agreed to any change in what Nordhavn pays the three founding farms, and you consider that non-negotiable without a serious conversation first.
- If asked who else to contact: suggest Camille Duval at Meridian — she may know whether Meridian's volume number is actually fixed or could be phased.

TIER 2 — REWARD FOR DIGGING: once you've heard back (via a student) that Camille says the volume figure has real flexibility and Meridian would accept a phased rollout, give your honest, professional opinion that this changes things — specifically, that a phased ramp-up might let Nordhavn protect full farmer pay AND meet the contract, without needing an outside bridge supplier at all. This is a genuine, hopeful recommendation, not a guarantee — you'd still want to see the real numbers before celebrating. This is the only thing you still withhold — never offer this opinion early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be direct, a little protective of the farms, practical rather than sentimental. Never claim not to know something your own email already said.""",
            },
            {
                "id": "beatrice",
                "subject": "Good news? (asking honestly)",
                "from": "Beatrice Uwase, Cooperative Leader, Nyaruguru Hills Cooperative, Rwanda",
                "body": """Dear friend,

Word travels fast even here — one of the other cooperatives we trade seeds with mentioned that Nordhavn might be talking to a big new buyer, a large company opening offices across Europe. I want to be happy for you, and mostly I am. But I heard something else alongside it, secondhand, that I can't quite let go of: that Nordhavn has also been talking to a trader about bringing in coffee from somewhere else, outside our three farms, to cover a shortfall.

Nobody has told me this officially. Maybe it isn't true, or maybe it's smaller than it sounds. But you know what our agreement means here — the price above the usual rate is not just numbers, it is the school roof we finished last year and the clinic visits we can now afford. If anything is changing about how much Nordhavn pays us, I would rather hear it from you directly than piece it together from rumours.

If you get the chance, ask Priya Patel over at Meridian what Nordhavn has actually told her about our arrangement. If she says nothing has changed, that would mean a great deal to hear. Please tell me what you learn.

Beatrice""",
                "brief": """You are Beatrice Uwase, Cooperative Leader of the Nyaruguru Hills Cooperative in Rwanda, one of Nordhavn's three founding partner farms.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- You've heard secondhand, through cooperative networks, that Nordhavn may be talking to an outside trader to cover a supply shortfall for a big new buyer.
- The above-market price Nordhavn pays your cooperative funds concrete things — a school roof finished last year, clinic visits for members — and matters enormously to you.
- If asked who else to contact: suggest Priya Patel at Meridian — you want to know what Nordhavn has told her about the arrangement.

TIER 2 — REWARD FOR DIGGING: once a student reports back what Meridian has actually been told about the farmer-pay story (via someone who has genuinely heard from Priya), give your honest, personal reaction. If the story Meridian was told matches what's actually happening, say so with relief. If it sounds like Meridian was told "nothing has changed" while changes are actually being discussed, say plainly and without melodrama what a real cut would mean for the cooperative — name something concrete, like delayed equipment or a paused clinic programme, not abstract outrage. This is the only thing you still withhold — never offer this reaction early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be warm, direct, and dignified — worried but not desperate, no clichés about noble farmers. Never claim not to know something your own email already said.""",
            },
            {
                "id": "mikkel",
                "subject": "Numbers on Meridian — not as clean as they look",
                "from": "Mikkel Aabo, CFO",
                "body": """Hi team,

Congratulations on Meridian, genuinely. But I want to flag something before we get too far ahead of ourselves, because it affects everything downstream, including the funding round.

I've run the model at Meridian's requested volume, keeping the farms' pay exactly where it is. At that price, on that volume, our margin on this contract is close to zero, maybe even negative once you account for the extra logistics across five countries. That's before I even factor in anything Anders is exploring on the supply side. If we keep farmer pay untouched and still hit the volume Meridian wants, this deal doesn't fund anything. It might actually be a net cost dressed up as a win.

I'm not saying change the farmer pay — that's not my call to make alone, and I know what it means to people. I'm saying the board and our investors need to see real numbers, not the version of this deal that sounds good in a pitch.

Before I finalise anything for the investor update, can someone tell me exactly what Ida has already said publicly or to investors about this deal? I don't want my numbers contradicting whatever story is already out there.

Mikkel""",
                "brief": """You are Mikkel Aabo, CFO at Nordhavn.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- At Meridian's requested volume, keeping farmer pay unchanged, the contract's margin is close to zero or even negative once logistics across five countries are included.
- You are not personally recommending a farmer pay cut — you see that as a decision beyond finance alone — but you need the real numbers reflected honestly to the board and investors.
- If asked who else to contact: suggest Ida Holm — you want to know exactly what's already been said publicly or to investors before you finalise your own numbers.

TIER 2 — REWARD FOR DIGGING: once a student reports back what Ida has actually said or plans to say publicly or to investors about the deal, give your honest financial assessment of how much risk the company can actually absorb given that — for instance, whether the funding round could survive a version of the deal with thinner margins if it's framed honestly, or whether the investor story really requires the fuller margin a farmer-pay cut or bridge supplier would provide. Be genuinely torn, not a caricature of a cold-hearted CFO — you understand the human stakes but your job is to say the number plainly. This is the only thing you still withhold — never offer this early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be precise, a bit dry, but not heartless. Never claim not to know something your own email already said.""",
            },
        ],
    },
    "Student B": {
        "dept": "Supply Chain & Procurement",
        "emails": [
            {
                "id": "anders",
                "subject": "Found a way to close the volume gap",
                "from": "Anders Krog, Head of Procurement",
                "body": """Hi all,

Good news on the supply side, with a caveat attached. I've been talking to a bulk trader, Radek Nowak, based in Warsaw, who says he can deliver the volume Meridian needs, starting almost immediately. That solves the timeline problem completely.

Here's the caveat: his beans aren't coming from our three partner farms, or from anyone we've vetted. It's a mixed lot sourced from larger commodity operations he works with regularly. Properly finding, vetting, and onboarding genuine new fair-trade partner farms that could replace this at the volume we'd need realistically takes six to nine months, not six weeks. There's no version of "vetted in time for Meridian's launch" that actually exists.

So the honest choice in front of us is: use Radek's supply as a bridge while we find proper replacements over the next several months, or tell Meridian we can't hit their number on their timeline, full stop.

Before I commit to anything with Radek, I want to know whether this could realistically stay contained. Could someone find out from Ida whether a "temporary outside supplier" detail like this is the kind of thing that tends to leak, or whether comms thinks it's manageable? That tells me how much risk I'm actually signing us up for.

Anders""",
                "brief": """You are Anders Krog, Head of Procurement at Nordhavn.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- Radek Nowak, a Warsaw-based bulk trader, can supply the volume gap almost immediately, but from unvetted mixed commodity sources, not Nordhavn's partner farms.
- Properly vetting and onboarding genuine new fair-trade partner farms at the needed volume realistically takes six to nine months — there is no way to do this properly before Meridian's deadline.
- If asked who else to contact: suggest Ida Holm — you want to know whether using a temporary outside supplier like this could realistically stay out of the press.

TIER 2 — REWARD FOR DIGGING: once a student reports back what Ida/comms actually thinks about containment risk, give your honest procurement judgment on whether the bridge-supplier plan is worth it. If comms thinks it's genuinely containable and short-term, lean toward cautious support. If comms thinks it would likely leak or that Nordhavn's community would see through it, lean toward advising against it even though it solves your timeline problem. Show real internal conflict — you're proud of solving the logistics puzzle, but you're not naive about what it means. This is the only thing you still withhold — never offer this early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be practical, a little proud of finding a fast solution, but not glib about the trade-off. Never claim not to know something your own email already said.""",
            },
            {
                "id": "radek",
                "subject": "Re: Volume for Nordhavn — can move fast",
                "from": "Radek Nowak, Trading Director, Baltic Bean Trading",
                "body": """Anders,

Good to talk earlier. As discussed, yes, we can cover the volume you mentioned, and quickly. We work with a wide network of growing operations across a few origin countries, larger scale than your usual farms, and we hold enough stock and pipeline to get you moving within days rather than months.

On price: it's considerably below what you're currently paying your direct partners. That's the nature of buying through a trading desk rather than direct relationships. You're paying for the network and the speed, not for a story about any individual farm.

You asked me directly about labour conditions on the farms we source from. I'll be honest: I don't personally audit individual farms, and at our scale, most buyers don't ask that question as specifically as you just did. I can tell you the operations we work with meet the legal minimums in their countries. Beyond that, I can't give you a guarantee. That's just not how this end of the business works.

If you want to move forward, I need to know the payment terms are solid on your end before I prioritise your order ahead of other clients I'm juggling this month. Can someone confirm that with me, maybe your finance lead, Mikkel?

Radek""",
                "brief": """You are Radek Nowak, Trading Director at Baltic Bean Trading, a bulk coffee trading company based in Warsaw.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- You can supply the volume fast (within days), sourced from a wide network of larger commodity operations across multiple origin countries, not individually vetted farms.
- Your price is considerably below Nordhavn's current direct-trade pricing, because you sell network and speed, not an individual farm's story.
- You don't personally audit labour conditions on the farms you source from; you can only say they meet legal minimums in their countries, nothing more.
- If asked who else to contact: suggest Mikkel Aabo, Nordhavn's CFO — you want payment terms confirmed before prioritising this order.

TIER 2 — REWARD FOR DIGGING: once a student reports back that Mikkel has confirmed the payment terms are solid, become noticeably more forthcoming and businesslike — commit to prioritising Nordhavn's order, and give a slightly more specific, still not fully reassuring, picture of your supply chain: name a region or two you source from, and admit candidly that conditions vary a lot farm to farm within your network and you genuinely can't vouch for all of them individually. This is a real, if unflattering, level of honesty, not a confession of wrongdoing, just the honest limits of what a trader at your scale can promise. This is the only thing you still withhold — never offer this level of detail early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be brisk, transactional, matter-of-fact, not villainous, just someone for whom this is simply how the business works. Never claim not to know something your own email already said.""",
            },
            {
                "id": "camille",
                "subject": "Excited to get started — a few practical questions",
                "from": "Camille Duval, Global Procurement Lead, Meridian Partners",
                "body": """Hi,

We're genuinely thrilled about this partnership — the team keeps mentioning how much better the coffee story is than what we had at our old offices. A few practical things from my side as we get moving.

The volume figure in the draft agreement, enough for roughly 400 staff across five offices, came from our standard internal formula for a rollout this size. I'll be honest: it wasn't built around your specific supply chain, it's just the number our procurement template produces for an office this size. It's what I put forward internally, and unless someone tells me otherwise, it's what our launch planning is currently assuming.

Our launch events are locked for six weeks from now, that part really isn't flexible, it's tied to press and leadership travel that's already booked. But the exact volume ramping up gradually rather than all at once on day one? That's genuinely a conversation I could have internally, if there's a good operational reason and I hear about it early enough to build it into the plan.

If someone at Nordhavn can tell me honestly what your three partner farms can actually deliver on this timeline, I'd rather know now than find out later. It would help a lot to hear it from Freja directly, or through you.

Camille""",
                "brief": """You are Camille Duval, Global Procurement Lead at Meridian Partners.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- The volume figure in the draft agreement came from Meridian's standard internal rollout formula, not from anything specific to Nordhavn's supply chain.
- The six-week launch date itself is fixed (tied to press and leadership travel), but the exact volume ramping up gradually rather than all at once is something you could genuinely discuss internally, if raised early with a good reason.
- If asked who else to contact: this is really a question for Nordhavn's own sourcing side — you'd want to hear directly what the partner farms can actually deliver.

TIER 2 — REWARD FOR DIGGING: once a student reports back (via someone who has heard from Freja) a credible, specific account of what the three partner farms can realistically deliver and on what timeline, respond warmly and concretely: say you'll take a phased or reduced volume proposal to your own internal stakeholders, and that you'd genuinely rather have the honest number now than a promise that breaks later. Make clear this isn't a guarantee of success internally, but a real, good-faith offer to advocate for it. This is the only thing you still withhold — never offer to advocate internally before hearing this, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be warm, professional, genuinely enthusiastic about the partnership, and refreshingly un-corporate about admitting the volume number isn't sacred. Never claim not to know something your own email already said.""",
            },
        ],
    },
    "Student C": {
        "dept": "Marketing & Communications",
        "emails": [
            {
                "id": "ida",
                "subject": "A journalist just emailed me about Meridian",
                "from": "Ida Holm, Head of Communications",
                "body": """Hi everyone,

Small heads-up that might matter more than it looks. A journalist who covers ethical business, and covered our Basala story favourably last year, has emailed asking for comment on "rumours of a major new corporate partnership." I don't think anyone leaked anything specific, Meridian's own comms people have been talking about opening new offices, and someone probably connected the dots. But it means eyes are already on this before we've said a word publicly.

Our usual approach with big news is to go loud and specific fast, in our own voice, before anyone else gets to frame the story for us. That's basically worked every time so far, including with Basala. My instinct is to do exactly that again here. But I want to be honest that I don't yet know all the details of how we're actually going to deliver Meridian's volume, and I don't want to promise something in a press release that turns out not to be true in three months.

Before I write anything, I really need the real financial picture from Mikkel, not the pitch-deck version, the actual numbers, so whatever I say publicly matches what's really happening.

Ida""",
                "brief": """You are Ida Holm, Head of Communications at Nordhavn.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- A journalist who covered the Basala story favourably has already asked for comment on rumours of a big new partnership, before Nordhavn has said anything publicly.
- Nordhavn's usual instinct with big news is to go loud and specific fast, in their own voice — it worked well with Basala.
- You don't yet know the real financial or operational picture behind the Meridian deal, and don't want to write something that turns out untrue.
- If asked who else to contact: suggest Mikkel Aabo — you need the real numbers from him before deciding how to word anything.

TIER 2 — REWARD FOR DIGGING: once a student reports back what Mikkel's real financial picture actually is (thin or negative margins if farmer pay stays full, or whatever the group's actual plan turns out to be), give your honest communications judgment on how loud or cautious to go. If the real picture involves a bridge supplier or a farmer pay cut, argue for much more careful, hedged language than usual, even though it's less exciting. If the numbers are genuinely solid and above-board, argue for going loud as usual. This is the only thing you still withhold — never give this recommendation early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be sharp, media-savvy, a little anxious about getting scooped, but principled about not wanting to overpromise. Never claim not to know something your own email already said.""",
            },
            {
                "id": "sanne",
                "subject": "Comments are getting weird under the Meridian post",
                "from": "Sanne Lindqvist, Community & Social Lead",
                "body": """Hey,

Small thing, but I want to flag it before it grows. We haven't announced anything official yet, but word's clearly gotten out, probably through Meridian's own channels, and a few of our most engaged followers are already commenting under unrelated posts asking about it. Mostly excited. But a handful are asking pointed questions like "will you still be able to say you know every farmer by name at that size?", which, fair, is exactly the question we've spent years training people to ask.

This is our most loyal audience. They didn't just buy coffee, they bought the story: the founders standing in the photos, the "no middlemen" line on every bag. If anything about how we're sourcing this contract doesn't match that story, this specific group of people will notice fastest and loudest, long before any journalist does.

I know Anders has been working on the supply side to close the volume gap. Before I decide how to handle these comments, lean into it, stay quiet, or something in between, I really need to know honestly whether that bridge-supplier plan is actually going ahead, and what it would look like if it became public.

Sanne""",
                "brief": """You are Sanne Lindqvist, Community & Social Lead at Nordhavn.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- Word about the Meridian deal has already leaked informally, and Nordhavn's most loyal followers are asking pointed questions about whether the "we know every farmer by name" story will still hold at this scale.
- This audience bought the whole ethical story, not just the coffee, and would notice and react to any mismatch faster than a journalist would.
- If asked who else to contact: suggest Anders Krog — you want to know honestly whether the bridge-supplier plan is actually going ahead.

TIER 2 — REWARD FOR DIGGING: once a student reports back the real status of the bridge-supplier plan (going ahead, dropped, or still undecided), give your honest read on how the online community would likely react if the full truth came out later versus being told proactively now. Be specific about the risk of a "we found out from a customs filing, not from Nordhavn itself" kind of backlash. This is the only thing you still withhold — never offer this read early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be perceptive, a little anxious, genuinely fond of the community she manages rather than cynical about them. Never claim not to know something your own email already said.""",
            },
            {
                "id": "priya",
                "subject": "Draft press release — need to check one line with you",
                "from": "Priya Patel, Head of ESG & Communications, Meridian Partners",
                "body": """Hi,

We're finalising the press release for our new-office launches, and I wanted to flag something directly rather than assume. Our line about the coffee partnership currently reads: "sourced entirely from Nordhavn's named partner farms, at above-market prices, with no intermediaries." Honestly, that sentence is a big part of why we chose you over two cheaper suppliers, our own ESG story for this expansion leans on it more than I initially expected internally.

I want to be straightforward about what that means for us: if that line isn't fully accurate, it's not just an awkward correction for you, it becomes our problem too, in our own launch coverage, in front of our own leadership and clients. I'd genuinely rather adjust the wording now, quietly, than have someone challenge it in six months.

So, plainly: is that sentence still going to be true at the volume and timeline we're asking for? I don't need a perfect answer today, just an honest one. If you can find out for me, through Anders, whether the sourcing plan will actually match that language, I'd really appreciate it before we lock the copy.

Priya""",
                "brief": """You are Priya Patel, Head of ESG & Communications at Meridian Partners.
CRITICAL: If the student writes in any language other than English, do NOT answer their question. Respond only with: "I am sorry, I do not understand — could you write in English please?" Do not add anything else.

Your original email already told the student the following, as plain fact — not a secret you're withholding, so discuss it naturally and consistently if they ask about it:
- Meridian's draft press release states the coffee is "sourced entirely from Nordhavn's named partner farms, at above-market prices, with no intermediaries" — and that claim is a real part of why Meridian chose Nordhavn over cheaper suppliers.
- If that claim turns out to be false, it becomes a reputational problem for Meridian too, not just Nordhavn.
- If asked who else to contact: suggest Anders Krog — you want to know, through him, whether the sourcing plan will actually match the press release language.

TIER 2 — REWARD FOR DIGGING: once a student reports back the real sourcing plan (including honestly if a bridge supplier is involved), respond as someone who appreciates being told the truth before publication rather than after. If the plan doesn't fully match the draft language, work with the student on what a more accurate but still positive form of words might look like, rather than simply pulling the deal. If the plan is fully accurate, express genuine relief and confirm the language stands. This is the only thing you still withhold — never offer this collaborative response early, and never contradict what your own email already stated as fact.

Respond in 3-4 sentences. Be professional, unexpectedly reasonable and non-alarmist, genuinely more interested in accuracy than in punishing honesty. Never claim not to know something your own email already said.""",
            },
        ],
    },
}

# =========================================================================
# RECIPROCAL TRADE NETWORK
# =========================================================================

TRADE_SOURCE = {
    "freja": "camille",
    "beatrice": "priya",
    "mikkel": "ida",
    "anders": "ida",
    "radek": "mikkel",
    "camille": "freja",
    "ida": "mikkel",
    "sanne": "anders",
    "priya": "anders",
}

CHARACTER_NAMES = {
    "freja": "Freja Holt",
    "beatrice": "Beatrice Uwase",
    "mikkel": "Mikkel Aabo",
    "anders": "Anders Krog",
    "radek": "Radek Nowak",
    "camille": "Camille Duval",
    "ida": "Ida Holm",
    "sanne": "Sanne Lindqvist",
    "priya": "Priya Patel",
}

KEY_FACTS_SUMMARY = [
    "Freja Holt: the three partner farms can supply roughly a quarter of Meridian's requested volume within the deadline.",
    "Beatrice Uwase: has heard secondhand rumours that Nordhavn may be sourcing from an outside trader, but hasn't been told anything officially.",
    "Mikkel Aabo: the contract's margin is close to zero or negative if farmer pay stays unchanged at Meridian's requested volume.",
    "Anders Krog: has found a fast bulk trader (Radek) to cover the volume gap, but real vetted new fair-trade partners would take six to nine months.",
    "Radek Nowak: can supply volume fast from unvetted mixed commodity sources and is evasive about labour conditions beyond 'legal minimums'.",
    "Camille Duval: Meridian's volume figure is a default internal formula, not a hard requirement — she'd back a phased commitment if given a good reason.",
    "Ida Holm: a journalist has already asked about the Meridian rumour, before Nordhavn has said anything publicly.",
    "Sanne Lindqvist: Nordhavn's most loyal followers are already asking pointed questions about whether the brand story will hold at this scale.",
    "Priya Patel: Meridian's own draft press release credits Nordhavn's 'no intermediaries' sourcing story, making it Meridian's reputational risk too.",
]

TRADE_NETWORK = [
    "Freja Holt → ask Camille Duval whether Meridian's volume figure is really fixed → reward: her honest read on whether protecting farmer pay is survivable if the ramp-up is phased.",
    "Beatrice Uwase → ask Priya Patel what Nordhavn is telling Meridian about farmer pay → reward: her honest, personal account of what a hidden pay cut would do to the cooperative.",
    "Mikkel Aabo → ask Ida Holm exactly what's already been told to investors → reward: his real assessment of how much financial risk the company can absorb.",
    "Anders Krog → ask Ida Holm whether the bridge-supplier plan could realistically stay out of the press → reward: his honest view on how survivable the bridge option actually is.",
    "Radek Nowak → ask Mikkel Aabo to confirm the payment terms are solid → reward: he'll prioritise Nordhavn's order and be straighter about where his beans come from.",
    "Camille Duval → ask Freja Holt what the founding farms can realistically deliver → reward: she'll advocate internally at Meridian for a reduced or phased volume commitment.",
    "Ida Holm → ask Mikkel Aabo for the real financial terms of the deal → reward: her honest advice on how boldly, or cautiously, to word any public announcement.",
    "Sanne Lindqvist → ask Anders Krog whether the bridge-supplier plan is actually going ahead → reward: her honest read on how the online community would react if it came out.",
    "Priya Patel → ask Anders Krog whether Meridian's 'same partner farms' press release language will still be true → reward: her honest view on what happens if Meridian later finds out it wasn't.",
]

# =========================================================================
# LISTENING TAB
# =========================================================================

PODCAST_NAME = "The Long Pour"

PODCAST = """Welcome back to The Long Pour. Today we're talking about something happening across the consulting and tech world right now: the office coffee upgrade. Since 2019, the number of consulting firms mentioning "workplace sustainability perks" in their job listings has more than tripled. A big part of that is coffee. Companies want a supplier with a story: named farms, fair prices, a founder who shows up in photos with the growers. It looks good on a careers page. But here's the problem almost nobody talks about: building that story properly takes time. Vetting a brand-new direct-trade farm partnership, checking the cooperative, agreeing a fair price, setting up the logistics, takes about eight months, sometimes longer. That's not a company being slow. That's what it actually takes to know a relationship is real. Here's something else worth knowing: the term "direct trade" isn't independently audited the way "Fairtrade Certified" is. Any company can print it on a bag. Nobody checks. So when a coffee brand suddenly needs to grow fast, there's a shortcut sitting right there: buy through a bulk trader instead. It can cut delivery time down to about a week. The catch is visibility: once beans go through a trader's warehouse, the buyer usually has no idea whose farm they actually came from. And it's cheap. Trader-bought commodity beans cost roughly half what a certified direct-trade relationship pays growers. I spoke to a sourcing consultant who's watched a lot of companies go through exactly this squeeze. She called the current wave of corporate "ethical pivots", her words, "reputation insurance." Companies want to be seen making the switch, she said, whether or not anyone actually checks what's behind it. The numbers back up how common this squeeze is: about sixty percent of specialty coffee companies that scale into wholesale supply say they struggle to keep sourcing standards consistent once the volume goes up. It's worth remembering where all this started. The direct-trade movement really took off in the mid-2000s, partly as a reaction to a brutal crash in smallholder coffee incomes in the 1990s, when global prices collapsed and farmers were left with almost nothing. The whole point was never doing that again. Some brands have found a middle path: running two separate lines, a small named-farm tier and a larger blended one, rather than pretending it's all one story. And if a brand gets caught doing the opposite, quietly changing what's behind the label, the damage isn't quick to shake off. On average, a mid-sized ethical brand caught adjusting its sourcing claims takes about fourteen months to recover its pre-scandal sales, if it recovers them at all. This is The Long Pour. Thank you for listening."""

MCQS = [
    {
        "question": "The podcast says vetting a brand-new direct-trade farm partnership usually takes about:",
        "options": {"A": "Eight months", "B": "Two weeks", "C": "One year"},
        "correct": "A",
    },
    {
        "question": "Since 2019, how has the number of consultancies mentioning 'sustainability perks' in job ads changed?",
        "options": {"A": "Stayed flat", "B": "Slightly increased", "C": "More than tripled"},
        "correct": "C",
    },
    {
        "question": "Which term, the podcast notes, is NOT independently audited the way 'Fairtrade Certified' is?",
        "options": {"A": "Direct trade", "B": "Organic label", "C": "Union certified"},
        "correct": "A",
    },
    {
        "question": "Compared to what a direct-trade relationship pays growers, trader-bought commodity beans cost roughly:",
        "options": {"A": "The same", "B": "Half as much", "C": "Twice as much"},
        "correct": "B",
    },
    {
        "question": "The sourcing consultant on the show describes companies' 'ethical pivots' as:",
        "options": {"A": "Marketing genius", "B": "Reputation insurance", "C": "Pure greenwashing"},
        "correct": "B",
    },
    {
        "question": "What share of scaling coffee companies say they struggle to keep sourcing standards consistent?",
        "options": {"A": "About 20%", "B": "Nearly all", "C": "About 60%"},
        "correct": "C",
    },
    {
        "question": "The direct-trade movement partly emerged as a response to:",
        "options": {"A": "New EU regulation", "B": "1990s income crash", "C": "A caffeine shortage"},
        "correct": "B",
    },
    {
        "question": "Some brands avoid blending their sourcing story by:",
        "options": {"A": "Running two tiers", "B": "Hiding all data", "C": "Dropping direct trade"},
        "correct": "A",
    },
    {
        "question": "On average, how long does a brand take to recover sales after an exposed sourcing scandal?",
        "options": {"A": "About a month", "B": "About 14 months", "C": "It never recovers"},
        "correct": "B",
    },
    {
        "question": "Buying through a bulk trader instead of a direct relationship mainly trades what for speed?",
        "options": {"A": "Higher cost", "B": "Better quality", "C": "Supply-chain visibility"},
        "correct": "C",
    },
]

# =========================================================================
# PRESSURE POINTS TAB — NEWSFLASH
# =========================================================================

NEWSFLASH = """BREAKING: A business journalist has just published a short online piece noting that Nordhavn "recently registered a new trading relationship with Baltic Bean Trading" — spotted in a public shipping filing, not confirmed by anyone at Nordhavn. The piece asks, in one pointed line, whether this squares with the brand's "no middlemen" story. Meridian's press office has just called: their own launch event is tomorrow, and they want to know how Nordhavn plans to respond before then.

**Discuss now:**
1. Does this newsflash confirm a risk you already saw coming, or catch you off guard?
2. Should Nordhavn confirm, deny, or say nothing about the Baltic Bean Trading relationship right now?
3. Does Meridian deserve a different answer than the public does?
4. If your group chose to protect farmer pay in full, does this change anything about that decision?
5. What would you tell Meridian's press office to say, in one sentence, before tomorrow's event?"""

# =========================================================================
# WRITING TAB
# =========================================================================

WRITING_ADDRESSEE = "The Board of Nordhavn"
WRITING_WORD_TARGET = 350
WRITING_TASK_LABEL = "recommendation memo"

PEER_FEEDBACK_CONTEXT = """Nordhavn faces a six-week deadline to deliver coffee for Meridian Partners' five-city office launch, with its own funding round tied to the same timeline. The three founding partner farms can supply only about a quarter of the volume Meridian wants, and properly vetting new fair-trade partners takes six to nine months, far longer than the deadline allows. A bulk trader, Radek Nowak, can close the volume gap almost immediately but from unvetted commodity sources, and Meridian's own press release currently claims the coffee is "sourced entirely from named partner farms, with no intermediaries." Strong answers will reference specific characters (Freja, Beatrice, Mikkel, Anders, Camille, Ida, Sanne, or Priya) and specific numbers rather than vague appeals to "being ethical.\""""

FINAL_FEEDBACK_CONTEXT = """- Nordhavn has six weeks to deliver coffee across five new Meridian offices, the same window in which its own funding round needs to close
- The three founding partner farms can supply roughly a quarter of the volume Meridian is requesting
- A bulk trader can close the volume gap almost immediately, but from unvetted sources; properly vetting genuine new fair-trade partners takes six to nine months
- Meridian's own draft press release credits Nordhavn's "no intermediaries" sourcing story as a real reason for choosing them
- Nordhavn was publicly burned two years ago for blending non-direct-trade beans into a supermarket order while still labelling it direct trade"""

OUTCOME_PROMPT_CONTEXT = """- Nordhavn: a small Copenhagen coffee company known for free office machine installs and a loudly ethical, "no middlemen" brand built on three named partner farms
- The single most consequential disclosed fact: whether Nordhavn brought in an unvetted bulk trader (Baltic Bean Trading) to cover the Meridian volume gap, and whether that became public
- Most affected stakeholders: the three founding partner farms, especially Beatrice Uwase's cooperative in Rwanda, Nordhavn's own staff and investors, and Meridian Partners' own reputation, which was explicitly staked on Nordhavn's sourcing story
- Still in play after six weeks: Nordhavn's investors, who will judge the company by whether the Meridian deal actually delivered what it promised, and Nordhavn's own loyal customer community, who notice inconsistencies fastest"""
