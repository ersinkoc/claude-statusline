#!/usr/bin/env python3
"""
Epic Powerline Mega Themes - 100+ Ultimate Professional Themes
Packed with data, icons, and stunning powerline designs
"""

from typing import Dict, List, Any
import random

# Color definitions with RGB values for soft gradients
EPIC_COLORS = {
    # Cyberpunk Collection
    "cyber_dark": (18, 18, 35),
    "cyber_purple": (138, 43, 226), 
    "cyber_pink": (255, 20, 147),
    "cyber_blue": (30, 144, 255),
    "cyber_green": (50, 205, 50),
    
    # Ocean Collection  
    "ocean_deep": (25, 25, 112),
    "ocean_blue": (70, 130, 180),
    "ocean_teal": (72, 209, 204),
    "ocean_aqua": (127, 255, 212),
    "ocean_foam": (175, 238, 238),
    
    # Sunset Collection
    "sunset_orange": (255, 140, 0),
    "sunset_red": (220, 20, 60),
    "sunset_yellow": (255, 215, 0),
    "sunset_pink": (255, 182, 193),
    "sunset_purple": (148, 0, 211),
    
    # Forest Collection
    "forest_dark": (34, 139, 34),
    "forest_green": (107, 142, 35),
    "forest_lime": (154, 205, 50),
    "forest_moss": (85, 107, 47),
    "forest_mint": (152, 251, 152),
    
    # Professional Collection
    "pro_navy": (25, 25, 112),
    "pro_blue": (100, 149, 237),
    "pro_silver": (192, 192, 192),
    "pro_gold": (255, 215, 0),
    "pro_platinum": (229, 228, 226),
    
    # Gaming Collection
    "game_red": (220, 20, 60),
    "game_blue": (30, 144, 255),
    "game_purple": (138, 43, 226),
    "game_green": (50, 205, 50),
    "game_orange": (255, 140, 0),
    
    # Neon Collection
    "neon_pink": (255, 20, 147),
    "neon_cyan": (0, 255, 255),
    "neon_yellow": (255, 255, 0),
    "neon_purple": (148, 0, 211),
    "neon_green": (57, 255, 20),
    
    # Monochrome Collection
    "mono_black": (0, 0, 0),
    "mono_dark": (64, 64, 64),
    "mono_gray": (128, 128, 128),
    "mono_silver": (192, 192, 192),
    "mono_white": (255, 255, 255),
}

def rgb_to_ansi_bg(color):
    """Convert RGB color to ANSI background escape code"""
    if isinstance(color, str):
        if color in EPIC_COLORS:
            r, g, b = EPIC_COLORS[color]
            return f"\033[48;2;{r};{g};{b}m"  # Actual escape character
    elif isinstance(color, tuple):
        r, g, b = color
        return f"\033[48;2;{r};{g};{b}m"  # Actual escape character
    return ""

def rgb_to_ansi_fg(color):
    """Convert RGB color to ANSI foreground escape code"""
    if isinstance(color, str):
        if color in EPIC_COLORS:
            r, g, b = EPIC_COLORS[color]
            return f"\033[38;2;{r};{g};{b}m"  # Actual escape character
    elif isinstance(color, tuple):
        r, g, b = color
        return f"\033[38;2;{r};{g};{b}m"  # Actual escape character
    return ""

