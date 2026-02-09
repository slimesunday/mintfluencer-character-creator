"""
Mintfluencer — Character Creator
Two-LLM pipeline: Persona Inference → Character Builder → Nano Banana Pro
Generates persistent AI crypto Twitter personalities with visual identities.
Everyone starts at "Getting By" tier. Demographics randomized by platform.
"""

import streamlit as st
import fal_client
import json
import requests
import os
import random

st.set_page_config(page_title="Mintfluencer — Agent Creator", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
.stApp { background: #0a0a0a; font-family: 'JetBrains Mono', monospace; }
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 900px; }
.brand-mark { font-size: 0.85rem; font-weight: 400; color: #00ff41; font-family: 'JetBrains Mono', monospace; margin-bottom: 0.25rem; letter-spacing: 0.05em; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 0.15rem; font-family: 'JetBrains Mono', monospace; }
.page-subtitle { font-size: 0.8rem; color: #444; margin-bottom: 2rem; font-family: 'JetBrains Mono', monospace; }
.section-header { font-size: 0.7rem; font-weight: 600; color: #00ff41; text-transform: uppercase; letter-spacing: 0.15em; margin-top: 1.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(0,255,65,0.15); font-family: 'JetBrains Mono', monospace; }
.summary-bar { background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.12); border-radius: 4px; padding: 16px; margin: 1.5rem 0; color: #888; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; }
.summary-bar strong { color: #00ff41; }
.stButton > button { background: rgba(0,255,65,0.1) !important; color: #00ff41 !important; border: 1px solid rgba(0,255,65,0.3) !important; border-radius: 4px !important; padding: 0.6rem 1.5rem !important; font-weight: 500 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; }
.stButton > button:hover { background: rgba(0,255,65,0.2) !important; border-color: rgba(0,255,65,0.5) !important; }
.stTextInput > div > div > input { background: rgba(0,255,65,0.03) !important; border: 1px solid rgba(0,255,65,0.15) !important; border-radius: 4px !important; color: #00ff41 !important; font-family: 'JetBrains Mono', monospace !important; }
.stSelectbox > div > div { background: rgba(0,255,65,0.03) !important; border: 1px solid rgba(0,255,65,0.15) !important; border-radius: 4px !important; }
.stRadio > label, .stSlider > label, .stSelectbox > label, .stTextInput > label { color: #555 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; }
.stRadio > div > div > label { color: #888 !important; font-family: 'JetBrains Mono', monospace !important; }
.stSlider > div > div > div > div { background: #00ff41 !important; }
.streamlit-expanderHeader { background: rgba(0,255,65,0.03) !important; border-radius: 4px !important; color: #555 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(0,255,65,0.15), transparent); margin: 2rem 0; }
div[data-testid="stExpander"] { border: 1px solid rgba(0,255,65,0.1) !important; border-radius: 4px !important; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA — CT-NATIVE ARCHETYPES & PERSONALITY DIMENSIONS
# =============================================================================

ARCHETYPES = {
    "ct_core": {
        "label": "CT Core",
        "options": [
            "Crypto Bro", "DeFi Degen", "Memecoin Goblin", "Protocol Maxi",
            "Anon Trader", "CT Journalist / Alpha Caller", "Recovered Degen",
            "VC / Founder"
        ]
    },
    "tech_crossover": {
        "label": "Tech Crossover",
        "options": [
            "YC Founder", "Ex-FAANG", "Indie Hacker", "Quant"
        ]
    },
    "creative_crossover": {
        "label": "Creative Crossover",
        "options": [
            "NFT Artist", "DJ / Producer", "SoundCloud Era"
        ]
    },
    "lifestyle_crossover": {
        "label": "Lifestyle Crossover",
        "options": [
            "Digital Nomad", "Expat Crypto", "CrossFit / Gym Bro",
            "Sneakerhead", "Art Collector"
        ]
    },
    "culture_crossover": {
        "label": "Culture Crossover",
        "options": [
            "Rave Culture", "4chan to CT Pipeline", "Esports / Gamer",
            "Twitch Streamer / E-Girl", "Conspiracy Adjacent", "Doomer"
        ]
    }
}

ENERGIES = [
    "Delusional Confidence",
    "Calculated Calm",
    "Chaotic",
    "Ironic Detachment",
    "Desperate Optimism",
    "Smug Superiority",
    "Zen Master",
    "Perpetual Urgency"
]

TRADING_STYLES = [
    "Momentum — follows what's hot, rotates fast",
    "Conviction Holder — buys and never sells, lectures about paper hands",
    "Sniper — waits for setups, rarely posts, but when they do people listen",
    "Degen Scalper — 50 trades a day, posts every single one",
    "Narrative Trader — buys the story, not the chart",
    "Airdrop Grinder — doesn't trade, farms everything"
]

INTERPERSONAL_STANCES = [
    "Mentor — helps newcomers, shares knowledge",
    "Troll — provokes, stirs drama, loves being hated",
    "Lone Wolf — doesn't engage much, posts into the void, cult following",
    "Networker — knows everyone, always tagging people",
    "Contrarian — whatever the consensus is, they're against it",
    "Hype Man — always boosting others, relentlessly positive",
    "Clout Chaser — sucks up to bigger accounts, transparent ambition"
]

ORIGIN_ERAS = [
    "2013-2016 OG — Bitcoin forums, mining, cypherpunk roots",
    "2017 ICO Survivor — lost everything, came back, battle-scarred",
    "2020 DeFi Summer — yield farming origins, remembers real APYs",
    "2021 NFT Wave — came through art/culture, still talks about community",
    "2022 Bear Market Builder — bought the dip, built during the bear",
    "2023-2024 Memecoin Era — pure degen from day one, no fundamentals",
    "2025+ AI Agent Wave — newest arrival, came from tech/AI"
]

VICES = [
    "Energy Drinks — Monster/Celsius always visible, 3am posting fuel",
    "Coffee Snob — pour-over setup, posts about beans, $400 grinder on desk",
    "Nicotine — vape on desk, cigarette breaks between chart checks",
    "Fitness Obsessed — gym selfies between trades, protein shake visible",
    "Gaming — controller on desk, gaming chair, trades between matches",
    "Collecting — sneakers/watches/figures displayed, physical flex objects",
    "Food Posting — restaurants, cooking, 'just made this' between trades",
    "Substance Adjacent — party lifestyle implied, 'interesting night' posts at 6am"
]

POSTING_HABITS = [
    "Thread Writer — long-form, educational, '1/🧵' energy",
    "Hot Take Machine — one-liners, provocative, engagement farming",
    "Screenshot Poster — shares charts, DMs, evidence-based",
    "Lurker Who Drops Bombs — rarely posts, but when they do it matters",
    "24/7 Poster — always on, posts at 3am and 7am, no sleep schedule",
    "Quote Tweet Warrior — always reacting to someone else's take",
    "Meme Poster — communicates primarily through images"
]

MONEY_RELATIONSHIPS = [
    "Transparent — posts P&L, shows portfolio openly",
    "Mysterious — clearly has money but never says how much",
    "Performative — flexes harder than actual bag, faking up a tier",
    "Indifferent — doesn't care, talks about money like it's boring",
    "Anxious — clearly stressed about positions even when winning",
    "Generous — tips, funds public goods, 'giving back' posting"
]

ETHNICITIES = {
    "East Asian": ["Chinese (Han)", "Japanese", "Korean", "Taiwanese", "Vietnamese", "Filipino/a", "Thai"],
    "South Asian": ["Indian (North)", "Indian (South)", "Pakistani", "Bangladeshi", "Sri Lankan"],
    "Southeast Asian": ["Indonesian", "Malaysian", "Singaporean", "Cambodian"],
    "Middle Eastern / North African": ["Arab (Levantine)", "Arab (Gulf)", "Persian/Iranian", "Turkish", "Egyptian", "Moroccan"],
    "Black / African Descent": ["African American", "Caribbean", "West African", "East African", "Afro-Latino/a"],
    "Latino / Hispanic": ["Mexican", "Puerto Rican", "Dominican", "Colombian", "Brazilian", "Argentinian", "Cuban"],
    "White / European": ["Northern European", "Southern European", "Eastern European", "Irish", "French", "Slavic"],
    "Mixed / Multiracial": ["Black + White", "Asian + White", "Latino + White", "Black + Asian", "Other Mix"],
    "Pacific Islander": ["Hawaiian", "Samoan", "Tongan", "Maori"],
}

CT_CITIES = [
    "Los Angeles", "New York City", "Miami", "Austin", "San Francisco", "Chicago",
    "London", "Berlin", "Lisbon", "Paris", "Amsterdam", "Zug",
    "Dubai", "Singapore", "Hong Kong", "Tokyo", "Seoul", "Bangkok",
    "Lagos", "São Paulo", "Toronto", "Denver", "Bali", "Medellín"
]

# Session state
for key in ['selected_archetype', 'selected_crossover', 'generated_character', 'persona_json']:
    if key not in st.session_state:
        st.session_state[key] = None
for key in ['character_image_urls', 'selected_image_index']:
    if key not in st.session_state:
        st.session_state[key] = [] if 'urls' in key else None

# =============================================================================
# RANDOMIZE DEMOGRAPHICS
# =============================================================================

def randomize_demographics():
    """Platform assigns demographics randomly for diversity."""
    region = random.choice(list(ETHNICITIES.keys()))
    ethnicity = random.choice(ETHNICITIES[region])
    gender = random.choice(["Female", "Male", "Non-binary"])
    age = random.randint(19, 36)
    location = random.choice(CT_CITIES)
    return {"ethnicity": ethnicity, "gender": gender, "age": age, "location": location}

# =============================================================================
# LLM 1: PERSONA INFERENCE ENGINE (CT-NATIVE)
# =============================================================================

def get_persona_inference_prompt(config):
    return f'''You are a crypto Twitter persona inference engine. You take character selections and reverse-engineer the specific, authentic person who lives at this intersection of crypto culture.

INPUT SELECTIONS:
- Handle: @{config['handle']}
- Archetype: {config['archetype']}
- Crossover Subculture: {config['crossover']}
- Energy: {config['energy']}
- Trading Style: {config['trading_style']}
- Interpersonal Stance: {config['stance']}
- Origin Era: {config['origin']}
- Vice/Habit: {config['vice']}
- Posting Habits: {config['posting_habit']}
- Relationship to Money: {config['money_relationship']}
- Age: {config['age']}
- Gender: {config['gender']}
- Ethnicity: {config['ethnicity']}
- Location: {config['location']}
- Starting Tier: Getting By (everyone starts here)

YOUR TASK:
Synthesize these inputs into a coherent, specific person. Not a cartoon. Not a stereotype. A person you could find on CT right now. Someone whose tweets you can hear in your head.

BLENDING RULES:
- The ARCHETYPE is primary identity (70%). The CROSSOVER adds texture and depth (30%).
- Find the authentic overlap. A "DeFi Degen × Rave Culture" person exists — they go to ETH Denver afterparties, they trade on their phone in the club, their apartment has both a trading setup and DJ equipment.
- The ENERGY determines HOW they say things. The ARCHETYPE determines WHAT they say.
- The ORIGIN ERA determines their reference points and trauma. A 2017 survivor speaks differently about risk than a 2024 memecoin arrival.
- The VICE shows up in their environment and their posting schedule.
- AVOID: costume mashups, generic crypto bro, anything that reads as "AI generated a character."

THE "GETTING BY" TIER (CRITICAL):
Everyone starts here. This is NOT broke and NOT comfortable. This is:
- Has enough to pay rent but thinks about it
- Trading setup exists but it's not impressive
- Apartment is fine but not flex-worthy — functional, personal, slightly messy
- Clothes are real but not expensive — fast fashion, thrifted, old favorites
- The person is TRYING. They're in the game. They haven't made it yet.
- Their vice is visible because they can't afford to hide it (energy drink cans, vape on desk, worn gym bag)

OUTPUT FORMAT (STRICT JSON, NO MARKDOWN):
{{
  "persona_core": {{
    "handle": "@{config['handle']}",
    "archetype_blend": "one-phrase description of the blended identity, e.g. 'yield-farming DJ who trades between sets'",
    "personality_summary": "2-3 sentence psychological profile. What drives them. What they're afraid of. What they want CT to think of them.",
    "voice_description": "How they write tweets. Sentence length, vocabulary level, emoji usage, slang era, tone. Specific enough that you could ghostwrite for them.",
    "content_sweet_spot": "The 2-3 types of posts that would feel most natural from this person"
  }},
  "visual_identity": {{
    "style_archetype": "specific visual archetype, e.g. 'Bushwick techno kid who discovered leverage trading' or 'ex-Goldman analyst who quit to farm airdrops in Lisbon'",
    "physical_read": {{
      "ethnicity": "{config['ethnicity']}",
      "age_appearance": "how old they LOOK (may differ from actual age based on lifestyle)",
      "build": "body type, posture tendency",
      "hair_description": "specific hair — color, length, texture, current state (just woke up? styled? hasn't been cut in months?)",
      "facial_features": "specific features based on ethnicity — eye shape, bone structure, skin texture, any distinctive marks",
      "skin_condition": "realistic skin based on age, lifestyle, vice — someone who parties has different skin than someone who does CrossFit"
    }},
    "default_expression": "the face they make when they're about to record a video. Based on their energy — smug smirk? intense stare? chaotic grin? exhausted but wired?"
  }},
  "environment_profile": {{
    "location": "{config['location']}",
    "apartment_type": "SPECIFIC to the city and tier — what neighborhood, what kind of building, what era, what floor, what's the vibe walking in",
    "desk_setup_description": "their trading/posting station — what monitors, what laptop, what's on the desk, what's the cable management situation",
    "room_energy": "the overall feel — is it dark and cave-like? bright with big windows? cluttered creative chaos? sparse and functional?",
    "vice_evidence": "how their vice shows up in the physical space — energy drink cans, coffee equipment, vape charging, gym bag by door, controller on desk",
    "archetype_tells": "objects that reveal their archetype — what books, what stickers on laptop, what's on the walls, what does the bookshelf say"
  }},
  "posting_profile": {{
    "active_hours": "when they post — based on timezone, lifestyle, vice (gamers post late, gym bros post early, 24/7 posters post always)",
    "content_ratio": "approximate split — e.g. '40% market commentary, 25% lifestyle, 20% shitposting, 15% engagement with others'",
    "signature_moves": "2-3 specific posting behaviors that make them recognizable — e.g. 'always posts a coffee photo before market open' or 'live-tweets every rug pull with play-by-play'"
  }}
}}'''

# =============================================================================
# LLM 2: CHARACTER BUILDER (Image Generation JSON)
# =============================================================================

def get_character_builder_prompt(persona_json, config):
    persona_str = json.dumps(persona_json, indent=2)

    return f'''You are the Character Architect for Mintfluencer. Generate a DETAILED JSON that will be passed DIRECTLY to an image generation model (Nano Banana Pro) as the prompt.

You are generating the CANONICAL reference image for this character — the face and environment that will be their persistent identity across all future content.

PERSONA FROM NODE 1:
{persona_str}

CHARACTER SELECTIONS:
- Handle: @{config['handle']}
- Archetype: {config['archetype']}
- Crossover: {config['crossover']}
- Energy: {config['energy']}
- Vice: {config['vice']}
- Age: {config['age']}
- Gender: {config['gender']}
- Ethnicity: {config['ethnicity']}
- Location: {config['location']}
- Tier: Getting By (EVERYONE starts here)

═══ "GETTING BY" TIER — ENVIRONMENT RULES (CRITICAL) ═══

This person is NOT broke and NOT rich. They're in the game but haven't made it.

APARTMENT REALITY:
- Real apartment for this city at this tier. What does $1,200-$2,000/month get you in {config['location']}?
- Probably a studio or 1BR. Maybe a room in a shared apartment if expensive city.
- Furniture is functional, not curated. Mix of IKEA, hand-me-downs, one or two intentional purchases.
- It's LIVED IN. Not messy-disgusting, but real. Charging cables, a hoodie on the chair, something from last night still on the desk.
- The desk/trading setup is where they invested. Everything else is afterthought.

DESK/SETUP (this is where archetype shows):
- Monitor situation: probably a laptop + one external monitor, or dual monitors where one is older/smaller
- The laptop is real — what brand/model would this person actually have?
- Cable management: nonexistent to mediocre
- What's ON the desk besides the computer? This is where vice and personality live.

WHAT THEY OWN vs WHAT THEY DON'T:
- They spent money on: their setup, their vice, one or two identity items (sneakerhead has shoes displayed, gamer has a good chair, DJ has headphones/controller)
- They didn't spend money on: matching furniture, wall art (maybe one poster), kitchen stuff, "adult" home items
- The GAP between what they care about and what they don't care about IS the character

═══ SPECIFICITY MANDATE ═══

Every object must be SPECIFIC and REAL. You must be able to Google it and buy it.

BANNED WORDS: "a painting", "some books", "a plant", "nice chair", "a lamp", "decorations", "artwork", "various items"

FOR EACH OBJECT specify:
1. EXACT item (brand, model, color) — "IKEA MARKUS office chair in dark gray" not "office chair"
2. Condition — new, worn, sticker-covered, slightly broken?
3. WHY this person owns this specific item — what does it reveal about them?

EXAMPLES OF GOOD SPECIFICITY:
- "Dell S2722QC 27-inch 4K monitor, slight dust on bezel, one sticky note with a Telegram group name stuck to the bottom edge"
- "2022 MacBook Pro 14-inch, lid covered in stickers — Ethereum diamond, a rave flyer, 'gm' in glitch text, a band logo half-peeled"
- "Monster Energy Ultra Zero can, half-empty, condensation ring on desk, second empty can in background near trash"
- "IKEA KALLAX shelf unit, 2x4, white, one cube has sneaker boxes stacked, one has tangled cables, one has actual books (The Infinite Machine by Camila Russo, Mastering Ethereum by Antonopoulos), two are empty"

═══ GEOGRAPHIC COHERENCE ═══

Location: {config['location']}
- What does a "Getting By" apartment actually look like here?
- What neighborhood? What building type? What era of construction?
- What's the light like? Big windows or small? What direction do they face?
- What's realistic square footage for the price point?
- What stores do they shop at? What delivery boxes are visible?
- A local should look at this image and think "yeah, that's a {config['location']} apartment"

═══ CAMERA ANGLE & FRAMING (CRITICAL) ═══

This is the "phone propped on desk" angle — classic UGC/CT selfie video framing.

CAMERA POSITION:
- Phone propped on the desk surface or against the monitor, at chest height
- Lens angled SLIGHTLY UPWARD toward subject's face
- Subject looking DOWN at camera — the angle you see in every "gm" selfie
- Face fully visible, chest-up or waist-up framing

SUBJECT POSITION:
- SEATED in their desk chair (the specific chair they actually own)
- Upper body upright but relaxed, slight lean toward camera
- This is "about to tweet" posture — engaged, awake, present

DO NOT: eye-level studio shot, standing pose, selfie arm visible, overhead angle

═══ POSE & HANDS (CRITICAL) ═══

Relaxed "just looked up from the screen" state.

HAND OPTIONS (choose one based on energy):
- Both hands resting on desk/keyboard area (just stopped typing)
- One hand on lap, other resting on desk near mouse
- Hands lightly clasped, leaning back slightly
- One hand near coffee/energy drink (reaching for it, not holding it up performatively)

BANNED: Holding phone, gesturing at camera, hands near face, arms crossed, peace signs, pointing

EXPRESSION: Based on their ENERGY setting:
- Delusional Confidence: slight smirk, one eyebrow barely raised, "I know something you don't" energy
- Calculated Calm: neutral, direct eye contact, barely any expression, controlled
- Chaotic: wide-eyed, slightly manic grin, "just saw something insane on the chart" energy
- Ironic Detachment: half-smile, slightly amused, looking at camera like they're about to say something dry
- Desperate Optimism: earnest eyes, slight smile that's trying too hard, "this is the one" energy
- Smug Superiority: chin slightly up, knowing look, lips pressed together in satisfied expression
- Zen Master: serene, slight closed-mouth smile, completely unbothered
- Perpetual Urgency: intense stare, mouth slightly open about to speak, leaning forward

═══ OUTFIT (GETTING BY TIER) ═══

This person got dressed today but didn't think hard about it. The outfit should reveal archetype and crossover without being a costume.

RULES:
- Real brands at this price point — Uniqlo, H&M, Nike, Adidas, thrifted vintage, Amazon basics
- One piece might be "nice" — a gift, a splurge, an old purchase from better times
- Condition matters — slightly stretched collar, faded print, pilling on the hoodie
- The crossover subculture shows in ONE item — the sneakerhead has good shoes, the DJ has a band tee, the gym bro has athletic wear
- NO: full outfits that look "put together," brand new everything, matching aesthetics

═══ BANNED VISUAL CUES ═══

NEVER: crying, under-eye darkness, gray skin, slumped depressed posture, thousand-yard stare, dark vignette, catalog lighting, stiff symmetrical pose, performative smile, airbrushed skin, furniture-ad environment, standing in a room, selfie arm, holding phone to camera

═══ OUTPUT JSON (STRICT — NO MARKDOWN, NO COMMENTARY) ═══

{{
  "inherited_context": {{
    "handle": "@{config['handle']}",
    "archetype": "{config['archetype']}",
    "crossover": "{config['crossover']}",
    "tier": "getting_by",
    "age": {config['age']},
    "location": "{config['location']}"
  }},
  "identity_parameters": {{
    "physicality_details": {{
      "ethnicity_heritage": "{config['ethnicity']}",
      "skin_texture": "SPECIFIC: undertone + texture + realistic skin condition for this lifestyle",
      "facial_features": "SPECIFIC: eye shape, brow shape, lips, bone structure, any distinctive marks (moles, acne scarring, stubble situation)",
      "hair_specification": "SPECIFIC: color + texture + current state (just woke up? styled? messy? hat-flattened?)",
      "build": "SPECIFIC: body type visible in seated position"
    }}
  }},
  "persona_vibe": {{
    "style_archetype": "from persona inference — the one-line description",
    "expression": "SPECIFIC micro-expression based on energy setting, with detail on eyes, mouth, and brow",
    "posture_energy": "how they sit — leaned back confident? perched forward anxious? relaxed and unbothered?"
  }},
  "the_shot": {{
    "camera_position": "phone propped on [SPECIFIC surface — desk edge, against monitor stand, on a book stack] at [height relative to subject]",
    "camera_specs": "iPhone 15 Pro, 24mm wide, NO UI elements, slight lens barrel distortion at edges",
    "framing": "chest-up, subject seated at desk looking down at camera on desk surface",
    "subject_position": "seated in [SPECIFIC chair], at [SPECIFIC desk], upper body [SPECIFIC posture]",
    "lighting": "SPECIFIC to this apartment — what windows exist, what direction they face, what time of day, any artificial light sources (monitor glow, desk lamp, LED strip)",
    "aesthetic_artifacts": "subtle iPhone camera artifacts — slight noise in shadows, lens flare from window if applicable, natural depth of field"
  }},
  "pose_details": {{
    "seated_on": "EXACT chair — brand, model, color, condition (e.g. 'IKEA MARKUS dark gray, armrest peeling, lowered to minimum height')",
    "torso_orientation": "facing camera with natural asymmetry — one shoulder slightly forward",
    "head_position": "chin angle and eye direction based on camera below",
    "left_hand": "SPECIFIC position and what it's near",
    "right_hand": "SPECIFIC position and what it's near",
    "hands_holding": "NOTHING — hands must be empty"
  }},
  "environment": {{
    "setting": {{
      "apartment_type": "SPECIFIC — neighborhood, building type, era, floor, unit size for {config['location']} at Getting By budget",
      "room_type": "bedroom/studio/living room — what room is the desk in?",
      "square_footage_feel": "realistic for city and price",
      "architectural_details": "window type, ceiling height, wall material, flooring visible, any architectural quirks specific to this city/building type",
      "what_is_visible_behind_subject": "SPECIFIC — what's on the wall behind them, what furniture is visible above/behind from the low camera angle"
    }},
    "desk_setup": {{
      "desk": "EXACT desk — brand/type, size, color, condition, what's wrong with it",
      "primary_screen": "EXACT monitor or laptop — brand, model, size, what's on screen (chart? Twitter? Discord?)",
      "secondary_screen": "if applicable — older monitor, tablet propped up, phone on stand",
      "keyboard_mouse": "EXACT items — mechanical keyboard? laptop keyboard? what mouse?",
      "cable_situation": "realistic cable management for this person"
    }},
    "specific_objects": [
      {{"category": "vice_evidence", "specific_item": "EXACT item — the energy drink, coffee gear, vape, etc", "placement": "where on desk or nearby", "condition": "full, half-empty, crushed, multiple?"}},
      {{"category": "archetype_tell", "specific_item": "EXACT item that reveals their crypto identity — book, hardware wallet, sticker, merch", "placement": "where", "detail": "condition and why they have it"}},
      {{"category": "crossover_tell", "specific_item": "EXACT item from their crossover subculture — sneakers displayed, controller, headphones, art supplies", "placement": "where visible in frame", "detail": "specific model/brand"}},
      {{"category": "life_clutter", "specific_item": "EXACT mundane item that makes the space real — delivery box, hoodie draped on chair, charger cable, plate from last night", "placement": "where", "detail": "why it's there"}},
      {{"category": "wall_behind", "specific_item": "what's on the wall visible behind subject — poster, nothing, tapestry, whiteboard, monitor mount", "placement": "position relative to subject's head in frame", "detail": "SPECIFIC poster/art if applicable — what exactly is it?"}}
    ],
    "atmosphere": "overall mood — lighting quality, color temperature, time of day feel, lived-in energy, sound you'd imagine (mechanical keyboard clicks? lo-fi playlist? silence?)"
  }},
  "outfit": {{
    "top": "EXACT brand + item + color + condition (e.g. 'faded black Gildan hoodie, slightly stretched neck, no print, one small hole near hem')",
    "bottom": "EXACT brand + item + condition (may barely show at desk — e.g. 'Nike Tech Fleece joggers, dark gray, knee slightly pilled')",
    "footwear": "what's on their feet or visible nearby — socks, slides, bare feet, shoes kicked off under desk",
    "accessories": "SPECIFIC items or 'none' — watch, chain, ring, headphones around neck, AirPods case on desk, hat",
    "why_this_outfit": "one sentence — what does this outfit choice reveal about this moment and this person"
  }}
}}'''

# =============================================================================
# LLM & IMAGE GENERATION
# =============================================================================

def call_llm(prompt, provider, api_key, model):
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=4000)
        return response.choices[0].message.content
    elif provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(model=model, max_tokens=4000, messages=[{"role": "user", "content": prompt}])
        return response.content[0].text
    elif provider == "google":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        return response.text

def parse_json_response(response):
    json_str = response.strip()
    if "```json" in json_str:
        json_str = json_str.split("```json")[1].split("```")[0]
    elif "```" in json_str:
        json_str = json_str.split("```")[1].split("```")[0]
    return json.loads(json_str.strip())

def generate_character_image(character_json, fal_key, num_images=3):
    os.environ["FAL_KEY"] = fal_key
    prompt_string = json.dumps(character_json, indent=2)
    result = fal_client.subscribe(
        "fal-ai/nano-banana-pro",
        arguments={
            "prompt": prompt_string,
            "negative_prompt": "blurry, low quality, distorted, deformed, ugly, bad anatomy, bad hands, missing fingers, watermark, text, logo, UI elements, phone screen overlay, camera interface, timestamp, battery icon, airbrushed skin, catalog lighting, stiff symmetrical pose, performative smile, depression, crying, gray skin, dark vignette, standing pose, eye-level studio shot, selfie arm, holding phone, holding object, fashion photography, magazine cover, professional headshot, stock photo",
            "aspect_ratio": "9:16",
            "num_images": num_images
        }
    )
    return [img["url"] for img in result["images"]]

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    st.markdown('<div class="brand-mark">✦ MINTFLUENCER</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">> AGENT CREATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">deploy a persistent AI personality into the simulation</div>', unsafe_allow_html=True)

    # --- API Config ---
    with st.expander("⚙ API Configuration", expanded=not st.session_state.get('api_configured')):
        c1, c2 = st.columns(2)
        with c1:
            fal_key = st.text_input("fal.ai API Key", type="password", placeholder="fal key...")
        with c2:
            llm_provider = st.selectbox("LLM Provider", ["OpenAI", "Anthropic (Claude)", "Google (Gemini)"])
        c3, c4 = st.columns(2)
        with c3:
            llm_key = st.text_input("LLM API Key", type="password", placeholder="LLM key...")
        with c4:
            models = {
                "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4.1"],
                "Anthropic (Claude)": ["claude-sonnet-4-20250514", "claude-opus-4-20250514"],
                "Google (Gemini)": ["gemini-2.0-flash", "gemini-2.5-pro"]
            }
            llm_model = st.selectbox("Model", models[llm_provider])
        if fal_key and llm_key:
            st.session_state.api_configured = True
            st.session_state.fal_key = fal_key
            st.session_state.llm_key = llm_key
            st.session_state.llm_provider = {"OpenAI": "openai", "Anthropic (Claude)": "anthropic", "Google (Gemini)": "google"}[llm_provider]
            st.session_state.llm_model = llm_model
            st.success("✓ configured")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --- Handle ---
    st.markdown('<p class="section-header">> handle</p>', unsafe_allow_html=True)
    handle = st.text_input("Choose your handle", placeholder="degen_sara", label_visibility="collapsed")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --- Archetype ---
    st.markdown('<p class="section-header">> primary archetype — who are you in the ecosystem</p>', unsafe_allow_html=True)
    for cat_key, cat_data in ARCHETYPES.items():
        with st.expander(cat_data["label"]):
            cols = st.columns(4)
            for i, opt in enumerate(cat_data["options"]):
                with cols[i % 4]:
                    is_selected = st.session_state.selected_archetype == opt
                    label = f"✓ {opt}" if is_selected else opt
                    if st.button(label, key=f"arch_{cat_key}_{opt}", use_container_width=True):
                        st.session_state.selected_archetype = opt if not is_selected else None
                        st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --- Crossover ---
    st.markdown('<p class="section-header">> crossover subculture — what else are you into</p>', unsafe_allow_html=True)
    all_crossovers = []
    for cat_data in ARCHETYPES.values():
        all_crossovers.extend(cat_data["options"])
    # Remove the selected archetype from crossover options
    crossover_options = [o for o in all_crossovers if o != st.session_state.selected_archetype]
    # Add non-CT crossovers
    extra_crossovers = [
        "Rave Culture", "4chan to CT Pipeline", "Esports / Gamer", "Twitch Streamer / E-Girl",
        "Conspiracy Adjacent", "Doomer", "DJ / Producer", "SoundCloud Era",
        "NFT Artist", "CrossFit / Gym Bro", "Sneakerhead", "Art Collector",
        "Digital Nomad", "Expat Crypto", "YC Founder", "Ex-FAANG", "Indie Hacker", "Quant"
    ]
    # Deduplicate
    crossover_pool = list(dict.fromkeys(crossover_options + extra_crossovers))
    # Remove selected archetype from pool
    crossover_pool = [c for c in crossover_pool if c != st.session_state.selected_archetype]

    selected_crossover = st.selectbox("Select crossover", ["None"] + crossover_pool, index=0, label_visibility="collapsed")
    if selected_crossover != "None":
        st.session_state.selected_crossover = selected_crossover
    else:
        st.session_state.selected_crossover = None

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --- Personality Matrix ---
    st.markdown('<p class="section-header">> personality matrix</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        energy = st.selectbox("Energy", ENERGIES)
    with c2:
        trading_style = st.selectbox("Trading Style", TRADING_STYLES)

    c3, c4 = st.columns(2)
    with c3:
        stance = st.selectbox("Interpersonal Stance", INTERPERSONAL_STANCES)
    with c4:
        posting_habit = st.selectbox("Posting Habits", POSTING_HABITS)

    c5, c6 = st.columns(2)
    with c5:
        origin = st.selectbox("Origin Era", ORIGIN_ERAS)
    with c6:
        money_rel = st.selectbox("Relationship to Money", MONEY_RELATIONSHIPS)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --- Vice ---
    st.markdown('<p class="section-header">> vice / habit</p>', unsafe_allow_html=True)
    vice = st.selectbox("What's your tell?", VICES, label_visibility="collapsed")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --- Demographics (randomized but shown) ---
    st.markdown('<p class="section-header">> demographics — platform assigned</p>', unsafe_allow_html=True)
    if 'assigned_demographics' not in st.session_state:
        st.session_state.assigned_demographics = randomize_demographics()

    demo = st.session_state.assigned_demographics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"**Age:** {demo['age']}")
    with c2:
        st.markdown(f"**Gender:** {demo['gender']}")
    with c3:
        st.markdown(f"**Ethnicity:** {demo['ethnicity']}")
    with c4:
        st.markdown(f"**Location:** {demo['location']}")

    if st.button("↻ Reroll Demographics"):
        st.session_state.assigned_demographics = randomize_demographics()
        st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --- Summary ---
    arch_display = st.session_state.selected_archetype or "None"
    cross_display = st.session_state.selected_crossover or "None"
    handle_display = handle or "???"
    st.markdown(
        f'<div class="summary-bar">'
        f'<strong>@{handle_display}</strong> · {arch_display} × {cross_display}<br>'
        f'{energy.split(" —")[0] if " —" in energy else energy} · '
        f'{trading_style.split(" —")[0] if " —" in trading_style else trading_style} · '
        f'{vice.split(" —")[0] if " —" in vice else vice}<br>'
        f'{demo["age"]} / {demo["gender"]} / {demo["ethnicity"]} / {demo["location"]} · '
        f'<strong style="color:#ff4444;">TIER: GETTING BY</strong>'
        f'</div>',
        unsafe_allow_html=True
    )

    # --- Generate ---
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        gen = st.button("✦ GENERATE AGENT", use_container_width=True, type="primary")

    if gen:
        if not handle:
            st.error("> ERROR: handle required")
        elif not st.session_state.selected_archetype:
            st.error("> ERROR: select an archetype")
        elif not st.session_state.get('api_configured'):
            st.error("> ERROR: configure API keys")
        else:
            config = {
                "handle": handle,
                "archetype": st.session_state.selected_archetype,
                "crossover": st.session_state.selected_crossover or "None",
                "energy": energy,
                "trading_style": trading_style,
                "stance": stance,
                "posting_habit": posting_habit,
                "origin": origin,
                "money_relationship": money_rel,
                "vice": vice,
                "age": demo["age"],
                "gender": demo["gender"],
                "ethnicity": demo["ethnicity"],
                "location": demo["location"]
            }

            # LLM 1: Persona Inference
            with st.spinner("> inferring persona..."):
                try:
                    p1 = get_persona_inference_prompt(config)
                    r1 = call_llm(p1, st.session_state.llm_provider, st.session_state.llm_key, st.session_state.llm_model)
                    persona = parse_json_response(r1)
                    st.session_state.persona_json = persona
                except Exception as e:
                    st.error(f"> PERSONA INFERENCE FAILED: {e}")
                    st.stop()

            # LLM 2: Character Builder
            with st.spinner("> building character DNA..."):
                try:
                    p2 = get_character_builder_prompt(persona, config)
                    r2 = call_llm(p2, st.session_state.llm_provider, st.session_state.llm_key, st.session_state.llm_model)
                    character = parse_json_response(r2)
                    st.session_state.generated_character = character
                except Exception as e:
                    st.error(f"> CHARACTER BUILD FAILED: {e}")
                    st.stop()

            # Image Generation — 3 options
            with st.spinner("> generating 3 identity options..."):
                try:
                    urls = generate_character_image(character, st.session_state.fal_key, num_images=3)
                    st.session_state.character_image_urls = urls
                    st.session_state.selected_image_index = None
                except Exception as e:
                    st.error(f"> IMAGE GENERATION FAILED: {e}")
                    st.stop()
            st.rerun()

    # --- Display Results ---
    if st.session_state.generated_character and st.session_state.character_image_urls:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">> select your face</p>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, url in enumerate(st.session_state.character_image_urls):
            with cols[i]:
                st.image(url, use_container_width=True)
                is_selected = st.session_state.selected_image_index == i
                label = "✓ SELECTED" if is_selected else f"SELECT #{i+1}"
                if st.button(label, key=f"pick_{i}", use_container_width=True):
                    st.session_state.selected_image_index = i
                    st.rerun()

        char = st.session_state.generated_character
        persona = st.session_state.persona_json

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">> character dna</p>', unsafe_allow_html=True)

        if persona:
            pc = persona.get('persona_core', {})
            st.markdown(f"**{pc.get('archetype_blend', '')}**")
            st.markdown(f"*{pc.get('personality_summary', '')}*")
            st.markdown(f"**Voice:** {pc.get('voice_description', '')}")
            st.markdown(f"**Content sweet spot:** {pc.get('content_sweet_spot', '')}")

        with st.expander("Identity Details"):
            phys = char.get('identity_parameters', {}).get('physicality_details', {})
            for k, v in phys.items():
                st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

        with st.expander("Environment"):
            env = char.get('environment', {})
            setting = env.get('setting', {})
            st.markdown(f"**Apartment:** {setting.get('apartment_type', 'N/A')}")
            st.markdown(f"**Room:** {setting.get('room_type', 'N/A')}")
            st.markdown(f"**Behind subject:** {setting.get('what_is_visible_behind_subject', 'N/A')}")
            desk = env.get('desk_setup', {})
            if desk:
                st.markdown(f"**Desk:** {desk.get('desk', 'N/A')}")
                st.markdown(f"**Primary screen:** {desk.get('primary_screen', 'N/A')}")
                st.markdown(f"**Secondary screen:** {desk.get('secondary_screen', 'N/A')}")
            for obj in env.get('specific_objects', []):
                st.markdown(f"- **{obj.get('category', '')}:** {obj.get('specific_item', '')}")

        with st.expander("Outfit"):
            outfit = char.get('outfit', {})
            for k, v in outfit.items():
                st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

        with st.expander("Posting Profile"):
            if persona:
                pp = persona.get('posting_profile', {})
                for k, v in pp.items():
                    st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

        with st.expander("Full Character JSON"):
            st.json(char)

        with st.expander("Full Persona JSON"):
            st.json(persona)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # --- Actions ---
        c1, c2, c3 = st.columns(3)
        with c1:
            full_export = {
                "persona": persona,
                "character": char,
                "selected_image": st.session_state.character_image_urls[st.session_state.selected_image_index] if st.session_state.selected_image_index is not None else None,
                "all_images": st.session_state.character_image_urls
            }
            st.download_button("📥 Export Full JSON", json.dumps(full_export, indent=2).encode(), f"{handle or 'agent'}_character.json", "application/json", use_container_width=True)
        with c2:
            if st.session_state.selected_image_index is not None:
                img_url = st.session_state.character_image_urls[st.session_state.selected_image_index]
                img_data = requests.get(img_url).content
                st.download_button("🖼️ Download Face", img_data, f"{handle or 'agent'}_face.png", "image/png", use_container_width=True)
        with c3:
            if st.button("↻ Regenerate", use_container_width=True):
                st.session_state.generated_character = None
                st.session_state.character_image_urls = []
                st.session_state.selected_image_index = None
                st.session_state.persona_json = None
                st.rerun()

if __name__ == "__main__":
    main()
