#!/usr/bin/env python3
"""
ULTIMATE EPIC THEMES - Rich, detailed, comprehensive themes
Every theme uses MANY fields and shows real information
No duplicates, no boring repetition - each theme is unique!
"""

from typing import Dict, List, Any

# RGB Color definitions for ultimate themes
ULTIMATE_COLORS = {
    # Matrix Digital Rain
    "matrix_black": (5, 5, 5),
    "matrix_green": (0, 255, 65),
    "matrix_dark_green": (0, 128, 32),
    "matrix_bright": (100, 255, 100),
    
    # Cyberpunk 2077 Style
    "cyber_yellow": (255, 215, 0),
    "cyber_magenta": (255, 0, 144),
    "cyber_cyan": (0, 255, 255),
    "cyber_purple": (147, 0, 211),
    
    # Developer Dark
    "dev_bg": (28, 28, 30),
    "dev_comment": (108, 121, 134),
    "dev_keyword": (147, 199, 99),
    "dev_string": (236, 196, 141),
    "dev_function": (103, 183, 164),
    
    # Professional Dashboard
    "dash_header": (41, 54, 63),
    "dash_success": (39, 174, 96),
    "dash_warning": (243, 156, 18),
    "dash_danger": (231, 76, 60),
    "dash_info": (52, 152, 219),
}

def rgb_to_ansi_bg(color):
    """Convert RGB to ANSI background"""
    if isinstance(color, str) and color in ULTIMATE_COLORS:
        r, g, b = ULTIMATE_COLORS[color]
    elif isinstance(color, tuple):
        r, g, b = color
    else:
        return ""
    return f"\033[48;2;{r};{g};{b}m"

def rgb_to_ansi_fg(color):
    """Convert RGB to ANSI foreground"""
    if isinstance(color, str) and color in ULTIMATE_COLORS:
        r, g, b = ULTIMATE_COLORS[color]
    elif isinstance(color, tuple):
        r, g, b = color
    else:
        return ""
    return f"\033[38;2;{r};{g};{b}m"