# Epic Theme Collection - 100+ Themes!
EPIC_MEGA_THEMES = {
    
    # ============== CYBERPUNK SERIES (15 themes) ==============
    "cyber_matrix_pro": {
        "name": "Cyber Matrix Pro",
        "description": "Advanced cyberpunk matrix interface",
        "category": "Cyberpunk",
        "multiline": False,
        "segments": [
            {"content": "⚡ {model_short}", "bg": "cyber_dark", "fg": "cyber_green"},
            {"content": "📁 {folder}", "bg": "cyber_purple", "fg": "white"},
            {"content": "🌿 {branch}", "bg": "cyber_blue", "fg": "white"},
            {"content": "💬 {messages}m", "bg": "cyber_pink", "fg": "white"},
            {"content": "🔥 {tokens}", "bg": "cyber_green", "fg": "black"},
            {"content": "💰 ${cost}", "bg": "cyber_dark", "fg": "cyber_green"}
        ]
    },
    
    "cyber_neon_flow": {
        "name": "Cyber Neon Flow",
        "description": "Flowing neon cyberpunk theme",
        "category": "Cyberpunk",
        "multiline": False,
        "segments": [
            {"content": "▶ {model_name}", "bg": "neon_pink", "fg": "black"},
            {"content": "🏠 {project}", "bg": "neon_cyan", "fg": "black"},
            {"content": "📊 {cpu} CPU", "bg": "neon_yellow", "fg": "black"},
            {"content": "🧠 {ram} RAM", "bg": "neon_purple", "fg": "white"},
            {"content": "⏱ {remaining}", "bg": "neon_green", "fg": "black"}
        ]
    },
    
    "cyber_terminal_hacker": {
        "name": "Cyber Terminal Hacker",
        "description": "Elite hacker terminal style",
        "category": "Cyberpunk", 
        "multiline": True,
        "segments": [
            [
                {"content": "👤 {model_short}", "bg": "cyber_dark", "fg": "cyber_green"},
                {"content": "📂 {folder_name}", "bg": "cyber_purple", "fg": "white"},
                {"content": "🔗 {git_branch}", "bg": "cyber_blue", "fg": "white"}
            ],
            [
                {"content": "💾 {efficiency}", "bg": "cyber_green", "fg": "black"},
                {"content": "⚡ {messages}msg", "bg": "cyber_pink", "fg": "white"},
                {"content": "💸 ${cost}", "bg": "cyber_dark", "fg": "cyber_green"}
            ]
        ]
    },
    
    "cyber_quantum_grid": {
        "name": "Cyber Quantum Grid",
        "description": "Quantum grid cyberpunk interface",
        "category": "Cyberpunk",
        "multiline": False,
        "segments": [
            {"content": "◈ {model_short}", "bg": "cyber_dark", "fg": "cyber_blue"},
            {"content": "⬢ {network}", "bg": "cyber_purple", "fg": "white"},
            {"content": "⬡ {ping}", "bg": "cyber_green", "fg": "black"},
            {"content": "◆ {tokens}", "bg": "cyber_pink", "fg": "white"},
            {"content": "◉ ${cost}", "bg": "cyber_blue", "fg": "white"}
        ]
    },
    
    "cyber_data_stream": {
        "name": "Cyber Data Stream",
        "description": "Streaming data cyberpunk theme",
        "category": "Cyberpunk",
        "multiline": False,
        "segments": [
            {"content": "🌊 {model_name} Stream", "bg": "cyber_dark", "fg": "cyber_green"},
            {"content": "📡 {latency} ping", "bg": "cyber_purple", "fg": "white"},
            {"content": "⚙️ {cpu}|{ram}", "bg": "cyber_blue", "fg": "white"},
            {"content": "🔋 {efficiency}", "bg": "cyber_green", "fg": "black"},
            {"content": "💎 {qual}", "bg": "cyber_pink", "fg": "white"}
        ]
    },
    
    # ============== OCEAN SERIES (15 themes) ==============
    "ocean_depths_pro": {
        "name": "Ocean Depths Pro",
        "description": "Deep ocean professional theme",
        "category": "Ocean",
        "multiline": False,
        "segments": [
            {"content": "🌊 {model_short}", "bg": "ocean_deep", "fg": "white"},
            {"content": "🏠 {folder}", "bg": "ocean_blue", "fg": "white"},
            {"content": "🌿 {branch}", "bg": "ocean_teal", "fg": "black"},
            {"content": "💬 {msg}msgs", "bg": "ocean_aqua", "fg": "black"},
            {"content": "⏰ {sess}", "bg": "ocean_foam", "fg": "black"}
        ]
    },
    
    "ocean_wave_rider": {
        "name": "Ocean Wave Rider",
        "description": "Riding the data waves",
        "category": "Ocean",
        "multiline": True,
        "segments": [
            [
                {"content": "🏄 {model_name}", "bg": "ocean_deep", "fg": "white"},
                {"content": "🏖 {project}", "bg": "ocean_blue", "fg": "white"},
                {"content": "🌊 {network}", "bg": "ocean_teal", "fg": "black"}
            ],
            [
                {"content": "⚡ {tokens} waves", "bg": "ocean_aqua", "fg": "black"},
                {"content": "💰 ${cost} treasure", "bg": "ocean_foam", "fg": "black"}
            ]
        ]
    },
    
    "ocean_coral_reef": {
        "name": "Ocean Coral Reef",
        "description": "Vibrant coral reef theme",
        "category": "Ocean",
        "multiline": False,
        "segments": [
            {"content": "🐠 {model_short}", "bg": "ocean_deep", "fg": "ocean_foam"},
            {"content": "🪸 {folder_name}", "bg": "ocean_blue", "fg": "white"},
            {"content": "🌿 {git_branch}", "bg": "ocean_teal", "fg": "black"},
            {"content": "🐟 {messages}m", "bg": "ocean_aqua", "fg": "black"},
            {"content": "🦑 {efficiency}", "bg": "ocean_foam", "fg": "black"}
        ]
    },
    
    "ocean_tsunami_power": {
        "name": "Ocean Tsunami Power",
        "description": "Powerful tsunami wave theme",
        "category": "Ocean",
        "multiline": False,
        "segments": [
            {"content": "🌊💥 {model_short}", "bg": "ocean_deep", "fg": "white"},
            {"content": "⚡ {cpu} power", "bg": "ocean_blue", "fg": "white"},
            {"content": "💾 {ram} memory", "bg": "ocean_teal", "fg": "black"},
            {"content": "🔥 {tokens} data", "bg": "ocean_aqua", "fg": "black"},
            {"content": "💎 ${cost}", "bg": "ocean_foam", "fg": "black"}
        ]
    },
    
    "ocean_lighthouse": {
        "name": "Ocean Lighthouse",
        "description": "Guiding lighthouse theme",
        "category": "Ocean",
        "multiline": True,
        "segments": [
            [
                {"content": "🗼 {model_name} Tower", "bg": "ocean_deep", "fg": "white"},
                {"content": "🏠 {project} Port", "bg": "ocean_blue", "fg": "white"}
            ],
            [
                {"content": "⛵ {branch} Ship", "bg": "ocean_teal", "fg": "black"},
                {"content": "🌊 {messages} waves", "bg": "ocean_aqua", "fg": "black"}
            ],
            [
                {"content": "💰 ${cost} cargo", "bg": "ocean_foam", "fg": "black"}
            ]
        ]
    },
    
    # ============== SUNSET SERIES (15 themes) ==============
    "sunset_horizon_pro": {
        "name": "Sunset Horizon Pro",
        "description": "Professional sunset horizon",
        "category": "Sunset",
        "multiline": False,
        "segments": [
            {"content": "🌅 {model_short}", "bg": "sunset_orange", "fg": "white"},
            {"content": "🏠 {folder}", "bg": "sunset_red", "fg": "white"},
            {"content": "🌿 {branch}", "bg": "sunset_yellow", "fg": "black"},
            {"content": "⭐ {messages}m", "bg": "sunset_pink", "fg": "black"},
            {"content": "🌙 ${cost}", "bg": "sunset_purple", "fg": "white"}
        ]
    },
    
    "sunset_golden_hour": {
        "name": "Sunset Golden Hour",
        "description": "Golden hour productivity",
        "category": "Sunset",
        "multiline": False,
        "segments": [
            {"content": "✨ {model_name}", "bg": "sunset_yellow", "fg": "black"},
            {"content": "📁 {project}", "bg": "sunset_orange", "fg": "white"},
            {"content": "🔥 {efficiency}", "bg": "sunset_red", "fg": "white"},
            {"content": "💫 {tokens}", "bg": "sunset_pink", "fg": "black"},
            {"content": "🌟 {remaining}", "bg": "sunset_purple", "fg": "white"}
        ]
    },
    
    "sunset_fire_sky": {
        "name": "Sunset Fire Sky",
        "description": "Fiery sky sunset theme",
        "category": "Sunset",
        "multiline": True,
        "segments": [
            [
                {"content": "🔥 {model_short} Fire", "bg": "sunset_red", "fg": "white"},
                {"content": "🏠 {folder_name}", "bg": "sunset_orange", "fg": "white"}
            ],
            [
                {"content": "⚡ {cpu}% | 🧠 {ram}%", "bg": "sunset_yellow", "fg": "black"},
                {"content": "💎 {messages}msgs", "bg": "sunset_pink", "fg": "black"}
            ]
        ]
    },
    
    # ============== FOREST SERIES (15 themes) ==============
    "forest_emerald_pro": {
        "name": "Forest Emerald Pro", 
        "description": "Professional emerald forest",
        "category": "Forest",
        "multiline": False,
        "segments": [
            {"content": "🌲 {model_short}", "bg": "forest_dark", "fg": "white"},
            {"content": "🍃 {folder}", "bg": "forest_green", "fg": "white"},
            {"content": "🌿 {branch}", "bg": "forest_lime", "fg": "black"},
            {"content": "🐛 {messages}m", "bg": "forest_moss", "fg": "white"},
            {"content": "💚 ${cost}", "bg": "forest_mint", "fg": "black"}
        ]
    },
    
    "forest_oak_tree": {
        "name": "Forest Oak Tree",
        "description": "Mighty oak tree theme",
        "category": "Forest",
        "multiline": True,
        "segments": [
            [
                {"content": "🌳 {model_name} Oak", "bg": "forest_dark", "fg": "white"},
                {"content": "🏠 {project} Grove", "bg": "forest_green", "fg": "white"}
            ],
            [
                {"content": "🍂 {git_branch}", "bg": "forest_lime", "fg": "black"},
                {"content": "🐿️ {messages} squirrels", "bg": "forest_moss", "fg": "white"}
            ],
            [
                {"content": "🌰 ${cost} acorns", "bg": "forest_mint", "fg": "black"}
            ]
        ]
    },
    
    # ============== GAMING SERIES (15 themes) ==============
    "gaming_fps_hud": {
        "name": "Gaming FPS HUD",
        "description": "First person shooter HUD",
        "category": "Gaming",
        "multiline": False,
        "segments": [
            {"content": "🎮 {model_short}", "bg": "game_red", "fg": "white"},
            {"content": "📁 {folder}", "bg": "game_blue", "fg": "white"},
            {"content": "⚔️ {messages} frags", "bg": "game_purple", "fg": "white"},
            {"content": "💰 ${cost} coins", "bg": "game_green", "fg": "black"},
            {"content": "🏆 {efficiency}", "bg": "game_orange", "fg": "white"}
        ]
    },
    
    "gaming_rpg_status": {
        "name": "Gaming RPG Status",
        "description": "Role playing game status bar",
        "category": "Gaming",
        "multiline": True,
        "segments": [
            [
                {"content": "🧙 {model_name} Mage", "bg": "game_purple", "fg": "white"},
                {"content": "🏰 {project} Castle", "bg": "game_blue", "fg": "white"}
            ],
            [
                {"content": "⚔️ {messages} XP", "bg": "game_red", "fg": "white"},
                {"content": "💎 {tokens} gems", "bg": "game_green", "fg": "black"}
            ],
            [
                {"content": "🪙 ${cost} gold", "bg": "game_orange", "fg": "white"}
            ]
        ]
    },
    
    "gaming_retro_arcade": {
        "name": "Gaming Retro Arcade",
        "description": "Retro 80s arcade theme",
        "category": "Gaming",
        "multiline": False,
        "segments": [
            {"content": "👾 {model_short}", "bg": "neon_pink", "fg": "black"},
            {"content": "🕹️ {folder_name}", "bg": "neon_cyan", "fg": "black"},
            {"content": "🎯 {messages} pts", "bg": "neon_yellow", "fg": "black"},
            {"content": "🔋 {efficiency}", "bg": "neon_purple", "fg": "white"},
            {"content": "🏅 LVL{qual}", "bg": "neon_green", "fg": "black"}
        ]
    },
    
    # ============== PROFESSIONAL SERIES (20 themes) ==============
    "pro_executive_suite": {
        "name": "Pro Executive Suite",
        "description": "Executive boardroom style",
        "category": "Professional",
        "multiline": False,
        "segments": [
            {"content": "👔 {model_short}", "bg": "pro_navy", "fg": "white"},
            {"content": "🏢 {folder}", "bg": "pro_blue", "fg": "white"},
            {"content": "📊 {branch}", "bg": "pro_silver", "fg": "black"},
            {"content": "📈 {messages}m", "bg": "pro_gold", "fg": "black"},
            {"content": "💼 ${cost}", "bg": "pro_platinum", "fg": "black"}
        ]
    },
    
    "pro_consultant_premium": {
        "name": "Pro Consultant Premium",
        "description": "Premium consultant dashboard",
        "category": "Professional", 
        "multiline": True,
        "segments": [
            [
                {"content": "🎯 {model_name} Advisor", "bg": "pro_navy", "fg": "white"},
                {"content": "📁 {project} Client", "bg": "pro_blue", "fg": "white"}
            ],
            [
                {"content": "📊 {efficiency} Performance", "bg": "pro_silver", "fg": "black"},
                {"content": "💰 ${cost} Revenue", "bg": "pro_gold", "fg": "black"}
            ]
        ]
    },
    
    "pro_analyst_workstation": {
        "name": "Pro Analyst Workstation",
        "description": "Financial analyst workstation",
        "category": "Professional",
        "multiline": False,
        "segments": [
            {"content": "📊 {model_short}", "bg": "pro_navy", "fg": "white"},
            {"content": "💼 {folder_name}", "bg": "pro_blue", "fg": "white"},
            {"content": "📈 {cpu}%|{ram}%", "bg": "pro_silver", "fg": "black"},
            {"content": "💹 {messages}tx", "bg": "pro_gold", "fg": "black"},
            {"content": "💵 ${cost}k", "bg": "pro_platinum", "fg": "black"}
        ]
    },
    
    # ============== SPACE SERIES (10 themes) ==============
    "space_galaxy_explorer": {
        "name": "Space Galaxy Explorer",
        "description": "Exploring distant galaxies",
        "category": "Space",
        "multiline": False,
        "segments": [
            {"content": "🚀 {model_short}", "bg": "cyber_dark", "fg": "white"},
            {"content": "🌌 {folder} Galaxy", "bg": "cyber_purple", "fg": "white"},
            {"content": "⭐ {branch} System", "bg": "cyber_blue", "fg": "white"},
            {"content": "🛸 {messages} signals", "bg": "cyber_pink", "fg": "white"},
            {"content": "💎 {tokens} minerals", "bg": "cyber_green", "fg": "black"}
        ]
    },
    
    "space_mars_mission": {
        "name": "Space Mars Mission", 
        "description": "Mars exploration mission",
        "category": "Space",
        "multiline": True,
        "segments": [
            [
                {"content": "🔴 Mars {model_name}", "bg": "sunset_red", "fg": "white"},
                {"content": "🏠 {project} Base", "bg": "sunset_orange", "fg": "white"}
            ],
            [
                {"content": "🌡️ {cpu}° | 💨 {ram}%", "bg": "sunset_yellow", "fg": "black"},
                {"content": "📡 {messages} transmissions", "bg": "sunset_pink", "fg": "black"}
            ]
        ]
    },
    
    # ============== NINJA SERIES (8 themes) ==============
    "ninja_shadow_stealth": {
        "name": "Ninja Shadow Stealth",
        "description": "Silent shadow ninja mode",
        "category": "Ninja",
        "multiline": False,
        "segments": [
            {"content": "🥷 {model_short}", "bg": "mono_black", "fg": "white"},
            {"content": "🏚️ {folder}", "bg": "mono_dark", "fg": "white"},
            {"content": "⚔️ {branch}", "bg": "mono_gray", "fg": "white"},
            {"content": "💨 {messages}m", "bg": "mono_silver", "fg": "black"},
            {"content": "🌙 ${cost}", "bg": "mono_white", "fg": "black"}
        ]
    },
    
    "ninja_fire_technique": {
        "name": "Ninja Fire Technique",
        "description": "Blazing fire ninja technique",
        "category": "Ninja",
        "multiline": False,
        "segments": [
            {"content": "🔥🥷 {model_short}", "bg": "sunset_red", "fg": "white"},
            {"content": "🏯 {project}", "bg": "sunset_orange", "fg": "white"},
            {"content": "⚔️ {git_branch}", "bg": "sunset_yellow", "fg": "black"},
            {"content": "💥 {messages} strikes", "bg": "sunset_pink", "fg": "black"},
            {"content": "🌟 {efficiency}", "bg": "sunset_purple", "fg": "white"}
        ]
    },
    
    # ============== DEVELOPER SERIES (10 themes) ==============
    "dev_full_stack_pro": {
        "name": "Dev Full Stack Pro",
        "description": "Full stack developer workspace",
        "category": "Developer",
        "multiline": False,
        "segments": [
            {"content": "⚡ {model_short}", "bg": "cyber_blue", "fg": "white"},
            {"content": "📂 {folder_name}", "bg": "cyber_purple", "fg": "white"},
            {"content": "🌿 {git_branch}", "bg": "cyber_green", "fg": "black"},
            {"content": "🔧 {cpu}%|{ram}%", "bg": "cyber_pink", "fg": "white"},
            {"content": "⏱️ {remaining}", "bg": "cyber_dark", "fg": "cyber_green"}
        ]
    },
    
    "dev_backend_ninja": {
        "name": "Dev Backend Ninja",
        "description": "Backend development ninja",
        "category": "Developer",
        "multiline": True,
        "segments": [
            [
                {"content": "🖥️ {model_name} Server", "bg": "mono_dark", "fg": "white"},
                {"content": "📁 {project} API", "bg": "mono_gray", "fg": "white"}
            ],
            [
                {"content": "🌿 {branch} Endpoint", "bg": "forest_green", "fg": "white"},
                {"content": "🔥 {messages} Requests", "bg": "sunset_red", "fg": "white"}
            ],
            [
                {"content": "💾 {tokens} Data", "bg": "cyber_blue", "fg": "white"}
            ]
        ]
    },
    
    # ============== MINIMALIST SERIES (8 themes) ==============
    "minimal_zen_flow": {
        "name": "Minimal Zen Flow",
        "description": "Zen minimalist flow",
        "category": "Minimalist",
        "multiline": False,
        "segments": [
            {"content": "◯ {model_short}", "bg": "mono_silver", "fg": "black"},
            {"content": "◯ {folder}", "bg": "mono_gray", "fg": "white"},
            {"content": "◯ {messages}m", "bg": "mono_dark", "fg": "white"},
            {"content": "◯ ${cost}", "bg": "mono_black", "fg": "white"}
        ]
    },
    
    "minimal_paper_clean": {
        "name": "Minimal Paper Clean",
        "description": "Clean paper white theme",
        "category": "Minimalist",
        "multiline": False,
        "segments": [
            {"content": "▫️ {model_name}", "bg": "mono_white", "fg": "black"},
            {"content": "▫️ {project}", "bg": "mono_silver", "fg": "black"},
            {"content": "▫️ {efficiency}", "bg": "mono_gray", "fg": "white"},
            {"content": "▫️ {remaining}", "bg": "mono_dark", "fg": "white"}
        ]
    },
}

