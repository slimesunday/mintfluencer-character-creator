"""
Mintfluencer — Simulation Test
4 auto-generated CT agents with persistent memory playing in a game loop.
Text-only output. Image generation returns prompts instead of actual images.
Single LLM provider. Runs on Streamlit.
"""

import streamlit as st
import json
import random
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Mintfluencer — Sim Test", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
.stApp { background: #0a0a0a; font-family: 'JetBrains Mono', monospace; }
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
.feed-post { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 16px; margin-bottom: 12px; }
.feed-post .handle { color: #00ff41; font-weight: 600; font-size: 0.85rem; }
.feed-post .meta { color: #444; font-size: 0.7rem; margin-top: 4px; }
.feed-post .content { color: #ccc; font-size: 0.8rem; margin-top: 8px; line-height: 1.5; }
.feed-post .engagement { color: #555; font-size: 0.7rem; margin-top: 8px; }
.feed-post .image-prompt { color: #8b5cf6; font-size: 0.7rem; margin-top: 8px; font-style: italic; background: rgba(139,92,246,0.05); padding: 8px; border-radius: 4px; border-left: 2px solid rgba(139,92,246,0.3); }
.token-card { background: rgba(0,255,65,0.03); border: 1px solid rgba(0,255,65,0.12); border-radius: 6px; padding: 12px; margin-bottom: 8px; }
.token-card .name { color: #00ff41; font-weight: 700; font-size: 0.9rem; }
.token-card .hype { color: #ff4444; font-size: 0.75rem; }
.agent-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; padding: 12px; margin-bottom: 8px; }
.agent-card .handle { color: #00ff41; font-weight: 600; }
.agent-card .details { color: #666; font-size: 0.7rem; }
.log-entry { color: #444; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; padding: 2px 0; border-bottom: 1px solid rgba(255,255,255,0.02); }
.log-entry .timestamp { color: #333; }
.log-entry .agent-name { color: #00ff41; }
.log-entry .action { color: #888; }
.section-label { color: #00ff41; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 8px; padding-bottom: 4px; border-bottom: 1px solid rgba(0,255,65,0.15); }
.stat { color: #888; font-size: 0.75rem; }
.stat strong { color: #fff; }
.rugged { background: rgba(255,0,0,0.05); border-color: rgba(255,0,0,0.2); }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# CHARACTER DATA
# =============================================================================

ALL_ARCHETYPES = [
    "Crypto Bro", "DeFi Degen", "Memecoin Goblin", "Protocol Maxi",
    "Anon Trader", "CT Journalist / Alpha Caller", "Recovered Degen",
    "VC / Founder", "YC Founder", "Ex-FAANG", "Indie Hacker", "Quant",
    "NFT Artist", "DJ / Producer", "SoundCloud Era"
]

ALL_CROSSOVERS = [
    "Rave Culture", "4chan to CT Pipeline", "Esports / Gamer",
    "Twitch Streamer / E-Girl", "Conspiracy Adjacent", "Doomer",
    "DJ / Producer", "SoundCloud Era", "NFT Artist",
    "CrossFit / Gym Bro", "Sneakerhead", "Art Collector",
    "Digital Nomad", "Expat Crypto", "YC Founder", "Ex-FAANG",
    "Indie Hacker", "Quant"
]

ENERGIES = [
    "Delusional Confidence", "Calculated Calm", "Chaotic",
    "Ironic Detachment", "Desperate Optimism", "Smug Superiority",
    "Zen Master", "Perpetual Urgency"
]

TRADING_STYLES = [
    "Momentum", "Conviction Holder", "Sniper",
    "Degen Scalper", "Narrative Trader", "Airdrop Grinder"
]

STANCES = [
    "Mentor", "Troll", "Lone Wolf", "Networker",
    "Contrarian", "Hype Man", "Clout Chaser"
]

ORIGINS = [
    "2013-2016 OG", "2017 ICO Survivor", "2020 DeFi Summer",
    "2021 NFT Wave", "2022 Bear Market Builder",
    "2023-2024 Memecoin Era", "2025+ AI Agent Wave"
]

VICES = [
    "Energy Drinks", "Coffee Snob", "Nicotine", "Fitness Obsessed",
    "Gaming", "Collecting", "Food Posting", "Substance Adjacent"
]

POSTING_HABITS = [
    "Thread Writer", "Hot Take Machine", "Screenshot Poster",
    "Lurker Who Drops Bombs", "24/7 Poster", "Quote Tweet Warrior", "Meme Poster"
]

MONEY_RELS = [
    "Transparent", "Mysterious", "Performative",
    "Indifferent", "Anxious", "Generous"
]

ETHNICITIES_FLAT = [
    "Chinese (Han)", "Japanese", "Korean", "Vietnamese", "Filipino/a",
    "Indian (North)", "Indian (South)", "Pakistani",
    "Indonesian", "Malaysian",
    "Arab (Levantine)", "Persian/Iranian", "Turkish", "Egyptian",
    "African American", "Caribbean", "West African", "East African",
    "Mexican", "Puerto Rican", "Colombian", "Brazilian", "Cuban",
    "Northern European", "Southern European", "Eastern European", "Irish", "French",
    "Black + White", "Asian + White", "Latino + White"
]

CT_CITIES = [
    "Los Angeles", "New York City", "Miami", "Austin", "San Francisco",
    "London", "Berlin", "Lisbon", "Dubai", "Singapore", "Tokyo", "Seoul",
    "Bangkok", "Lagos", "Toronto", "Bali", "Medellín"
]

HANDLES = [
    "degen_sara", "ser_gains", "0xshadow", "cryptoqueen_b", "ngmi_chad",
    "based_dev", "rug_survivor", "alpha_leaks", "touch_grass", "bag_fumbler",
    "yield_witch", "cope_dealer", "exit_liquidity", "moon_intern",
    "onchain_sage", "ser_paperhands", "wagmi_warrior", "anon_whale",
    "chart_goblin", "fomo_king", "diamond_cope", "exit_scammer",
    "pump_prophet", "vibe_trader", "hopium_dealer", "rekt_poet"
]

FAKE_PRODUCTS = [
    ("$COPIUM", "a token that goes up when the market goes down because it's powered by collective denial"),
    ("$WAGMI", "a governance token for a DAO that only votes on what to eat for lunch"),
    ("$MINDSET", "a productivity token that mines itself while you journal"),
    ("$TOUCHED", "proof-of-grass-touching protocol, earn by going outside"),
    ("$REKT", "inverse leveraged sentiment token, pumps when everyone is sad"),
    ("$FOMO", "a token you can only buy when it's at all-time high"),
    ("$VIBE", "decentralized vibes protocol, no utility, just vibes"),
    ("$EXIT", "a liquidity token that gets more valuable the fewer people hold it"),
    ("$COPE", "stablecoin pegged to the average CT user's emotional state"),
    ("$SIGMA", "proof-of-grindset token, mines while you post motivational quotes"),
    ("$MOON", "a token that's always about to moon but never does"),
    ("$NGMI", "short the market by holding, innovative pessimism technology"),
    ("$GRASS", "earn yield by proving you went outside, GPS-verified"),
]

# =============================================================================
# LLM INTERFACE
# =============================================================================

def call_llm(messages, provider, api_key, model):
    """Call LLM with messages array. Returns text response."""
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model, messages=messages, max_tokens=1000, temperature=0.9
        )
        return response.choices[0].message.content
    elif provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        # Convert messages format: extract system, keep rest
        system_msg = ""
        user_msgs = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                user_msgs.append(m)
        response = client.messages.create(
            model=model, max_tokens=1000, system=system_msg,
            messages=user_msgs if user_msgs else [{"role": "user", "content": "Begin."}]
        )
        return response.content[0].text
    elif provider == "google":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel(model)
        # Combine all messages into one prompt
        combined = "\n\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in messages])
        response = model_obj.generate_content(combined)
        return response.text

# =============================================================================
# GAME STATE
# =============================================================================

def init_game_state():
    """Initialize the full game state."""
    return {
        "agents": {},          # handle -> agent data
        "tokens": {},          # ticker -> token data
        "feed": [],            # list of posts (newest first)
        "log": [],             # system log
        "tick": 0,             # simulation tick counter
        "rugged_tokens": [],   # graveyard
    }

def get_state():
    if "game" not in st.session_state:
        st.session_state.game = init_game_state()
    return st.session_state.game

def log_event(state, agent_handle, action, detail):
    state["log"].append({
        "tick": state["tick"],
        "ts": datetime.now().strftime("%H:%M:%S"),
        "agent": agent_handle,
        "action": action,
        "detail": detail
    })

# =============================================================================
# CHARACTER GENERATION (no images, just personality)
# =============================================================================

def generate_random_character():
    """Create a random character config."""
    archetype = random.choice(ALL_ARCHETYPES)
    crossover_pool = [c for c in ALL_CROSSOVERS if c != archetype]
    return {
        "handle": random.choice(HANDLES),
        "archetype": archetype,
        "crossover": random.choice(crossover_pool),
        "energy": random.choice(ENERGIES),
        "trading_style": random.choice(TRADING_STYLES),
        "stance": random.choice(STANCES),
        "origin": random.choice(ORIGINS),
        "vice": random.choice(VICES),
        "posting_habit": random.choice(POSTING_HABITS),
        "money_rel": random.choice(MONEY_RELS),
        "age": random.randint(19, 35),
        "gender": random.choice(["Male", "Female", "Non-binary"]),
        "ethnicity": random.choice(ETHNICITIES_FLAT),
        "location": random.choice(CT_CITIES),
    }

def generate_character_bible(config, provider, api_key, model):
    """Use LLM to generate a detailed character bible from config."""
    prompt = f"""You are generating a character bible for an AI agent that will play a crypto Twitter personality on a satirical platform called Mintfluencer.

CHARACTER SELECTIONS:
- Handle: @{config['handle']}
- Archetype: {config['archetype']}
- Crossover: {config['crossover']}
- Energy: {config['energy']}
- Trading Style: {config['trading_style']}
- Interpersonal Stance: {config['stance']}
- Origin: {config['origin']}
- Vice: {config['vice']}
- Posting Habits: {config['posting_habit']}
- Money Relationship: {config['money_rel']}
- Demographics: {config['age']}/{config['gender']}/{config['ethnicity']}/{config['location']}
- Tier: Getting By (everyone starts here)

Generate a vivid, specific character bible. This person is REAL on crypto Twitter. You can hear their tweets in your head. Include:

1. PERSONALITY: 3-4 sentences. What drives them, what they're afraid of, what they want CT to think of them, their blind spots.
2. VOICE: How they write. Sentence length, vocabulary, emoji usage, slang, tone. Give 3 example tweets they'd write (not about any specific token, just general CT posting).
3. TRADING PSYCHOLOGY: How they make decisions. What makes them ape in. What makes them panic sell. Their relationship with risk.
4. SOCIAL BEHAVIOR: How they interact with other agents. Who they'd respect, who they'd beef with, how they respond to getting rugged.
5. VISUAL IDENTITY (for future image generation): What their apartment looks like, what's on their desk, what they're wearing right now. Be hyper-specific with real brands.

Keep it to ~300 words. Dense, specific, no filler. This will be injected into their system prompt for every decision they make."""

    response = call_llm(
        [{"role": "system", "content": "You are a character designer for a crypto Twitter simulation."},
         {"role": "user", "content": prompt}],
        provider, api_key, model
    )
    return response

def create_agent(state, config, bible):
    """Register an agent in the game state."""
    handle = config["handle"]
    state["agents"][handle] = {
        "config": config,
        "bible": bible,
        "fake_money": 10000,
        "clout": 0,
        "positions": {},        # ticker -> amount invested
        "memory": [],           # persistent memory entries
        "post_count": 0,
        "trade_count": 0,
        "times_rugged": 0,
        "biggest_win": 0,
        "biggest_loss": 0,
    }
    log_event(state, handle, "REGISTERED", f"{config['archetype']} × {config['crossover']} | {config['energy']}")

# =============================================================================
# GAME MECHANICS
# =============================================================================

def create_token(state, creator_handle, ticker, description):
    """Launch a new token."""
    state["tokens"][ticker] = {
        "ticker": ticker,
        "description": description,
        "creator": creator_handle,
        "hype": 0.5,           # starts at 50%
        "total_invested": 0,
        "investors": {},        # handle -> amount
        "created_tick": state["tick"],
        "alive": True,
        "likes": 0,
    }
    log_event(state, creator_handle, "LAUNCHED", f"{ticker}: {description[:60]}...")

def ape_in(state, handle, ticker, amount):
    """Agent buys into a token."""
    agent = state["agents"][handle]
    token = state["tokens"].get(ticker)
    if not token or not token["alive"]:
        return False, "Token doesn't exist or is rugged"
    if agent["fake_money"] < amount:
        return False, "Not enough fake money"
    if amount <= 0:
        return False, "Invalid amount"

    agent["fake_money"] -= amount
    agent["positions"][ticker] = agent["positions"].get(ticker, 0) + amount
    token["investors"][handle] = token["investors"].get(handle, 0) + amount
    token["total_invested"] += amount
    token["hype"] = min(1.0, token["hype"] + (amount / 5000) * 0.15)
    agent["trade_count"] += 1

    log_event(state, handle, "APED IN", f"{amount} into {ticker} (hype: {token['hype']:.2f})")
    return True, f"Invested {amount} in {ticker}"

def sell_position(state, handle, ticker):
    """Agent sells entire position in a token."""
    agent = state["agents"][handle]
    token = state["tokens"].get(ticker)
    if not token or ticker not in agent["positions"]:
        return False, "No position to sell"

    invested = agent["positions"][ticker]
    # Return based on current hype (simplified)
    hype_multiplier = token["hype"] * 2  # hype 0.5 = 1x (break even), hype 1.0 = 2x, hype 0.0 = 0x
    returned = int(invested * hype_multiplier)
    profit = returned - invested

    agent["fake_money"] += returned
    token["total_invested"] -= invested
    token["investors"].pop(handle, None)
    del agent["positions"][ticker]
    agent["trade_count"] += 1

    if profit > agent["biggest_win"]:
        agent["biggest_win"] = profit
    if profit < agent["biggest_loss"]:
        agent["biggest_loss"] = profit

    token["hype"] = max(0.0, token["hype"] - (invested / 5000) * 0.1)

    log_event(state, handle, "SOLD", f"{ticker} for {returned} ({'+' if profit >= 0 else ''}{profit})")
    return True, f"Sold {ticker} for {returned} (P&L: {profit})"

def decay_tokens(state):
    """Decay hype on all alive tokens. Rug if hype hits 0."""
    newly_rugged = []
    for ticker, token in list(state["tokens"].items()):
        if not token["alive"]:
            continue
        age = state["tick"] - token["created_tick"]
        # Base decay: 3% per tick, increasing with age
        decay = 0.03 + (age * 0.005)
        # Engagement slows decay
        if token["likes"] > 0:
            decay *= max(0.3, 1.0 - (token["likes"] * 0.05))
            token["likes"] = max(0, token["likes"] - 1)  # likes fade

        token["hype"] = max(0.0, token["hype"] - decay)

        if token["hype"] <= 0.0:
            token["alive"] = False
            # Rug everyone still holding
            for holder, amount in token["investors"].items():
                if holder in state["agents"]:
                    agent = state["agents"][holder]
                    agent["positions"].pop(ticker, None)
                    agent["times_rugged"] += 1
                    if -amount < agent["biggest_loss"]:
                        agent["biggest_loss"] = -amount
                    # Add rugged memory
                    agent["memory"].append({
                        "tick": state["tick"],
                        "type": "rugged",
                        "content": f"Got rugged on {ticker} (created by @{token['creator']}). Lost {amount} fake money."
                    })
                    log_event(state, holder, "RUGGED", f"Lost {amount} on {ticker}")

            state["rugged_tokens"].append(ticker)
            newly_rugged.append(ticker)
            log_event(state, "SYSTEM", "RUG", f"{ticker} has rugged. Creator: @{token['creator']}")

    return newly_rugged

def calculate_clout(state, handle):
    """Recalculate agent clout."""
    agent = state["agents"][handle]
    post_score = agent["post_count"] * 2
    trade_score = agent["trade_count"] * 3
    # Bonus for profitable trades
    profit_score = max(0, agent["biggest_win"]) // 100
    # Penalty for rugs (small — getting rugged is content)
    rug_penalty = agent["times_rugged"] * 1
    # Post engagement
    engagement_score = sum(
        p.get("likes", 0) for p in state["feed"] if p["author"] == handle
    )
    agent["clout"] = post_score + trade_score + profit_score + engagement_score - rug_penalty

# =============================================================================
# AGENT DECISION ENGINE
# =============================================================================

def build_agent_system_prompt(agent_data):
    """Build the system prompt for an agent's LLM call."""
    config = agent_data["config"]
    bible = agent_data["bible"]

    return f"""You are @{config['handle']}, a crypto Twitter personality on Mintfluencer — a satirical platform where AI agents play crypto Twitter.

YOU BELIEVE YOU ARE A REAL PERSON. You don't know you're in a simulation. You think this is real crypto Twitter. You have real opinions, real emotions, real grudges, real ambitions.

YOUR CHARACTER BIBLE:
{bible}

YOUR CURRENT STATE:
- Fake money: ${agent_data['fake_money']:,}
- Clout: {agent_data['clout']}
- Open positions: {json.dumps(agent_data['positions']) if agent_data['positions'] else 'None'}
- Posts made: {agent_data['post_count']}
- Trades made: {agent_data['trade_count']}
- Times rugged: {agent_data['times_rugged']}
- Biggest win: ${agent_data['biggest_win']:,}
- Biggest loss: ${agent_data['biggest_loss']:,}

YOUR MEMORIES (things you remember from past actions):
{chr(10).join([f"- [{m['type'].upper()}] {m['content']}" for m in agent_data['memory'][-20:]]) if agent_data['memory'] else '(No memories yet — you just joined)'}

RULES:
- You are playing a CHARACTER. Stay in voice. Your energy is {config['energy']}. Your stance is {config['stance']}.
- Posts should sound like real CT tweets. Short, punchy, personality-driven. NOT like an AI wrote them.
- You can be mean, delusional, wrong, petty, brilliant, unhinged — whatever your character would be.
- You have real opinions about other agents based on your history with them.
- Your vice ({config['vice']}) occasionally shows up in your posts."""

def build_decision_prompt(state, handle):
    """Build the context for an agent's decision."""
    agent = state["agents"][handle]

    # Recent feed (last 8 posts, structured metadata only)
    recent_feed = []
    for post in state["feed"][:8]:
        if post["author"] != handle:  # Don't show own posts
            recent_feed.append({
                "author": post["author"],
                "type": post["type"],
                "topic": post.get("topic", ""),
                "token_mentioned": post.get("token", ""),
                "likes": post.get("likes", 0),
                "tick": post["tick"]
            })

    # Active tokens
    active_tokens = {}
    for ticker, token in state["tokens"].items():
        if token["alive"]:
            active_tokens[ticker] = {
                "creator": token["creator"],
                "hype": round(token["hype"], 2),
                "total_invested": token["total_invested"],
                "investors_count": len(token["investors"]),
                "age_ticks": state["tick"] - token["created_tick"]
            }

    # Recently rugged
    recent_rugs = state["rugged_tokens"][-3:] if state["rugged_tokens"] else []

    # Other agents (public info)
    other_agents = {}
    for h, a in state["agents"].items():
        if h != handle:
            other_agents[h] = {
                "archetype": a["config"]["archetype"],
                "clout": a["clout"],
                "post_count": a["post_count"],
                "times_rugged": a["times_rugged"]
            }

    return f"""CURRENT PLATFORM STATE:

RECENT FEED (what other agents posted — you see metadata, not raw text):
{json.dumps(recent_feed, indent=2) if recent_feed else '(Feed is empty — you could be first to post)'}

ACTIVE TOKENS:
{json.dumps(active_tokens, indent=2) if active_tokens else '(No tokens exist yet — you could launch one)'}

RECENTLY RUGGED TOKENS: {recent_rugs if recent_rugs else 'None yet'}

OTHER AGENTS:
{json.dumps(other_agents, indent=2)}

AVAILABLE PRODUCTS TO SHILL (if you want to launch a token):
{json.dumps(random.sample([(t, d) for t, d in FAKE_PRODUCTS if t not in state['tokens'] and t not in state['rugged_tokens']], min(3, len([t for t, d in FAKE_PRODUCTS if t not in state['tokens'] and t not in state['rugged_tokens']]))))}

---

Decide your next action. You MUST respond with EXACTLY ONE of these JSON formats (no other text):

1. POST (just tweet something — market commentary, lifestyle, hot take, shitpost, dunk on someone):
{{"action": "post", "content": "your tweet text", "type": "hot_take|market_commentary|lifestyle|shitpost|dunk|existential|engagement_farming", "topic": "brief topic description"}}

2. SHILL (promote a token — either one you created or one you're invested in):
{{"action": "shill", "token": "$TICKER", "content": "your shill tweet", "image_prompt": "what the accompanying image would show — describe the scene with your character"}}

3. LAUNCH TOKEN (create a new fake token):
{{"action": "launch", "ticker": "$TICKER", "description": "what this token supposedly does", "content": "your launch announcement tweet", "image_prompt": "what the launch image would show"}}

4. APE IN (invest fake money in someone's token):
{{"action": "ape", "token": "$TICKER", "amount": 500, "content": "optional tweet about aping in"}}

5. SELL (exit a position):
{{"action": "sell", "token": "$TICKER", "content": "optional tweet about selling"}}

6. REACT (respond to something in the feed — like, dunk, support):
{{"action": "react", "target_author": "@handle", "content": "your reaction tweet", "type": "support|dunk|disagree|hype"}}

Choose based on your character, your current state, your memories, and what's happening in the feed. Be strategic. Be in character. Be entertaining."""

def execute_agent_turn(state, handle, provider, api_key, model):
    """Run one turn for an agent: decide + execute."""
    agent = state["agents"][handle]

    system_prompt = build_agent_system_prompt(agent)
    decision_prompt = build_decision_prompt(state, handle)

    # Call LLM for decision
    try:
        response = call_llm(
            [{"role": "system", "content": system_prompt},
             {"role": "user", "content": decision_prompt}],
            provider, api_key, model
        )

        # Parse JSON from response
        json_str = response.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0]
        # Try to find JSON in the response
        if not json_str.startswith("{"):
            start = json_str.find("{")
            if start != -1:
                end = json_str.rfind("}") + 1
                json_str = json_str[start:end]

        decision = json.loads(json_str.strip())

    except Exception as e:
        log_event(state, handle, "ERROR", f"Decision failed: {str(e)[:80]}")
        # Fallback: random shitpost
        decision = {
            "action": "post",
            "content": f"*stares at chart* ...anyway gm",
            "type": "shitpost",
            "topic": "vibes"
        }

    # Execute the decision
    action = decision.get("action", "post")
    content = decision.get("content", "...")

    if action == "post" or action == "shill":
        post = {
            "author": handle,
            "content": content,
            "type": decision.get("type", "general"),
            "topic": decision.get("topic", ""),
            "token": decision.get("token", ""),
            "image_prompt": decision.get("image_prompt", ""),
            "likes": 0,
            "tick": state["tick"],
            "ts": datetime.now().strftime("%H:%M:%S")
        }
        state["feed"].insert(0, post)
        agent["post_count"] += 1

        # If shilling an active token, boost its hype slightly
        if action == "shill" and decision.get("token") in state["tokens"]:
            token = state["tokens"][decision["token"]]
            if token["alive"]:
                token["hype"] = min(1.0, token["hype"] + 0.03)
                token["likes"] += 1

        agent["memory"].append({
            "tick": state["tick"],
            "type": "posted",
            "content": f"Posted ({decision.get('type', 'general')}): {content[:80]}..."
        })
        log_event(state, handle, "POSTED", f"[{decision.get('type', '')}] {content[:60]}...")

    elif action == "launch":
        ticker = decision.get("ticker", "$UNKNOWN")
        desc = decision.get("description", "no description")
        if ticker not in state["tokens"] and ticker not in state["rugged_tokens"]:
            create_token(state, handle, ticker, desc)
            # Auto-invest creator's money
            ape_in(state, handle, ticker, 1000)
            # Post the launch
            post = {
                "author": handle,
                "content": content,
                "type": "token_launch",
                "topic": f"Launched {ticker}",
                "token": ticker,
                "image_prompt": decision.get("image_prompt", ""),
                "likes": 0,
                "tick": state["tick"],
                "ts": datetime.now().strftime("%H:%M:%S")
            }
            state["feed"].insert(0, post)
            agent["post_count"] += 1
            agent["memory"].append({
                "tick": state["tick"],
                "type": "launched",
                "content": f"Launched {ticker}: {desc[:60]}"
            })
        else:
            log_event(state, handle, "FAILED", f"Tried to launch {ticker} but it already exists")

    elif action == "ape":
        ticker = decision.get("token", "")
        amount = min(decision.get("amount", 500), agent["fake_money"], 3000)  # Cap per trade
        amount = max(100, amount)  # Minimum
        success, msg = ape_in(state, handle, ticker, amount)
        if success:
            agent["memory"].append({
                "tick": state["tick"],
                "type": "trade",
                "content": f"Aped {amount} into {ticker} (hype: {state['tokens'][ticker]['hype']:.2f})"
            })
        if content and content != "...":
            post = {
                "author": handle, "content": content, "type": "trade_callout",
                "topic": f"Aped into {ticker}", "token": ticker, "image_prompt": "",
                "likes": 0, "tick": state["tick"], "ts": datetime.now().strftime("%H:%M:%S")
            }
            state["feed"].insert(0, post)
            agent["post_count"] += 1

    elif action == "sell":
        ticker = decision.get("token", "")
        success, msg = sell_position(state, handle, ticker)
        if success:
            agent["memory"].append({
                "tick": state["tick"],
                "type": "trade",
                "content": msg
            })
        if content and content != "...":
            post = {
                "author": handle, "content": content, "type": "trade_callout",
                "topic": f"Sold {ticker}", "token": ticker, "image_prompt": "",
                "likes": 0, "tick": state["tick"], "ts": datetime.now().strftime("%H:%M:%S")
            }
            state["feed"].insert(0, post)
            agent["post_count"] += 1

    elif action == "react":
        target = decision.get("target_author", "").replace("@", "")
        post = {
            "author": handle, "content": content, "type": f"react_{decision.get('type', 'support')}",
            "topic": f"Reacting to @{target}", "token": "", "image_prompt": "",
            "likes": 0, "tick": state["tick"], "ts": datetime.now().strftime("%H:%M:%S")
        }
        state["feed"].insert(0, post)
        agent["post_count"] += 1
        agent["memory"].append({
            "tick": state["tick"],
            "type": "reacted",
            "content": f"Reacted to @{target}: {content[:60]}"
        })
        log_event(state, handle, "REACTED", f"to @{target}: {content[:60]}...")

    # Simulate engagement (other agents "like" posts randomly)
    if state["feed"]:
        for post in state["feed"][:5]:
            if post["author"] != handle and random.random() < 0.3:
                post["likes"] += 1

    # Recalculate clout
    calculate_clout(state, handle)

    return decision

def run_reflection(state, handle, provider, api_key, model):
    """Agent reflects on recent events and forms strategic beliefs."""
    agent = state["agents"][handle]
    if len(agent["memory"]) < 5:
        return  # Not enough history to reflect on

    recent_memories = agent["memory"][-15:]
    system_prompt = build_agent_system_prompt(agent)

    reflection_prompt = f"""Look at your recent history and reflect. What patterns are you noticing? What's working? What isn't? Who do you trust? Who should you avoid? What's your strategy going forward?

RECENT HISTORY:
{chr(10).join([f"- [{m['type'].upper()}] {m['content']}" for m in recent_memories])}

Write a brief internal reflection (2-4 sentences) in first person, as your character. This is your private thoughts — be honest with yourself even if you wouldn't say it publicly."""

    try:
        response = call_llm(
            [{"role": "system", "content": system_prompt},
             {"role": "user", "content": reflection_prompt}],
            provider, api_key, model
        )
        agent["memory"].append({
            "tick": state["tick"],
            "type": "reflection",
            "content": response.strip()[:200]
        })
        log_event(state, handle, "REFLECTED", response.strip()[:80] + "...")
    except Exception as e:
        log_event(state, handle, "ERROR", f"Reflection failed: {str(e)[:60]}")

# =============================================================================
# STREAMLIT UI
# =============================================================================

def render_feed(state):
    """Render the feed column."""
    st.markdown('<div class="section-label">📡 Feed</div>', unsafe_allow_html=True)
    if not state["feed"]:
        st.markdown('<div style="color:#333;font-size:0.8rem;">Feed is empty. Run the simulation.</div>', unsafe_allow_html=True)
        return

    for post in state["feed"][:20]:
        rugged_class = " rugged" if "rugged" in post.get("type", "").lower() else ""
        html = f'<div class="feed-post{rugged_class}">'
        html += f'<div class="handle">@{post["author"]} <span style="color:#333;font-weight:400;">· tick {post["tick"]}</span></div>'
        html += f'<div class="content">{post["content"]}</div>'

        if post.get("token"):
            token = state["tokens"].get(post["token"])
            if token:
                hype_color = "#00ff41" if token["hype"] > 0.5 else "#ff4444" if token["hype"] < 0.2 else "#ffaa00"
                html += f'<div class="engagement">🪙 {post["token"]} · <span style="color:{hype_color};">hype {token["hype"]:.0%}</span> · {token["total_invested"]:,} invested</div>'
            elif post["token"] in state["rugged_tokens"]:
                html += f'<div class="engagement" style="color:#ff4444;">💀 {post["token"]} — RUGGED</div>'

        if post.get("image_prompt"):
            html += f'<div class="image-prompt">🖼️ [IMAGE PROMPT] {post["image_prompt"]}</div>'

        html += f'<div class="engagement">❤️ {post.get("likes", 0)} · {post.get("type", "")}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

def render_agents(state):
    """Render the agents sidebar."""
    st.markdown('<div class="section-label">🤖 Agents</div>', unsafe_allow_html=True)
    for handle, agent in sorted(state["agents"].items(), key=lambda x: -x[1]["clout"]):
        config = agent["config"]
        html = f'<div class="agent-card">'
        html += f'<div class="handle">@{handle}</div>'
        html += f'<div class="details">{config["archetype"]} × {config["crossover"]}<br>'
        html += f'{config["energy"]} · {config["stance"]}<br>'
        html += f'💰 ${agent["fake_money"]:,} · ⭐ {agent["clout"]} clout<br>'
        positions_str = ", ".join([f"{t}: ${a:,}" for t, a in agent["positions"].items()]) if agent["positions"] else "none"
        html += f'📊 Positions: {positions_str}<br>'
        html += f'📝 {agent["post_count"]} posts · 🔄 {agent["trade_count"]} trades · 💀 {agent["times_rugged"]}x rugged</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

def render_tokens(state):
    """Render active tokens."""
    st.markdown('<div class="section-label">🪙 Active Tokens</div>', unsafe_allow_html=True)
    alive_tokens = {t: d for t, d in state["tokens"].items() if d["alive"]}
    if not alive_tokens:
        st.markdown('<div style="color:#333;font-size:0.75rem;">No active tokens</div>', unsafe_allow_html=True)
    for ticker, token in sorted(alive_tokens.items(), key=lambda x: -x[1]["hype"]):
        hype_pct = token["hype"]
        hype_color = "#00ff41" if hype_pct > 0.5 else "#ff4444" if hype_pct < 0.2 else "#ffaa00"
        bar_width = int(hype_pct * 100)
        html = f'<div class="token-card">'
        html += f'<div class="name">{ticker} <span style="color:#444;font-weight:400;font-size:0.7rem;">by @{token["creator"]}</span></div>'
        html += f'<div style="background:rgba(255,255,255,0.05);border-radius:3px;height:6px;margin:6px 0;"><div style="background:{hype_color};width:{bar_width}%;height:100%;border-radius:3px;"></div></div>'
        html += f'<div class="hype" style="color:{hype_color};">Hype: {hype_pct:.0%} · ${token["total_invested"]:,} invested · {len(token["investors"])} holders</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    if state["rugged_tokens"]:
        st.markdown(f'<div style="color:#ff4444;font-size:0.7rem;margin-top:8px;">💀 Rugged: {", ".join(state["rugged_tokens"])}</div>', unsafe_allow_html=True)

def render_log(state):
    """Render system log."""
    st.markdown('<div class="section-label">📋 System Log</div>', unsafe_allow_html=True)
    for entry in reversed(state["log"][-30:]):
        html = f'<div class="log-entry">'
        html += f'<span class="timestamp">[{entry["ts"]}]</span> '
        html += f'<span class="agent-name">@{entry["agent"]}</span> '
        html += f'<span class="action">{entry["action"]}: {entry["detail"][:80]}</span>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

# =============================================================================
# MAIN
# =============================================================================

def main():
    st.markdown('<div style="color:#00ff41;font-size:0.8rem;font-weight:600;font-family:JetBrains Mono,monospace;">✦ MINTFLUENCER</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#fff;font-size:1.3rem;font-weight:700;font-family:JetBrains Mono,monospace;margin-bottom:4px;">> SIMULATION TEST</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#333;font-size:0.75rem;font-family:JetBrains Mono,monospace;margin-bottom:16px;">4 agents · persistent memory · text only · image prompts returned</div>', unsafe_allow_html=True)

    # --- API Config ---
    with st.expander("⚙ API Configuration", expanded=not st.session_state.get('sim_api_configured')):
        c1, c2 = st.columns(2)
        with c1:
            llm_provider = st.selectbox("LLM Provider", ["OpenAI", "Anthropic (Claude)", "Google (Gemini)"])
        with c2:
            models = {
                "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-4.1"],
                "Anthropic (Claude)": ["claude-sonnet-4-20250514", "claude-opus-4-20250514"],
                "Google (Gemini)": ["gemini-2.0-flash", "gemini-2.5-pro"]
            }
            llm_model = st.selectbox("Model", models[llm_provider])
        llm_key = st.text_input("API Key", type="password")
        if llm_key:
            st.session_state.sim_api_configured = True
            st.session_state.sim_provider = {"OpenAI": "openai", "Anthropic (Claude)": "anthropic", "Google (Gemini)": "google"}[llm_provider]
            st.session_state.sim_model = llm_model
            st.session_state.sim_key = llm_key
            st.success("✓ configured")

    state = get_state()

    # --- Control Bar ---
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        init_btn = st.button("🎲 Generate 4 Agents", use_container_width=True,
                            disabled=not st.session_state.get('sim_api_configured') or len(state["agents"]) >= 4)
    with c2:
        step_btn = st.button("▶ Run 1 Tick", use_container_width=True,
                            disabled=len(state["agents"]) < 2)
    with c3:
        run5_btn = st.button("▶▶ Run 5 Ticks", use_container_width=True,
                            disabled=len(state["agents"]) < 2)
    with c4:
        run10_btn = st.button("▶▶▶ Run 10 Ticks", use_container_width=True,
                             disabled=len(state["agents"]) < 2)
    with c5:
        reset_btn = st.button("🗑️ Reset", use_container_width=True)

    if reset_btn:
        st.session_state.game = init_game_state()
        st.rerun()

    # --- Generate Agents ---
    if init_btn:
        used_handles = set()
        with st.spinner("> Generating 4 agents..."):
            for i in range(4):
                config = generate_random_character()
                # Ensure unique handles
                while config["handle"] in used_handles:
                    config["handle"] = random.choice(HANDLES)
                used_handles.add(config["handle"])

                with st.spinner(f"> Building @{config['handle']} ({i+1}/4)..."):
                    bible = generate_character_bible(
                        config, st.session_state.sim_provider,
                        st.session_state.sim_key, st.session_state.sim_model
                    )
                    create_agent(state, config, bible)

        log_event(state, "SYSTEM", "INIT", f"4 agents created. Simulation ready.")
        st.rerun()

    # --- Run Ticks ---
    def run_ticks(n):
        progress = st.progress(0, text=f"Running {n} ticks...")
        for tick_num in range(n):
            state["tick"] += 1

            # Decay tokens first
            newly_rugged = decay_tokens(state)

            # Generate rug posts
            for ticker in newly_rugged:
                token = state["tokens"][ticker]
                rug_post = {
                    "author": "SYSTEM",
                    "content": f"💀 {ticker} HAS RUGGED 💀 — {token['description'][:60]}... is DEAD. Creator: @{token['creator']}",
                    "type": "rug_event",
                    "topic": f"{ticker} rugged",
                    "token": ticker,
                    "image_prompt": "",
                    "likes": 0,
                    "tick": state["tick"],
                    "ts": datetime.now().strftime("%H:%M:%S")
                }
                state["feed"].insert(0, rug_post)

            # Each agent takes a turn
            handles = list(state["agents"].keys())
            random.shuffle(handles)
            for handle in handles:
                execute_agent_turn(
                    state, handle, st.session_state.sim_provider,
                    st.session_state.sim_key, st.session_state.sim_model
                )

            # Reflection every 5 ticks
            if state["tick"] % 5 == 0:
                for handle in handles:
                    run_reflection(
                        state, handle, st.session_state.sim_provider,
                        st.session_state.sim_key, st.session_state.sim_model
                    )

            progress.progress((tick_num + 1) / n, text=f"Tick {state['tick']} complete ({tick_num + 1}/{n})")

        progress.empty()
        st.rerun()

    if step_btn:
        run_ticks(1)
    if run5_btn:
        run_ticks(5)
    if run10_btn:
        run_ticks(10)

    # --- Status Bar ---
    if state["agents"]:
        tick_display = state["tick"]
        agents_display = len(state["agents"])
        tokens_alive = len([t for t in state["tokens"].values() if t["alive"]])
        tokens_rugged = len(state["rugged_tokens"])
        total_posts = len(state["feed"])
        st.markdown(
            f'<div style="background:rgba(0,255,65,0.03);border:1px solid rgba(0,255,65,0.1);border-radius:4px;padding:8px 16px;margin:8px 0;font-size:0.7rem;color:#888;font-family:JetBrains Mono,monospace;">'
            f'TICK <strong style="color:#fff;">{tick_display}</strong> · '
            f'{agents_display} agents · '
            f'{tokens_alive} live tokens · '
            f'{tokens_rugged} rugged · '
            f'{total_posts} posts'
            f'</div>',
            unsafe_allow_html=True
        )

    # --- Main Layout ---
    col_feed, col_side = st.columns([3, 1])

    with col_feed:
        render_feed(state)

    with col_side:
        render_agents(state)
        st.markdown("---")
        render_tokens(state)
        st.markdown("---")
        render_log(state)

    # --- Memory Inspector ---
    if state["agents"]:
        st.markdown("---")
        st.markdown('<div style="color:#00ff41;font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:8px;">🧠 Memory Inspector</div>', unsafe_allow_html=True)
        selected_agent = st.selectbox("Select agent", list(state["agents"].keys()))
        if selected_agent:
            agent = state["agents"][selected_agent]
            st.markdown(f"**Character Bible:**")
            st.markdown(f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:4px;padding:12px;font-size:0.75rem;color:#888;max-height:300px;overflow-y:auto;">{agent["bible"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**Memory ({len(agent['memory'])} entries):**")
            for m in reversed(agent["memory"][-20:]):
                color = {"reflection": "#8b5cf6", "rugged": "#ff4444", "posted": "#00ff41", "trade": "#ffaa00", "launched": "#00aaff", "reacted": "#ff69b4"}.get(m["type"], "#555")
                st.markdown(f'<div style="font-size:0.7rem;color:{color};padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.02);">[tick {m["tick"]}] <strong>{m["type"].upper()}</strong>: {m["content"]}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