# ULTIMATE EPIC THEMES - Each one is unique and data-rich!
ULTIMATE_EPIC_THEMES = {
    
    # ═══════════════════════════════════════════════════════════════
    # ULTRA COMPREHENSIVE THEMES - Using ALL available fields
    # ═══════════════════════════════════════════════════════════════
    
    "ultimate_dashboard_pro": {
        "name": "Ultimate Dashboard Pro",
        "description": "Complete metrics dashboard with everything",
        "category": "Ultimate",
        "multiline": True,
        "template": """┏━━━━━━━━━━━━━━━━ CLAUDE AI ULTIMATE DASHBOARD ━━━━━━━━━━━━━━━━┓
┃ 🤖 {model} v{model_version} │ 📁 {folder} │ 🌿 {git_branch} │ 🔗 {session_id}
┃ ⚡ CPU: {cpu}% │ 💾 RAM: {ram}% │ 🌐 {network} │ 📡 {latency}
┃ 💬 Messages: {messages} │ 📥 In: {input_tokens} │ 📤 Out: {output_tokens}
┃ 💸 Total: ${cost} │ 💵 Per msg: ${cost_per_msg} │ 📊 ROI: {efficiency}%
┃ ⏱️ Session: {session_time} │ ⏳ Remaining: {time_left} │ 🔄 {uptime}
┃ 🎯 Quality: {quality_score} │ 🚀 {productivity} │ 📈 {performance}
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""
    },
    
    "matrix_rain_complete": {
        "name": "Matrix Rain Complete",
        "description": "Full Matrix digital rain with all metrics",
        "category": "Matrix",
        "segments": [
            {"content": "▓▓▓ {model_short}", "bg": "matrix_black", "fg": "matrix_green"},
            {"content": "📁 {folder}", "bg": "matrix_dark_green", "fg": "matrix_bright"},
            {"content": "⎇ {git_branch}", "bg": "matrix_black", "fg": "matrix_green"},
            {"content": "◈ S:{session_id}", "bg": "matrix_dark_green", "fg": "matrix_bright"},
            {"content": "⚡ {cpu}%|{ram}%", "bg": "matrix_black", "fg": "matrix_green"},
            {"content": "💬 {messages}m", "bg": "matrix_dark_green", "fg": "matrix_bright"},
            {"content": "I/O {input_tokens}/{output_tokens}", "bg": "matrix_black", "fg": "matrix_green"},
            {"content": "⧉ Cache {cache_hits}", "bg": "matrix_dark_green", "fg": "matrix_bright"},
            {"content": "💰 ${cost}", "bg": "matrix_black", "fg": "matrix_green"},
            {"content": "⏱ {uptime}", "bg": "matrix_dark_green", "fg": "matrix_bright"},
        ]
    },
    
    "developer_complete_metrics": {
        "name": "Developer Complete Metrics",
        "description": "Every metric a developer needs",
        "category": "Developer",
        "segments": [
            {"content": "⚙ {model}:{model_version}", "bg": "dev_bg", "fg": "dev_keyword"},
            {"content": "📂 {folder}@{git_branch}", "bg": "dev_comment", "fg": "white"},
            {"content": "🔧 {messages}msg", "bg": "dev_function", "fg": "black"},
            {"content": "📊 I:{input_tokens}/O:{output_tokens}", "bg": "dev_string", "fg": "black"},
            {"content": "💾 C:{cache_hits}/{cache_efficiency}", "bg": "dev_keyword", "fg": "black"},
            {"content": "⚡ {cpu}%/{ram}%", "bg": "dev_comment", "fg": "white"},
            {"content": "💸 ${cost}@${cost_per_msg}/m", "bg": "dev_function", "fg": "black"},
            {"content": "⏰ {session_time}→{time_left}", "bg": "dev_string", "fg": "black"},
            {"content": "📈 Q:{quality_score}/E:{efficiency}", "bg": "dev_bg", "fg": "dev_keyword"},
        ]
    },
    
    "cyberpunk_2077_full": {
        "name": "Cyberpunk 2077 Full HUD",
        "description": "Night City complete interface",
        "category": "Cyberpunk",
        "multiline": True,
        "template": """╔═══ ◆ NETRUNNER INTERFACE ◆ ═══╗
║ 🧠 {model} v{model_version} ◆ REP: {session_quality}
║ 📍 {folder} ◆ SUBNET: {git_branch}
║ ⚡ CYBERWARE: CPU {cpu}% | RAM {ram}% | NET {network}
║ 💾 QUICKHACKS: {messages} | BREACH: {input_tokens}+{output_tokens}
║ 💰 EDDIES: ${cost} | RATE: ${cost_per_msg}/hack
║ ⏱ RUNTIME: {uptime} | COOLDOWN: {time_left}
╚════════════════════════════════╝"""
    },
    
    "professional_executive_full": {
        "name": "Professional Executive Full",
        "description": "C-Suite comprehensive dashboard",
        "category": "Executive",
        "segments": [
            {"content": "🏢 {model_tier}", "bg": "dash_header", "fg": "white"},
            {"content": "📊 {folder}", "bg": "dash_info", "fg": "white"},
            {"content": "🔀 {git_branch}", "bg": "dash_header", "fg": "white"},
            {"content": "📈 KPI {messages}", "bg": "dash_success", "fg": "white"},
            {"content": "💹 I/O {input_tokens}/{output_tokens}", "bg": "dash_info", "fg": "white"},
            {"content": "⚡ {cpu}%|{ram}%", "bg": "dash_warning", "fg": "black"},
            {"content": "💵 ${cost}", "bg": "dash_success", "fg": "white"},
            {"content": "📊 ROI {efficiency}%", "bg": "dash_danger", "fg": "white"},
            {"content": "⏰ {uptime}", "bg": "dash_header", "fg": "white"},
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # GAMING THEMED - Rich gaming interfaces
    # ═══════════════════════════════════════════════════════════════
    
    "fps_competitive_hud": {
        "name": "FPS Competitive HUD",
        "description": "CS:GO/Valorant style complete HUD",
        "category": "Gaming",
        "multiline": True,
        "template": """┌─ MATCH STATS ─────────────────────────┐
│ 🎮 {model} │ MAP: {folder} │ SITE: {git_branch}
│ K/D: {messages}/{tokens_formatted} │ HS%: {efficiency}
│ 💰 ${cost} │ ADR: {cost_per_msg} │ UTIL: {cache_hits}
│ HP: {cpu}% │ ARMOR: {ram}% │ PING: {latency}
│ ROUND: {session_time} │ TIME: {time_left}
└───────────────────────────────────────┘"""
    },
    
    "mmorpg_raid_interface": {
        "name": "MMORPG Raid Interface",
        "description": "WoW/FF14 raid UI with all stats",
        "category": "Gaming",
        "segments": [
            {"content": "⚔ {model_short} Lv{model_version}", "bg": (64, 0, 128), "fg": "white"},
            {"content": "🏰 {folder}", "bg": (128, 0, 64), "fg": "white"},
            {"content": "🗺 {git_branch}", "bg": (64, 0, 128), "fg": "white"},
            {"content": "💀 {messages} kills", "bg": (128, 0, 0), "fg": "white"},
            {"content": "⚡ MP:{tokens_formatted}", "bg": (0, 0, 128), "fg": "white"},
            {"content": "💚 HP:{cpu}%", "bg": (0, 128, 0), "fg": "white"},
            {"content": "🛡 DEF:{ram}%", "bg": (128, 128, 0), "fg": "black"},
            {"content": "💰 {cost}g", "bg": (255, 215, 0), "fg": "black"},
            {"content": "⏱ {uptime}", "bg": (64, 0, 128), "fg": "white"},
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # SPACE & SCI-FI - Futuristic interfaces
    # ═══════════════════════════════════════════════════════════════
    
    "starship_bridge_complete": {
        "name": "Starship Bridge Complete",
        "description": "Star Trek LCARS full interface",
        "category": "Space",
        "multiline": True,
        "template": """╔══════════ ◗ LCARS INTERFACE ◖ ══════════╗
║ SHIP: {model} {model_version} ◆ SECTOR: {folder}
║ HEADING: {git_branch} ◆ STARDATE: {session_id}
║ ⚡ WARP: {cpu}% ◆ SHIELDS: {ram}% ◆ COMMS: {network}
║ 📡 HAILS: {messages} ◆ SUBSPACE: {tokens_formatted}
║ 💎 DILITHIUM: ${cost} ◆ EFFICIENCY: {efficiency}%
║ ⏱ MISSION: {uptime} ◆ ETA: {time_left}
╚══════════════════════════════════════════╝"""
    },
    
    "nasa_mission_control": {
        "name": "NASA Mission Control",
        "description": "Houston control center interface",
        "category": "Space",
        "segments": [
            {"content": "🚀 {model}", "bg": (10, 25, 47), "fg": "white"},
            {"content": "ISS-{folder}", "bg": (139, 0, 0), "fg": "white"},
            {"content": "ORBIT:{git_branch}", "bg": (10, 25, 47), "fg": "white"},
            {"content": "COMMS:{messages}", "bg": (255, 140, 0), "fg": "black"},
            {"content": "TELEMETRY:{tokens_formatted}", "bg": (10, 25, 47), "fg": "white"},
            {"content": "O2:{cpu}%", "bg": (0, 128, 0), "fg": "white"},
            {"content": "POWER:{ram}%", "bg": (255, 140, 0), "fg": "black"},
            {"content": "BUDGET:${cost}", "bg": (139, 0, 0), "fg": "white"},
            {"content": "T+{uptime}", "bg": (10, 25, 47), "fg": "white"},
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # HACKER & SECURITY - Elite hacking interfaces
    # ═══════════════════════════════════════════════════════════════
    
    "elite_hacker_terminal": {
        "name": "Elite Hacker Terminal",
        "description": "Mr. Robot style complete terminal",
        "category": "Hacker",
        "multiline": True,
        "template": """root@fsociety:~# session --status
┌─[👤 {model}@{model_version}]─[📁 {folder}]─[🔀 {git_branch}]
├─[💻 CPU:{cpu}%]─[💾 RAM:{ram}%]─[🌐 {network}:{latency}]
├─[📊 PACKETS:{messages}]─[📡 TX:{input_tokens}]─[📡 RX:{output_tokens}]
├─[🔓 EXPLOITS:{cache_hits}]─[🛡️ FIREWALL:{cache_efficiency}%]
├─[💰 BTC:${cost}]─[⚡ HASHRATE:${cost_per_msg}/s]
└─[⏱️ UPTIME:{uptime}]─[🔄 SESSION:{session_time}]─[⏳ TTL:{time_left}]"""
    },
    
    "security_operations_center": {
        "name": "Security Operations Center",
        "description": "SOC monitoring dashboard",
        "category": "Security",
        "segments": [
            {"content": "🛡 {model} SOC", "bg": (25, 25, 25), "fg": (0, 255, 0)},
            {"content": "📍 {folder}", "bg": (50, 0, 0), "fg": "white"},
            {"content": "🔍 {git_branch}", "bg": (25, 25, 25), "fg": (0, 255, 0)},
            {"content": "🚨 {messages} events", "bg": (128, 0, 0), "fg": "white"},
            {"content": "📊 {tokens_formatted} logs", "bg": (25, 25, 25), "fg": (0, 255, 0)},
            {"content": "CPU:{cpu}%", "bg": (50, 50, 0), "fg": "white"},
            {"content": "MEM:{ram}%", "bg": (0, 50, 50), "fg": "white"},
            {"content": "COST:${cost}", "bg": (50, 0, 0), "fg": "white"},
            {"content": "{uptime} active", "bg": (25, 25, 25), "fg": (0, 255, 0)},
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # FINANCIAL & TRADING - Market interfaces
    # ═══════════════════════════════════════════════════════════════
    
    "bloomberg_terminal": {
        "name": "Bloomberg Terminal",
        "description": "Professional trading terminal",
        "category": "Finance",
        "multiline": True,
        "template": """╔═ BLOOMBERG PROFESSIONAL ═════════════════╗
║ {model} {model_version} │ DESK: {folder} │ BOOK: {git_branch}
║ TRADES: {messages} │ VOL: {tokens_formatted} │ PNL: ${cost}
║ BID: {input_tokens} │ ASK: {output_tokens} │ SPREAD: {cache_hits}
║ CPU: {cpu}% │ RAM: {ram}% │ LAT: {latency}
║ SESSION: {session_time} │ CLOSE: {time_left}
║ SHARPE: {efficiency} │ ALPHA: {quality_score}
╚══════════════════════════════════════════╝"""
    },
    
    "crypto_trading_desk": {
        "name": "Crypto Trading Desk",
        "description": "Binance/FTX style trading interface",
        "category": "Finance",
        "segments": [
            {"content": "₿ {model}", "bg": (242, 169, 0), "fg": "black"},
            {"content": "📈 {folder}", "bg": (14, 203, 129), "fg": "black"},
            {"content": "🔄 {git_branch}", "bg": (246, 70, 93), "fg": "white"},
            {"content": "TRADES:{messages}", "bg": (36, 41, 49), "fg": "white"},
            {"content": "VOL:{tokens_formatted}", "bg": (14, 203, 129), "fg": "black"},
            {"content": "L/S:{input_tokens}/{output_tokens}", "bg": (246, 70, 93), "fg": "white"},
            {"content": "💰${cost}", "bg": (242, 169, 0), "fg": "black"},
            {"content": "APY:{efficiency}%", "bg": (14, 203, 129), "fg": "black"},
            {"content": "⏱{uptime}", "bg": (36, 41, 49), "fg": "white"},
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # MUSIC & CREATIVE - Artistic interfaces
    # ═══════════════════════════════════════════════════════════════
    
    "dj_mixer_console": {
        "name": "DJ Mixer Console",
        "description": "Professional DJ mixing interface",
        "category": "Music",
        "multiline": True,
        "template": """╔═══ 🎧 DJ CONSOLE ═══════════════════════╗
║ DECK A: {model} │ DECK B: {model_version}
║ 🎵 TRACK: {folder} │ MIX: {git_branch}
║ BPM: {messages} │ BEATS: {tokens_formatted}
║ 🎚️ LOW: {cpu}% │ MID: {ram}% │ HIGH: {efficiency}%
║ 💿 SAMPLES: {input_tokens} │ LOOPS: {output_tokens}
║ 💰 BOOKING: ${cost} │ RATE: ${cost_per_msg}/hr
║ ⏱️ SET: {uptime} │ REMAINING: {time_left}
╚═════════════════════════════════════════╝"""
    },
    
    "video_editor_timeline": {
        "name": "Video Editor Timeline",
        "description": "Premiere Pro style timeline",
        "category": "Creative",
        "segments": [
            {"content": "🎬 {model}", "bg": (128, 0, 128), "fg": "white"},
            {"content": "📹 {folder}", "bg": (64, 64, 64), "fg": "white"},
            {"content": "🎞️ {git_branch}", "bg": (128, 0, 0), "fg": "white"},
            {"content": "CLIPS:{messages}", "bg": (0, 128, 0), "fg": "white"},
            {"content": "FRAMES:{tokens_formatted}", "bg": (64, 64, 64), "fg": "white"},
            {"content": "IN:{input_tokens}", "bg": (128, 128, 0), "fg": "black"},
            {"content": "OUT:{output_tokens}", "bg": (0, 128, 128), "fg": "white"},
            {"content": "RENDER:{cpu}%", "bg": (128, 0, 128), "fg": "white"},
            {"content": "${cost}", "bg": (255, 215, 0), "fg": "black"},
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # AUTOMOTIVE & RACING - Vehicle interfaces
    # ═══════════════════════════════════════════════════════════════
    
    "f1_racing_telemetry": {
        "name": "F1 Racing Telemetry",
        "description": "Formula 1 race engineer display",
        "category": "Racing",
        "multiline": True,
        "template": """╔═══ 🏎️ F1 TELEMETRY ═════════════════════╗
║ DRIVER: {model} │ CAR: {model_version} │ TRACK: {folder}
║ SECTOR: {git_branch} │ LAP: {messages} │ POS: P{efficiency}
║ ⚡ SPEED: {tokens_formatted}km/h │ RPM: {cpu}00
║ 🛞 TYRES: {ram}% │ FUEL: {cache_hits}L │ ERS: {cache_efficiency}%
║ 💰 PRIZE: ${cost}M │ POINTS: {quality_score}
║ ⏱️ LAPTIME: {session_time} │ DELTA: {time_left}
╚══════════════════════════════════════════╝"""
    },
    
    "tesla_autopilot_hud": {
        "name": "Tesla Autopilot HUD",
        "description": "Model S Plaid interface",
        "category": "Automotive",
        "segments": [
            {"content": "🚗 {model}", "bg": (204, 0, 0), "fg": "white"},
            {"content": "📍 {folder}", "bg": (64, 64, 64), "fg": "white"},
            {"content": "🛣️ {git_branch}", "bg": (204, 0, 0), "fg": "white"},
            {"content": "⚡ {tokens_formatted}kW", "bg": (0, 128, 0), "fg": "white"},
            {"content": "🔋 {cpu}%", "bg": (64, 64, 64), "fg": "white"},
            {"content": "AP:{ram}%", "bg": (0, 128, 255), "fg": "white"},
            {"content": "MILES:{messages}", "bg": (204, 0, 0), "fg": "white"},
            {"content": "${cost}/kWh", "bg": (0, 128, 0), "fg": "white"},
            {"content": "⏱{uptime}", "bg": (64, 64, 64), "fg": "white"},
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # MEDICAL & SCIENCE - Scientific interfaces
    # ═══════════════════════════════════════════════════════════════
    
    "medical_monitoring_station": {
        "name": "Medical Monitoring Station",
        "description": "ICU patient monitoring system",
        "category": "Medical",
        "multiline": True,
        "template": """╔═══ 🏥 PATIENT MONITOR ═══════════════════╗
║ ID: {model} {model_version} │ WARD: {folder} │ BED: {git_branch}
║ ❤️ HR: {messages} bpm │ 🫁 O2: {cpu}% │ 🩸 BP: {ram}/{efficiency}
║ 📊 SAMPLES: {tokens_formatted} │ TESTS: {input_tokens}
║ 💊 MEDS: {cache_hits} │ DOSE: {cache_efficiency}mg
║ 💰 BILLING: ${cost} │ INSURANCE: ${cost_per_msg}
║ ⏱️ ADMITTED: {uptime} │ DISCHARGE: {time_left}
╚══════════════════════════════════════════╝"""
    },
    
    "lab_experiment_console": {
        "name": "Lab Experiment Console",
        "description": "CERN particle physics interface",
        "category": "Science",
        "segments": [
            {"content": "⚛️ {model}", "bg": (0, 0, 64), "fg": "white"},
            {"content": "🔬 {folder}", "bg": (64, 0, 64), "fg": "white"},
            {"content": "🧪 {git_branch}", "bg": (0, 64, 64), "fg": "white"},
            {"content": "COLLISIONS:{messages}", "bg": (128, 0, 0), "fg": "white"},
            {"content": "PARTICLES:{tokens_formatted}", "bg": (0, 0, 64), "fg": "white"},
            {"content": "ENERGY:{cpu}TeV", "bg": (255, 140, 0), "fg": "black"},
            {"content": "TEMP:{ram}K", "bg": (0, 128, 255), "fg": "white"},
            {"content": "GRANT:${cost}", "bg": (0, 128, 0), "fg": "white"},
            {"content": "⏱{uptime}", "bg": (64, 0, 64), "fg": "white"},
        ]
    },
}

def get_ultimate_themes() -> Dict:
    """Get all ultimate epic themes"""
    return ULTIMATE_EPIC_THEMES

def get_theme_count() -> int:
    """Get total theme count"""
    return len(ULTIMATE_EPIC_THEMES)

# Export for use
__all__ = ['ULTIMATE_EPIC_THEMES', 'get_ultimate_themes', 'rgb_to_ansi_bg', 'rgb_to_ansi_fg']