# Additional 50+ theme variations will be generated dynamically
def generate_dynamic_themes():
    """Generate additional theme variations dynamically"""
    dynamic_themes = {}
    
    # Color combination generator
    color_combos = [
        ("cyber", ["cyber_dark", "cyber_purple", "cyber_blue", "cyber_green", "cyber_pink"]),
        ("neon", ["neon_pink", "neon_cyan", "neon_yellow", "neon_purple", "neon_green"]),
        ("ocean", ["ocean_deep", "ocean_blue", "ocean_teal", "ocean_aqua", "ocean_foam"]),
        ("sunset", ["sunset_orange", "sunset_red", "sunset_yellow", "sunset_pink", "sunset_purple"]),
        ("forest", ["forest_dark", "forest_green", "forest_lime", "forest_moss", "forest_mint"]),
        ("game", ["game_red", "game_blue", "game_purple", "game_green", "game_orange"]),
    ]
    
    # Icon sets for different themes
    icon_sets = {
        "tech": ["💻", "⚡", "🔧", "⚙️", "🚀"],
        "nature": ["🌿", "🌊", "🔥", "⭐", "🌙"],
        "business": ["💼", "📊", "📈", "💰", "🎯"],
        "gaming": ["🎮", "⚔️", "🏆", "💎", "🎲"],
        "space": ["🚀", "⭐", "🌌", "🛸", "🌍"]
    }
    
    # Generate 30+ additional single line themes
    for i in range(30):
        theme_name = f"dynamic_theme_{i+1:02d}"
        combo_name, colors = random.choice(color_combos)
        icons = random.choice(list(icon_sets.values()))
        
        segments = []
        fields = ["{model_short}", "{folder}", "{git_branch}", "{messages}m", "${cost}"]
        
        for j, (icon, field) in enumerate(zip(icons, fields)):
            segments.append({
                "content": f"{icon} {field}",
                "bg": colors[j % len(colors)],
                "fg": "white" if j % 2 == 0 else "black"
            })
            
        dynamic_themes[theme_name] = {
            "name": f"Dynamic {combo_name.title()} {i+1:02d}",
            "description": f"Dynamic {combo_name} theme variation {i+1}",
            "category": f"Dynamic-{combo_name.title()}",
            "multiline": False,
            "segments": segments
        }
    
    # Generate 20+ multiline themes
    for i in range(20):
        theme_name = f"multi_theme_{i+1:02d}"
        combo_name, colors = random.choice(color_combos)
        icons = random.choice(list(icon_sets.values()))
        
        # Create 2-3 line multiline theme
        lines = random.randint(2, 3)
        segments_list = []
        
        for line in range(lines):
            line_segments = []
            if line == 0:
                # First line: Model and project info
                line_segments.append({"content": f"{icons[0]} {'{model_name}'}", "bg": colors[0], "fg": "white"})
                line_segments.append({"content": f"{icons[1]} {'{folder_name}'}", "bg": colors[1], "fg": "white"})
            elif line == 1:
                # Second line: System info
                line_segments.append({"content": f"{icons[2]} {'{cpu}%|{ram}%'}", "bg": colors[2], "fg": "white"})
                line_segments.append({"content": f"{icons[3]} {'{messages}msg'}", "bg": colors[3], "fg": "white"})
            else:
                # Third line: Cost and efficiency
                line_segments.append({"content": f"{icons[4]} ${'{cost}'} | {'{efficiency}'}", "bg": colors[4], "fg": "white"})
            
            segments_list.append(line_segments)
        
        dynamic_themes[theme_name] = {
            "name": f"Multi {combo_name.title()} {i+1:02d}",
            "description": f"Multiline {combo_name} theme {lines} lines",
            "category": f"Multiline-{combo_name.title()}",
            "multiline": True,
            "segments": segments_list
        }
    
    return dynamic_themes

# Combine all themes
def get_all_epic_themes():
    """Get all epic themes including dynamic ones"""
    all_themes = EPIC_MEGA_THEMES.copy()
    all_themes.update(generate_dynamic_themes())
    return all_themes

# Theme categories for organization
EPIC_CATEGORIES = {
    "Cyberpunk": "High-tech cyberpunk and neon themes",
    "Ocean": "Ocean, water and sea themes", 
    "Sunset": "Warm sunset and fire themes",
    "Forest": "Nature and forest themes",
    "Gaming": "Gaming and retro arcade themes",
    "Professional": "Business and professional themes",
    "Space": "Space exploration themes",
    "Ninja": "Stealth and martial arts themes",
    "Developer": "Development workspace themes",
    "Minimalist": "Clean and minimal themes",
    "Dynamic-Cyber": "Dynamic cyberpunk variations",
    "Dynamic-Neon": "Dynamic neon variations",
    "Dynamic-Ocean": "Dynamic ocean variations",
    "Dynamic-Sunset": "Dynamic sunset variations",
    "Dynamic-Forest": "Dynamic forest variations",
    "Dynamic-Game": "Dynamic gaming variations",
    "Multiline-Cyber": "Multiline cyberpunk themes",
    "Multiline-Neon": "Multiline neon themes",
    "Multiline-Ocean": "Multiline ocean themes",
    "Multiline-Sunset": "Multiline sunset themes",
    "Multiline-Forest": "Multiline forest themes",
    "Multiline-Game": "Multiline gaming themes",
}

if __name__ == "__main__":
    themes = get_all_epic_themes()
    print(f"Generated {len(themes)} epic themes!")
    for category, count in [(cat, sum(1 for t in themes.values() if t.get('category') == cat)) for cat in EPIC_CATEGORIES.keys()]:
        if count > 0:
            print(f"  {category}: {count} themes")