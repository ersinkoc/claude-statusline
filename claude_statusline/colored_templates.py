#!/usr/bin/env python3
"""
Enhanced Colored Templates for Claude Statusline
Rich collection of themed templates with color support
"""

from typing import Dict, Any, Optional, Tuple
import random
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        BLACK = WHITE = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = ''
        LIGHTBLACK_EX = LIGHTWHITE_EX = LIGHTRED_EX = LIGHTGREEN_EX = ''
        LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTCYAN_EX = ''
        RESET = ''
    class Back:
        BLACK = WHITE = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = ''
        LIGHTBLACK_EX = LIGHTWHITE_EX = LIGHTRED_EX = LIGHTGREEN_EX = ''
        LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTCYAN_EX = ''
        RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''


class ColoredTemplates:
    """Collection of colored statusline templates"""
    
    def __init__(self):
        """Initialize colored templates"""
        self.templates = {
            # Developer Templates
            'vscode': self.vscode_format,
            'intellij': self.intellij_format,
            'sublime': self.sublime_format,
            'atom': self.atom_format,
            'neovim': self.neovim_format,
            'emacs': self.emacs_format,
            
            # Gaming Templates
            'minecraft': self.minecraft_format,
            'cyberpunk': self.cyberpunk_format,
            'retro': self.retro_format,
            'arcade': self.arcade_format,
            'rpg': self.rpg_format,
            
            # Professional Templates  
            'executive': self.executive_format,
            'analyst': self.analyst_format,
            'consultant': self.consultant_format,
            'startup': self.startup_format,
            
            # Creative Templates
            'rainbow': self.rainbow_format,
            'neon': self.neon_format,
            'pastel': self.pastel_format,
            'gradient': self.gradient_format,
            'artistic': self.artistic_format,
            
            # System Templates
            'windows': self.windows_format,
            'macos': self.macos_format,
            'ubuntu': self.ubuntu_format,
            'arch': self.arch_format,
            
            # Social Media Templates
            'twitter': self.twitter_format,
            'instagram': self.instagram_format,
            'youtube': self.youtube_format,
            'linkedin': self.linkedin_format,
            'reddit': self.reddit_format,
            
            # Special Templates
            'christmas': self.christmas_format,
            'halloween': self.halloween_format,
            'summer': self.summer_format,
            'winter': self.winter_format,
            'space': self.space_format,
            'ocean': self.ocean_format,
            'forest': self.forest_format,
            'desert': self.desert_format,
            
            # Minimalist Templates
            'mono': self.mono_format,
            'duo': self.duo_format,
            'noir': self.noir_format,
            'clean': self.clean_format,
            
            # Fun Templates
            'emoji_party': self.emoji_party_format,
            'kawaii': self.kawaii_format,
            'leetspeak': self.leetspeak_format,
            'pirate': self.pirate_format,
            'robot': self.robot_format,
            'wizard': self.wizard_format,
            
            # New Financial/Trading Templates
            'trading': self.trading_format,
            'crypto': self.crypto_format,
            'stock_market': self.stock_market_format,
            'banking': self.banking_format,
            
            # New Space/Science Templates  
            'nasa': self.nasa_format,
            'space_station': self.space_station_format,
            'alien': self.alien_format,
            'laboratory': self.laboratory_format,
            
            # New Medical/Health Templates
            'medical': self.medical_format,
            'hospital': self.hospital_format,
            'pharmacy': self.pharmacy_format,
            
            # New Transportation Templates
            'aviation': self.aviation_format,
            'railway': self.railway_format,
            'automotive': self.automotive_format,
            'maritime': self.maritime_format,
            
            # New Entertainment Templates
            'cinema': self.cinema_format,
            'music': self.music_format,
            'sports': self.sports_format,
            'news': self.news_format
        }
    
    def _get_data(self, data: Dict[str, Any]) -> Tuple:
        """Extract common data fields with enhanced information"""
        model = self._format_model(data.get('primary_model', data.get('model', 'Unknown')))
        active = data.get('active', False)
        remaining = data.get('remaining_seconds', 0)
        messages = data.get('message_count', 0)
        tokens = self._format_tokens(data.get('tokens', data.get('total_tokens', 0)))
        cost = data.get('cost', data.get('total_cost', 0.0))
        end_time = data.get('session_end_time', '')
        session_num = data.get('session_number', 0)
        
        # Git information
        git_branch = self._get_git_branch()
        git_status = self._get_git_status()
        
        # System information  
        folder = self._get_current_folder()
        cpu_usage = self._get_cpu_usage()
        memory_usage = self._get_memory_usage()
        
        # Time information
        current_time = datetime.now().strftime('%H:%M')
        remaining_formatted = self._format_remaining_time(remaining)
        
        if active and remaining > 0:
            status = 'LIVE'
        elif remaining > 0:
            status = 'ACTIVE'
        else:
            status = 'OFF'
            
        return (model, status, messages, tokens, cost, end_time, remaining, 
                session_num, git_branch, git_status, folder, cpu_usage, 
                memory_usage, current_time, remaining_formatted)
    
    def _format_model(self, model: str) -> str:
        """Format model name"""
        if not model or model == 'Unknown':
            return 'Unknown'
        
        # Try to get display name from prices.json
        try:
            import json
            from pathlib import Path
            prices_file = Path(__file__).parent / 'prices.json'
            if prices_file.exists():
                with open(prices_file, 'r') as f:
                    prices = json.load(f)
                    models = prices.get('models', {})
                    if model in models:
                        return models[model].get('name', model)
        except:
            pass
        
        # Fallback formatting
        model_lower = model.lower()
        if 'opus' in model_lower:
            if '4.1' in model:
                return 'Opus 4.1'
            return 'Opus'
        elif 'sonnet' in model_lower:
            if '3.5' in model:
                return 'Sonnet 3.5'
            return 'Sonnet'
        elif 'haiku' in model_lower:
            return 'Haiku'
        
        return model.replace('claude-', '').split('-')[0].title()
    
    def _format_tokens(self, tokens: int) -> str:
        """Format token count"""
        if tokens < 1000:
            return f"{tokens}"
        elif tokens < 1_000_000:
            return f"{tokens/1000:.1f}k"
        else:
            return f"{tokens/1_000_000:.1f}M"
    
    def _get_git_branch(self) -> str:
        """Get current git branch"""
        try:
            import subprocess
            result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return 'main'
    
    def _get_git_status(self) -> str:
        """Get git status"""
        try:
            import subprocess
            result = subprocess.run(['git', 'status', '--porcelain'],
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                if result.stdout.strip():
                    return 'modified'
                return 'clean'
        except:
            pass
        return 'unknown'
    
    def _get_current_folder(self) -> str:
        """Get current folder name"""
        try:
            from pathlib import Path
            return Path.cwd().name
        except:
            return 'folder'
    
    def _get_cpu_usage(self) -> str:
        """Get CPU usage percentage"""
        try:
            import psutil
            return f"{psutil.cpu_percent(interval=0.1):.0f}%"
        except:
            return f"{random.randint(15, 85)}%"
    
    def _get_memory_usage(self) -> str:
        """Get memory usage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return f"{memory.percent:.0f}%"
        except:
            return f"{random.randint(40, 80)}%"
    
    def _format_remaining_time(self, seconds: int) -> str:
        """Format remaining time"""
        if seconds <= 0:
            return "0m"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h{minutes}m"
        else:
            return f"{minutes}m"
    
    def _get_battery_info(self) -> str:
        """Get battery information"""
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                percent = int(battery.percent)
                if battery.power_plugged:
                    return f"🔌{percent}%"
                elif percent > 80:
                    return f"🔋{percent}%"
                elif percent > 20:
                    return f"🔋{percent}%"
                else:
                    return f"🪫{percent}%"
        except:
            pass
        return "🔋85%"
    
    # DEVELOPER TEMPLATES
    
    def vscode_format(self, data: Dict[str, Any]) -> str:
        """Enhanced VSCode style statusline with full information"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        if status == 'LIVE':
            status_color = Fore.GREEN
            icon = '●'
        else:
            status_color = Fore.YELLOW
            icon = '○'
        
        git_color = Fore.GREEN if git_status == 'clean' else Fore.YELLOW
        battery = self._get_battery_info()
        
        return (f"{Fore.BLUE}◈ {Fore.CYAN}{model}{Style.RESET_ALL} "
                f"{status_color}{icon} {status}{Style.RESET_ALL} "
                f"{Fore.WHITE}#{session_num}{Style.RESET_ALL} "
                f"{git_color}⎇ {git_branch}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}📁 {folder}{Style.RESET_ALL} "
                f"{Fore.WHITE}Ln {msgs}, Col {tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.CYAN}⏰ {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🖥️ {cpu} 🧠 {memory}{Style.RESET_ALL} "
                f"{battery} "
                f"{Fore.MAGENTA}UTF-8{Style.RESET_ALL}")
    
    def intellij_format(self, data: Dict[str, Any]) -> str:
        """Enhanced IntelliJ IDEA style with project info"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        status_bg = Back.GREEN if status == 'LIVE' else Back.YELLOW
        git_icon = "✓" if git_status == 'clean' else "⚡"
        
        return (f"{Fore.WHITE}🧠 {model}{Style.RESET_ALL} "
                f"{status_bg}{Fore.BLACK} {status} {Style.RESET_ALL} "
                f"{Fore.GREEN}📁 {folder}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}{git_icon} {git_branch}{Style.RESET_ALL} "
                f"{Fore.BLUE}↕ {msgs} msgs{Style.RESET_ALL} "
                f"{Fore.CYAN}∑ {tokens} tokens{Style.RESET_ALL} "
                f"{Fore.YELLOW}$ {cost:.3f}{Style.RESET_ALL} "
                f"{Fore.RED}⏱️ {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🖥️ CPU: {cpu} RAM: {memory}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}Session #{session_num} | {current_time}{Style.RESET_ALL}")
    
    def sublime_format(self, data: Dict[str, Any]) -> str:
        """Enhanced Sublime Text style with elegant info"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        status_dot = "🟢" if status == 'LIVE' else "🟡"
        
        return (f"{Fore.LIGHTWHITE_EX}✨ {model}{Style.RESET_ALL} "
                f"{status_dot} "
                f"{Fore.CYAN}📂 {folder}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}🌿 {git_branch}{Style.RESET_ALL} "
                f"{Fore.CYAN}⟨{msgs} msgs⟩{Style.RESET_ALL} "
                f"{Fore.MAGENTA}◆{tokens} tokens{Style.RESET_ALL} "
                f"{Fore.GREEN}💰 ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.YELLOW}⏰ {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}{cpu} {memory} | #{session_num}{Style.RESET_ALL}")
    
    def atom_format(self, data: Dict[str, Any]) -> str:
        """Enhanced Atom editor style with packages info"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        status_color = Fore.LIGHTGREEN_EX if status == 'LIVE' else Fore.LIGHTBLACK_EX
        git_icon = "📦" if git_status == 'clean' else "⚠️"
        
        return (f"{Fore.GREEN}⚛️ {Style.RESET_ALL}"
                f"{Fore.LIGHTCYAN_EX}{model}{Style.RESET_ALL} "
                f"{status_color}[{status}]{Style.RESET_ALL} "
                f"{Fore.MAGENTA}{git_icon} {git_branch}{Style.RESET_ALL} "
                f"{Fore.BLUE}📁 {folder}{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs}:{tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}💵 ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.CYAN}🕐 {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}Session {session_num} | {current_time}{Style.RESET_ALL}")
    
    def neovim_format(self, data: Dict[str, Any]) -> str:
        """Enhanced Neovim style with powerline symbols and vim info"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        if status == 'LIVE':
            mode = f"{Back.GREEN}{Fore.BLACK} ● LIVE {Style.RESET_ALL}"
        else:
            mode = f"{Back.YELLOW}{Fore.BLACK} ◐ INSERT {Style.RESET_ALL}"
        
        git_info = f"{Back.MAGENTA}{Fore.WHITE} ⎇ {git_branch} {Style.RESET_ALL}" if git_branch != 'main' else ""
        
        return (f"{mode} "
                f"{Back.BLUE}{Fore.WHITE} 🧠 {model} {Style.RESET_ALL}"
                f"{git_info}"
                f"{Back.CYAN}{Fore.BLACK} 📁 {folder} {Style.RESET_ALL}"
                f"{Fore.WHITE}  {msgs}L {tokens}C{Style.RESET_ALL} "
                f"{Fore.YELLOW}💰 ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.RED}⏰ {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}#{session_num} {cpu} {memory}{Style.RESET_ALL}")
    
    def emacs_format(self, data: Dict[str, Any]) -> str:
        """Enhanced Emacs modeline with elisp-style info"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        mode_indicator = "***" if status == 'LIVE' else "-UU"
        git_indicator = f"Git:{git_branch}" if git_branch else ""
        
        return (f"{Fore.LIGHTBLACK_EX}{mode_indicator}:{Style.RESET_ALL}"
                f"{Fore.CYAN}**{Style.RESET_ALL}"
                f"{Fore.WHITE}-{Style.RESET_ALL}"
                f"{Fore.GREEN}F1{Style.RESET_ALL}  "
                f"{Fore.LIGHTWHITE_EX}({model}){Style.RESET_ALL}  "
                f"{Fore.MAGENTA}[{folder}]{Style.RESET_ALL} "
                f"{Fore.BLUE}{git_indicator}{Style.RESET_ALL} "
                f"{Fore.WHITE}L{msgs} C{tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}(Cost:${cost:.3f}){Style.RESET_ALL} "
                f"{Fore.RED}(Time:{time_left}){Style.RESET_ALL} "
                f"{Fore.CYAN}(Sess:{session_num}){Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}--{status}--{current_time}--{Style.RESET_ALL}")
    
    # GAMING TEMPLATES
    
    def minecraft_format(self, data: Dict[str, Any]) -> str:
        """Enhanced Minecraft style with inventory and world info"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        if status == 'LIVE':
            heart = f"{Fore.RED}♥♥♥♥♥{Style.RESET_ALL}"
            hunger = f"{Fore.YELLOW}🍖🍖🍖🍖🍖{Style.RESET_ALL}"
        else:
            heart = f"{Fore.LIGHTBLACK_EX}♥♥{Style.RESET_ALL}{Fore.RED}♥♥♥{Style.RESET_ALL}"
            hunger = f"{Fore.YELLOW}🍖🍖🍖{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}🍖🍖{Style.RESET_ALL}"
        
        # Generate minecraft items based on info
        items = ["⛏️", "🪓", "⚔️", "🏹", "🛡️", "💎"]
        current_item = items[session_num % len(items)]
        
        return (f"{Fore.GREEN}{current_item}{Style.RESET_ALL} "
                f"{Fore.LIGHTGREEN_EX}[{model}]{Style.RESET_ALL} "
                f"{Fore.CYAN}🌍 {folder} Biome{Style.RESET_ALL} "
                f"{Fore.MAGENTA}Day {session_num}{Style.RESET_ALL} "
                f"{heart} "
                f"{hunger} "
                f"{Fore.YELLOW}XP: {msgs}{Style.RESET_ALL} "
                f"{Fore.CYAN}💎 {tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}⛃ {cost:.0f} Coins{Style.RESET_ALL} "
                f"{Fore.RED}⏰ {time_left}{Style.RESET_ALL}")
    
    def cyberpunk_format(self, data: Dict[str, Any]) -> str:
        """Enhanced Cyberpunk 2077 style with neural interface"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        neural_status = "ONLINE" if status == 'LIVE' else "STANDBY"
        corp_name = folder.upper()[:8]  # Use folder as corp name
        
        # Generate glitch effect occasionally
        glitch = random.choice(["", "░", "▒", "▓"]) if random.random() < 0.1 else ""
        
        return (f"{Fore.MAGENTA}◢{Style.BRIGHT}NEURAL{Style.RESET_ALL}{Fore.MAGENTA}◤{Style.RESET_ALL} "
                f"{Fore.CYAN}{Style.BRIGHT}[{model}]{Style.RESET_ALL} "
                f"{Fore.YELLOW}⟦{neural_status}⟧{Style.RESET_ALL} "
                f"{Fore.GREEN}CORP: {corp_name}{Style.RESET_ALL} "
                f"{Fore.LIGHTMAGENTA_EX}RAM: {msgs}GB{Style.RESET_ALL} "
                f"{Fore.LIGHTCYAN_EX}CPU: {tokens}GHz{Style.RESET_ALL} "
                f"{Fore.YELLOW}€$ {cost:.1f}K{Style.RESET_ALL} "
                f"{Fore.RED}SYS: {cpu} {memory}{Style.RESET_ALL} "
                f"{Fore.BLUE}NET: {git_branch}{Style.RESET_ALL} "
                f"{Fore.WHITE}TIME: {time_left}{Style.RESET_ALL}{glitch} "
                f"{Fore.MAGENTA}◢{Style.BRIGHT}#{session_num:03d}{Style.RESET_ALL}{Fore.MAGENTA}◤{Style.RESET_ALL}")
    
    def retro_format(self, data: Dict[str, Any]) -> str:
        """80s retro style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        colors = [Fore.MAGENTA, Fore.CYAN, Fore.YELLOW]
        model_colored = ''.join(colors[i % 3] + c for i, c in enumerate(model)) + Style.RESET_ALL
        
        return (f"{Fore.MAGENTA}▓▒░{Style.RESET_ALL} "
                f"{model_colored} "
                f"{Fore.CYAN}◄{msgs}►{Style.RESET_ALL} "
                f"{Fore.YELLOW}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}░▒▓{Style.RESET_ALL}")
    
    def arcade_format(self, data: Dict[str, Any]) -> str:
        """Arcade game style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        score = msgs * 100
        
        return (f"{Fore.YELLOW}★{Style.RESET_ALL} "
                f"{Fore.CYAN}PLAYER:{model}{Style.RESET_ALL} "
                f"{Fore.GREEN}SCORE:{score:06d}{Style.RESET_ALL} "
                f"{Fore.RED}COINS:{int(cost)}{Style.RESET_ALL} "
                f"{Fore.YELLOW}★{Style.RESET_ALL}")
    
    def rpg_format(self, data: Dict[str, Any]) -> str:
        """RPG game style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        hp = min(100, remaining // 180)  # HP based on remaining time
        # Convert tokens string to number for MP calculation
        token_num = data.get('tokens', data.get('total_tokens', 0))
        if isinstance(token_num, str):
            token_num = 0
        mp = min(100, token_num // 10000)  # MP based on tokens
        
        return (f"{Fore.GREEN}♦{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}{model}{Style.RESET_ALL} "
                f"{Fore.RED}HP:{hp}/100{Style.RESET_ALL} "
                f"{Fore.BLUE}MP:{mp}/100{Style.RESET_ALL} "
                f"{Fore.YELLOW}LV:{msgs}{Style.RESET_ALL} "
                f"{Fore.YELLOW}₲{cost:.0f}{Style.RESET_ALL}")
    
    # PROFESSIONAL TEMPLATES
    
    def executive_format(self, data: Dict[str, Any]) -> str:
        """Executive dashboard style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} "
                f"{Fore.WHITE}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.YELLOW}{status}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}Sessions: {msgs}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}Volume: {tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}│{Style.RESET_ALL} "
                f"{Fore.GREEN}${cost:,.2f}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}│{Style.RESET_ALL}")
    
    def analyst_format(self, data: Dict[str, Any]) -> str:
        """Data analyst style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.BLUE}📊{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}[{Style.RESET_ALL}"
                f"{Fore.CYAN}n={msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}Σ={tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}μ=${cost:.2f}{Style.RESET_ALL}"
                f"{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL}")
    
    def consultant_format(self, data: Dict[str, Any]) -> str:
        """Management consultant style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        roi = (msgs * 10) / max(cost, 1)  # Fake ROI calculation
        
        return (f"{Fore.LIGHTBLACK_EX}▪{Style.RESET_ALL} "
                f"{Fore.WHITE}Model: {model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}▪{Style.RESET_ALL} "
                f"{Fore.WHITE}Utilization: {msgs}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}▪{Style.RESET_ALL} "
                f"{Fore.WHITE}ROI: {roi:.1f}x{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}▪{Style.RESET_ALL} "
                f"{Fore.GREEN}Budget: ${cost:.2f}{Style.RESET_ALL}")
    
    def startup_format(self, data: Dict[str, Any]) -> str:
        """Startup hustle style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.CYAN}🚀{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}{model}{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.YELLOW}•{status}{Style.RESET_ALL} "
                f"{Fore.WHITE}🔥{msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}⚡{tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}💰${cost:.0f}{Style.RESET_ALL}")
    
    # CREATIVE TEMPLATES
    
    def rainbow_format(self, data: Dict[str, Any]) -> str:
        """Rainbow colored output"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        
        output = ""
        parts = [f"[{model}]", status, f"{msgs}msg", tokens, f"${cost:.0f}"]
        
        for i, part in enumerate(parts):
            color = colors[i % len(colors)]
            output += f"{color}{part}{Style.RESET_ALL} "
        
        return output.strip()
    
    def neon_format(self, data: Dict[str, Any]) -> str:
        """Neon lights style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}◆{model}◆{Style.RESET_ALL} "
                f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}{status}{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{msgs}msg{Style.RESET_ALL} "
                f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTRED_EX}{Style.BRIGHT}${cost:.0f}{Style.RESET_ALL}")
    
    def pastel_format(self, data: Dict[str, Any]) -> str:
        """Soft pastel colors"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTMAGENTA_EX}✿ {model}{Style.RESET_ALL} "
                f"{Fore.LIGHTCYAN_EX}{status}{Style.RESET_ALL} "
                f"{Fore.LIGHTGREEN_EX}{msgs} messages{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}${cost:.1f}{Style.RESET_ALL} "
                f"{Fore.LIGHTMAGENTA_EX}✿{Style.RESET_ALL}")
    
    def gradient_format(self, data: Dict[str, Any]) -> str:
        """Gradient style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.BLUE}░{Fore.CYAN}▒{Fore.GREEN}▓ "
                f"{Fore.LIGHTWHITE_EX}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTGREEN_EX}{msgs}msg{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}{tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTRED_EX}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.GREEN}▓{Fore.CYAN}▒{Fore.BLUE}░{Style.RESET_ALL}")
    
    def artistic_format(self, data: Dict[str, Any]) -> str:
        """Artistic style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.MAGENTA}◈{Style.RESET_ALL} "
                f"{Fore.CYAN}❨{model}❩{Style.RESET_ALL} "
                f"{Fore.YELLOW}✦{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs} strokes{Style.RESET_ALL} "
                f"{Fore.YELLOW}✦{Style.RESET_ALL} "
                f"{Fore.GREEN}${cost:.1f}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}◈{Style.RESET_ALL}")
    
    # SYSTEM TEMPLATES
    
    def windows_format(self, data: Dict[str, Any]) -> str:
        """Windows 11 style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.CYAN}⊞{Style.RESET_ALL} "
                f"{Fore.WHITE}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}|{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.YELLOW}{status}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}|{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs} items{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}|{Style.RESET_ALL} "
                f"{Fore.YELLOW}${cost:.2f}{Style.RESET_ALL}")
    
    def macos_format(self, data: Dict[str, Any]) -> str:
        """macOS style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTWHITE_EX} {model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}—{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.YELLOW}●{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}{msgs}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}—{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}{tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}—{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}${cost:.2f}{Style.RESET_ALL}")
    
    def ubuntu_format(self, data: Dict[str, Any]) -> str:
        """Ubuntu style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTRED_EX}●{Fore.LIGHTYELLOW_EX}●{Fore.LIGHTGREEN_EX}● "
                f"{Fore.WHITE}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}>{Style.RESET_ALL} "
                f"{Fore.GREEN}{msgs} tasks{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}>{Style.RESET_ALL} "
                f"{Fore.YELLOW}${cost:.1f}{Style.RESET_ALL}")
    
    def arch_format(self, data: Dict[str, Any]) -> str:
        """Arch Linux style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.CYAN}λ{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}{model}{Style.RESET_ALL} "
                f"{Fore.CYAN}::{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs}{Style.RESET_ALL} "
                f"{Fore.CYAN}::{Style.RESET_ALL} "
                f"{Fore.WHITE}{tokens}{Style.RESET_ALL} "
                f"{Fore.CYAN}::{Style.RESET_ALL} "
                f"{Fore.YELLOW}${cost:.2f}{Style.RESET_ALL}")
    
    # Fun continues with more templates...
    
    def mono_format(self, data: Dict[str, Any]) -> str:
        """Monochrome minimalist"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        return f"{Fore.WHITE}{model} {msgs} ${cost:.0f}{Style.RESET_ALL}"
    
    def kawaii_format(self, data: Dict[str, Any]) -> str:
        """Kawaii cute style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTMAGENTA_EX}(◕‿◕){Style.RESET_ALL} "
                f"{Fore.LIGHTCYAN_EX}{model}-chan{Style.RESET_ALL} "
                f"{Fore.LIGHTRED_EX}♥{msgs}{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}✨{tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTGREEN_EX}¥{cost:.0f}{Style.RESET_ALL} "
                f"{Fore.LIGHTMAGENTA_EX}(´｡• ᵕ •｡`){Style.RESET_ALL}")
    
    # SOCIAL MEDIA TEMPLATES
    
    def twitter_format(self, data: Dict[str, Any]) -> str:
        """Twitter/X style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.CYAN}𝕏{Style.RESET_ALL} "
                f"{Fore.WHITE}@{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}·{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs} posts{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}·{Style.RESET_ALL} "
                f"{Fore.CYAN}{tokens} impressions{Style.RESET_ALL}")
    
    def instagram_format(self, data: Dict[str, Any]) -> str:
        """Instagram style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.MAGENTA}📷{Style.RESET_ALL} "
                f"{Fore.WHITE}{model}{Style.RESET_ALL} "
                f"{Fore.RED}♥ {msgs}{Style.RESET_ALL} "
                f"{Fore.WHITE}💬 {tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}${cost:.0f}{Style.RESET_ALL}")
    
    def youtube_format(self, data: Dict[str, Any]) -> str:
        """YouTube style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        views = msgs * 1000
        
        return (f"{Back.RED}{Fore.WHITE} ▶ {Style.RESET_ALL} "
                f"{Fore.WHITE}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}•{Style.RESET_ALL} "
                f"{Fore.WHITE}{views:,} views{Style.RESET_ALL} "
                f"{Fore.GREEN}👍 {msgs}{Style.RESET_ALL}")
    
    def linkedin_format(self, data: Dict[str, Any]) -> str:
        """LinkedIn professional style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.BLUE}in{Style.RESET_ALL} "
                f"{Fore.WHITE}{model} Professional{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}|{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs} connections{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}|{Style.RESET_ALL} "
                f"{Fore.BLUE}${cost:.2f}{Style.RESET_ALL}")
    
    def reddit_format(self, data: Dict[str, Any]) -> str:
        """Reddit style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        karma = msgs * 10
        
        return (f"{Fore.LIGHTRED_EX}🤖{Style.RESET_ALL} "
                f"{Fore.WHITE}u/{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTRED_EX}↑{karma}{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs} posts{Style.RESET_ALL} "
                f"{Fore.YELLOW}🏅{int(cost/10)}{Style.RESET_ALL}")
    
    # SEASONAL TEMPLATES
    
    def christmas_format(self, data: Dict[str, Any]) -> str:
        """Christmas theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.RED}🎄{Style.RESET_ALL} "
                f"{Fore.GREEN}{model}{Style.RESET_ALL} "
                f"{Fore.RED}🎅{Style.RESET_ALL} "
                f"{Fore.WHITE}{msgs} gifts{Style.RESET_ALL} "
                f"{Fore.YELLOW}⭐{tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.RED}🎁{Style.RESET_ALL}")
    
    def halloween_format(self, data: Dict[str, Any]) -> str:
        """Halloween spooky theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTRED_EX}🎃{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}👻{msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}🦇{tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}💀${cost:.0f}{Style.RESET_ALL}")
    
    def summer_format(self, data: Dict[str, Any]) -> str:
        """Summer vibes"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.YELLOW}☀️{Style.RESET_ALL} "
                f"{Fore.CYAN}{model}{Style.RESET_ALL} "
                f"{Fore.BLUE}🌊{msgs}{Style.RESET_ALL} "
                f"{Fore.GREEN}🌴{tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.CYAN}🏖️{Style.RESET_ALL}")
    
    def winter_format(self, data: Dict[str, Any]) -> str:
        """Winter theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.CYAN}❄️{Style.RESET_ALL} "
                f"{Fore.LIGHTCYAN_EX}{model}{Style.RESET_ALL} "
                f"{Fore.WHITE}⛄{msgs}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLUE_EX}🌨️{tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}${cost:.0f}{Style.RESET_ALL}")
    
    def space_format(self, data: Dict[str, Any]) -> str:
        """Space theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.BLUE}🚀{Style.RESET_ALL} "
                f"{Fore.LIGHTWHITE_EX}{model}{Style.RESET_ALL} "
                f"{Fore.YELLOW}⭐{msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}🌌{tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.CYAN}🛸{Style.RESET_ALL}")
    
    def ocean_format(self, data: Dict[str, Any]) -> str:
        """Ocean theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.BLUE}🌊{Style.RESET_ALL} "
                f"{Fore.CYAN}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLUE_EX}🐠{msgs}{Style.RESET_ALL} "
                f"{Fore.BLUE}🐙{tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.CYAN}🐚{Style.RESET_ALL}")
    
    def forest_format(self, data: Dict[str, Any]) -> str:
        """Forest theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.GREEN}🌲{Style.RESET_ALL} "
                f"{Fore.LIGHTGREEN_EX}{model}{Style.RESET_ALL} "
                f"{Fore.YELLOW}🦌{msgs}{Style.RESET_ALL} "
                f"{Fore.GREEN}🌿{tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.GREEN}🍄{Style.RESET_ALL}")
    
    def desert_format(self, data: Dict[str, Any]) -> str:
        """Desert theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.YELLOW}🏜️{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}{model}{Style.RESET_ALL} "
                f"{Fore.GREEN}🌵{msgs}{Style.RESET_ALL} "
                f"{Fore.YELLOW}☀️{tokens}{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}${cost:.0f}{Style.RESET_ALL} "
                f"{Fore.YELLOW}🦂{Style.RESET_ALL}")
    
    # MINIMALIST TEMPLATES
    
    def duo_format(self, data: Dict[str, Any]) -> str:
        """Two-tone minimalist"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.WHITE}{model}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}| {msgs} | {tokens} | ${cost:.0f}{Style.RESET_ALL}")
    
    def noir_format(self, data: Dict[str, Any]) -> str:
        """Dark noir theme"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTBLACK_EX}■ {model} ■ {msgs} ■ ${cost:.0f} ■{Style.RESET_ALL}")
    
    def clean_format(self, data: Dict[str, Any]) -> str:
        """Clean minimal"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return f"{Fore.LIGHTWHITE_EX}{model}  {msgs}  ${cost:.0f}{Style.RESET_ALL}"
    
    # FUN TEMPLATES
    
    def emoji_party_format(self, data: Dict[str, Any]) -> str:
        """Emoji party mode"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        emojis = ['🎉', '🎊', '🎈', '🎆', '✨']
        import random
        emoji = random.choice(emojis)
        
        return (f"{emoji} {Fore.MAGENTA}{model}{Style.RESET_ALL} "
                f"{emoji} {Fore.CYAN}{msgs}{Style.RESET_ALL} "
                f"{emoji} {Fore.YELLOW}${cost:.0f}{Style.RESET_ALL} {emoji}")
    
    def leetspeak_format(self, data: Dict[str, Any]) -> str:
        """L33t h4x0r style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        # Convert to leetspeak
        leet_model = model.replace('O', '0').replace('o', '0').replace('E', '3').replace('e', '3')
        
        return (f"{Fore.GREEN}[{leet_model}]{Style.RESET_ALL} "
                f"{Fore.GREEN}m5g5:{msgs}{Style.RESET_ALL} "
                f"{Fore.GREEN}t0k3n5:{tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}c0$t:{cost:.0f}{Style.RESET_ALL}")
    
    def pirate_format(self, data: Dict[str, Any]) -> str:
        """Pirate speak arrr"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.YELLOW}🏴‍☠️{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}Cap'n {model}{Style.RESET_ALL} "
                f"{Fore.WHITE}⚓ {msgs} messages{Style.RESET_ALL} "
                f"{Fore.YELLOW}🪙 {cost:.0f} doubloons{Style.RESET_ALL} "
                f"{Fore.LIGHTYELLOW_EX}Arrr!{Style.RESET_ALL}")
    
    def robot_format(self, data: Dict[str, Any]) -> str:
        """Robot beep boop"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.LIGHTBLACK_EX}[{Style.RESET_ALL}"
                f"{Fore.CYAN}UNIT:{model}{Style.RESET_ALL}"
                f"{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} "
                f"{Fore.GREEN}MSGS={msgs}{Style.RESET_ALL} "
                f"{Fore.YELLOW}TOKENS={tokens}{Style.RESET_ALL} "
                f"{Fore.RED}COST=${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}[BEEP]{Style.RESET_ALL}")
    
    def wizard_format(self, data: Dict[str, Any]) -> str:
        """Wizard magical style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        return (f"{Fore.MAGENTA}🔮{Style.RESET_ALL} "
                f"{Fore.LIGHTMAGENTA_EX}Wizard {model}{Style.RESET_ALL} "
                f"{Fore.CYAN}✨ {msgs} spells{Style.RESET_ALL} "
                f"{Fore.YELLOW}⚗️ {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}💰 {cost:.0f}gp{Style.RESET_ALL} "
                f"{Fore.MAGENTA}🪄{Style.RESET_ALL}")
    
    # NEW FINANCIAL/TRADING TEMPLATES
    
    def trading_format(self, data: Dict[str, Any]) -> str:
        """Trading terminal style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        # Generate mock trading data
        ticker = folder.upper()[:4]
        trend = "📈" if status == 'LIVE' else "📉"
        price_change = f"+{cost*10:.2f}" if status == 'LIVE' else f"-{cost*5:.2f}"
        volume = f"{msgs*1000:,}"
        
        return (f"{Fore.GREEN}$ {ticker} {trend}{Style.RESET_ALL} "
                f"{Fore.WHITE}[{model}] TRADING{Style.RESET_ALL} "
                f"{Fore.CYAN}#{session_num:04d}{Style.RESET_ALL} "
                f"{Fore.YELLOW}PRICE: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.RED}{price_change} ({cost*2:.1f}%){Style.RESET_ALL} "
                f"{Fore.BLUE}VOL: {volume}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}TOKENS: {tokens}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}NYSE OPEN{Style.RESET_ALL}")
    
    def crypto_format(self, data: Dict[str, Any]) -> str:
        """Cryptocurrency exchange style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        # Generate crypto symbols
        crypto_symbols = ["₿", "Ξ", "◈", "Ł", "⊗"]
        symbol = crypto_symbols[session_num % len(crypto_symbols)]
        coin_name = folder.upper()[:3] + "C"  # ClaudeCoin, etc.
        
        market_cap = f"{cost * msgs * 1000:.0f}K"
        
        return (f"{Fore.YELLOW}{symbol} {coin_name}{Style.RESET_ALL} "
                f"{Fore.CYAN}[{model} BLOCKCHAIN]{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.RED}●{Style.RESET_ALL} "
                f"{Fore.WHITE}${cost:.6f}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}24H: {tokens}{Style.RESET_ALL} "
                f"{Fore.CYAN}VOL: {msgs}B{Style.RESET_ALL} "
                f"{Fore.YELLOW}MCAP: ${market_cap}{Style.RESET_ALL} "
                f"{Fore.BLUE}MINING: {cpu} {memory}{Style.RESET_ALL} "
                f"{Fore.WHITE}⛏️ #{session_num} | {time_left}{Style.RESET_ALL}")
    
    def stock_market_format(self, data: Dict[str, Any]) -> str:
        """Bloomberg terminal style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        ticker = (folder[:3] + "AI").upper()
        exchange = random.choice(["NYSE", "NASDAQ", "LSE", "TSX"])
        
        return (f"{Fore.YELLOW}■ {ticker}:{exchange}{Style.RESET_ALL} "
                f"{Back.BLUE}{Fore.WHITE} {model} ANALYTICS {Style.RESET_ALL} "
                f"{Fore.GREEN}LAST: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.CYAN}VOL: {msgs}M{Style.RESET_ALL} "
                f"{Fore.MAGENTA}TOKENS: {tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}P/E: {session_num:.1f}{Style.RESET_ALL} "
                f"{Fore.RED}52W H/L: ${cost*2:.0f}/${cost*0.5:.0f}{Style.RESET_ALL} "
                f"{Fore.BLUE}⏰ MARKET {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}SYS: {cpu} {memory}{Style.RESET_ALL}")
    
    def banking_format(self, data: Dict[str, Any]) -> str:
        """Banking system style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        account_num = f"{session_num:06d}"
        balance = f"${cost * msgs * 100:,.2f}"
        
        return (f"{Fore.BLUE}🏦 CLAUDE BANK{Style.RESET_ALL} "
                f"{Fore.WHITE}[{model} SECURE]{Style.RESET_ALL} "
                f"{Fore.GREEN}ACC: ****{account_num[-4:]}{Style.RESET_ALL} "
                f"{Fore.YELLOW}BAL: {balance}{Style.RESET_ALL} "
                f"{Fore.CYAN}TXN: {msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}CREDITS: {tokens}{Style.RESET_ALL} "
                f"{Fore.RED}PENDING: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.BLUE}⏰ {current_time} | {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🔒 ENCRYPTED | {git_branch}{Style.RESET_ALL}")
    
    # NEW SPACE/SCIENCE TEMPLATES
    
    def nasa_format(self, data: Dict[str, Any]) -> str:
        """NASA Mission Control style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        mission_name = f"CLAUDE-{session_num:02d}"
        altitude = f"{msgs * 100}km"
        velocity = f"{tokens[:4]}m/s" if isinstance(tokens, str) else f"{random.randint(7000,8000)}m/s"
        
        return (f"{Fore.WHITE}🚀 NASA HOUSTON{Style.RESET_ALL} "
                f"{Fore.CYAN}[{model} MISSION CONTROL]{Style.RESET_ALL} "
                f"{Fore.GREEN}GO/NO-GO: {status}{Style.RESET_ALL} "
                f"{Fore.YELLOW}MISSION: {mission_name}{Style.RESET_ALL} "
                f"{Fore.BLUE}ALT: {altitude}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}VEL: {velocity}{Style.RESET_ALL} "
                f"{Fore.RED}FUEL: {100-int(cost)}%{Style.RESET_ALL} "
                f"{Fore.CYAN}COMMS: {msgs}{Style.RESET_ALL} "
                f"{Fore.WHITE}T- {time_left} | {current_time} UTC{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🌍 EARTH ORBIT{Style.RESET_ALL}")
    
    def space_station_format(self, data: Dict[str, Any]) -> str:
        """International Space Station style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        orbit = f"ORB {session_num:03d}"
        solar_power = f"{100-int(cost)}%"
        
        return (f"{Fore.BLUE}🛰️ ISS-CLAUDE{Style.RESET_ALL} "
                f"{Fore.WHITE}[{model} STATION]{Style.RESET_ALL} "
                f"{Fore.GREEN}SYS: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}{orbit}{Style.RESET_ALL} "
                f"{Fore.YELLOW}⚡ {solar_power}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}EXP: {msgs}{Style.RESET_ALL} "
                f"{Fore.BLUE}DATA: {tokens}{Style.RESET_ALL} "
                f"{Fore.RED}💰 ${cost:.1f}M{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🌍↗️🌙 {cpu} {memory}{Style.RESET_ALL}")
    
    def alien_format(self, data: Dict[str, Any]) -> str:
        """Alien contact style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        # Alien symbols
        alien_chars = ["◊", "◈", "♦", "⬟", "⬢", "⬡"]
        symbols = "".join(random.choices(alien_chars, k=3))
        
        return (f"{Fore.GREEN}👽 {symbols}{Style.RESET_ALL} "
                f"{Fore.CYAN}[{model} XENOTECH]{Style.RESET_ALL} "
                f"{Fore.GREEN}SIGNAL: {status}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}COORD: {session_num}.{msgs}{Style.RESET_ALL} "
                f"{Fore.YELLOW}ENERGY: {tokens}{Style.RESET_ALL} "
                f"{Fore.RED}DANGER: {cost:.1f}⚡{Style.RESET_ALL} "
                f"{Fore.BLUE}TRANSLATE: {folder[:6]}{Style.RESET_ALL} "
                f"{Fore.WHITE}TIME: {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🌌 SECTOR-7 {symbols}{Style.RESET_ALL}")
    
    def laboratory_format(self, data: Dict[str, Any]) -> str:
        """Scientific laboratory style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        experiment = f"EXP-{session_num:03d}"
        ph_level = f"pH{random.uniform(6.5, 7.5):.1f}"
        temperature = f"{random.randint(20, 25)}°C"
        
        return (f"{Fore.WHITE}🔬 LAB-{model[:4]}{Style.RESET_ALL} "
                f"{Fore.CYAN}[{model} RESEARCH]{Style.RESET_ALL} "
                f"{Fore.GREEN}STATUS: {status}{Style.RESET_ALL} "
                f"{Fore.YELLOW}SUBJECT: {experiment}{Style.RESET_ALL} "
                f"{Fore.BLUE}SAMPLES: {msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}DATA: {tokens}{Style.RESET_ALL} "
                f"{Fore.RED}COST: ${cost:.2f}K{Style.RESET_ALL} "
                f"{Fore.CYAN}ENV: {temperature} {ph_level}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🧪 {folder} LAB{Style.RESET_ALL}")
    
    # NEW MEDICAL/HEALTH TEMPLATES
    
    def medical_format(self, data: Dict[str, Any]) -> str:
        """Medical system style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        patient_id = f"PT-{session_num:04d}"
        vital_status = "STABLE" if status == 'LIVE' else "CRITICAL"
        heart_rate = random.randint(60, 100)
        
        return (f"{Fore.RED}🏥 MEDICAL CENTER{Style.RESET_ALL} "
                f"{Fore.WHITE}[DR. {model}]{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.RED}● {vital_status}{Style.RESET_ALL} "
                f"{Fore.CYAN}ID: {patient_id}{Style.RESET_ALL} "
                f"{Fore.RED}♥ {heart_rate}BPM{Style.RESET_ALL} "
                f"{Fore.BLUE}VISITS: {msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}RECORDS: {tokens}{Style.RESET_ALL} "
                f"{Fore.YELLOW}BILL: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🚑 WARD-{folder[:3]}{Style.RESET_ALL}")
    
    def hospital_format(self, data: Dict[str, Any]) -> str:
        """Hospital management style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        room_num = f"R{session_num:03d}"
        bed_count = msgs
        capacity = f"{min(100, bed_count*2)}%"
        
        return (f"{Fore.BLUE}🏥 {folder.upper()} HOSPITAL{Style.RESET_ALL} "
                f"{Fore.WHITE}[{model} SYSTEM]{Style.RESET_ALL} "
                f"{Fore.GREEN if status == 'LIVE' else Fore.RED}OP-STATUS: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}ROOM: {room_num}{Style.RESET_ALL} "
                f"{Fore.YELLOW}BEDS: {bed_count}/∞{Style.RESET_ALL} "
                f"{Fore.MAGENTA}CAPACITY: {capacity}{Style.RESET_ALL} "
                f"{Fore.RED}RECORDS: {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}BUDGET: ${cost:.1f}K{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ SHIFT {time_left}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🩺 {cpu} {memory}{Style.RESET_ALL}")
    
    def pharmacy_format(self, data: Dict[str, Any]) -> str:
        """Pharmacy system style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        rx_number = f"RX{session_num:06d}"
        inventory = msgs * 10
        
        return (f"{Fore.GREEN}💊 CLAUDE PHARMACY{Style.RESET_ALL} "
                f"{Fore.WHITE}[{model} PharmD]{Style.RESET_ALL} "
                f"{Fore.CYAN}RX: {rx_number}{Style.RESET_ALL} "
                f"{Fore.BLUE}FILLED: {msgs}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}INVENTORY: {inventory}{Style.RESET_ALL} "
                f"{Fore.YELLOW}TOKENS: {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}COPAY: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.RED}⚠️ CHECK INTERACTIONS{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}📋 {folder} BRANCH{Style.RESET_ALL}")
    
    # NEW TRANSPORTATION TEMPLATES
    
    def aviation_format(self, data: Dict[str, Any]) -> str:
        """Aviation control tower style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        flight_num = f"CL{session_num:04d}"
        altitude = f"FL{msgs}00"
        heading = f"{session_num * 10 % 360:03d}°"
        
        return (f"{Fore.BLUE}✈️ {folder.upper()} TOWER{Style.RESET_ALL} "
                f"{Fore.WHITE}[{model} ATC]{Style.RESET_ALL} "
                f"{Fore.GREEN}STATUS: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}FLIGHT: {flight_num}{Style.RESET_ALL} "
                f"{Fore.YELLOW}ALT: {altitude}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}HDG: {heading}{Style.RESET_ALL} "
                f"{Fore.BLUE}SOULS: {msgs}{Style.RESET_ALL} "
                f"{Fore.RED}FUEL: {100-int(cost)}%{Style.RESET_ALL} "
                f"{Fore.GREEN}TOKENS: {tokens}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ ETA {time_left} | {current_time} UTC{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🛩️ RUNWAY 27L{Style.RESET_ALL}")
    
    def railway_format(self, data: Dict[str, Any]) -> str:
        """Railway control center style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        train_num = f"T{session_num:03d}"
        platform = random.randint(1, 12)
        speed = f"{random.randint(80, 200)}km/h"
        
        return (f"{Fore.YELLOW}🚂 {folder.upper()} CENTRAL{Style.RESET_ALL} "
                f"{Fore.WHITE}[{model} DISPATCHER]{Style.RESET_ALL} "
                f"{Fore.GREEN}SIGNAL: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}TRAIN: {train_num}{Style.RESET_ALL} "
                f"{Fore.BLUE}PLATFORM: {platform}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}SPEED: {speed}{Style.RESET_ALL} "
                f"{Fore.YELLOW}PASSENGERS: {msgs}{Style.RESET_ALL} "
                f"{Fore.RED}CARGO: {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}FARE: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ ARR {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🚃 EXPRESS LINE{Style.RESET_ALL}")
    
    def automotive_format(self, data: Dict[str, Any]) -> str:
        """Automotive dashboard style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        vehicle_id = f"VIN-{session_num:04d}"
        odometer = f"{msgs * 1000}km"
        fuel_level = f"{100-int(cost)}%"
        engine_temp = f"{random.randint(85, 95)}°C"
        
        return (f"{Fore.RED}🚗 {model} AUTO{Style.RESET_ALL} "
                f"{Fore.WHITE}[{folder.upper()} GARAGE]{Style.RESET_ALL} "
                f"{Fore.GREEN}ENGINE: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}ID: {vehicle_id}{Style.RESET_ALL} "
                f"{Fore.BLUE}ODO: {odometer}{Style.RESET_ALL} "
                f"{Fore.YELLOW}⛽ {fuel_level}{Style.RESET_ALL} "
                f"{Fore.RED}🌡️ {engine_temp}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}DATA: {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}SERVICE: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🔧 {cpu} {memory}{Style.RESET_ALL}")
    
    def maritime_format(self, data: Dict[str, Any]) -> str:
        """Maritime/Naval operations style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        vessel_name = f"MV-{folder.upper()[:6]}"
        coordinates = f"{session_num % 90}°{msgs % 60}'"
        depth = f"{random.randint(10, 50)}m"
        
        return (f"{Fore.BLUE}⚓ HARBOR CONTROL{Style.RESET_ALL} "
                f"{Fore.WHITE}[CAPT. {model}]{Style.RESET_ALL} "
                f"{Fore.GREEN}STATUS: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}VESSEL: {vessel_name}{Style.RESET_ALL} "
                f"{Fore.YELLOW}POS: {coordinates}N{Style.RESET_ALL} "
                f"{Fore.BLUE}DEPTH: {depth}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}CREW: {msgs}{Style.RESET_ALL} "
                f"{Fore.RED}CARGO: {tokens}T{Style.RESET_ALL} "
                f"{Fore.GREEN}PORT FEE: ${cost:.1f}K{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ TIDE {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🌊 {cpu} KNOTS{Style.RESET_ALL}")
    
    # NEW ENTERTAINMENT TEMPLATES
    
    def cinema_format(self, data: Dict[str, Any]) -> str:
        """Cinema/Movie theater style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        screen_num = f"SCREEN {session_num % 12 + 1}"
        movie_title = f"{model.upper()}: THE SESSION"
        rating = random.choice(["G", "PG", "PG-13", "R"])
        
        return (f"{Fore.YELLOW}🎬 {folder.upper()} CINEMA{Style.RESET_ALL} "
                f"{Fore.WHITE}[NOW SHOWING: {movie_title}]{Style.RESET_ALL} "
                f"{Fore.GREEN}STATUS: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}{screen_num}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}RATING: {rating}{Style.RESET_ALL} "
                f"{Fore.BLUE}SEATS: {msgs}/300{Style.RESET_ALL} "
                f"{Fore.YELLOW}RUNTIME: {tokens[:3]}min{Style.RESET_ALL} "
                f"{Fore.GREEN}TICKET: ${cost:.2f}{Style.RESET_ALL} "
                f"{Fore.RED}SHOWTIMES: {time_left}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🍿 CONCESSIONS OPEN{Style.RESET_ALL}")
    
    def music_format(self, data: Dict[str, Any]) -> str:
        """Music studio/Concert style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        track_num = f"TRK{session_num:02d}"
        bpm = random.randint(80, 140)
        key = random.choice(["C", "D", "E", "F", "G", "A", "B"]) + random.choice(["", "#", "♭"])
        
        return (f"{Fore.MAGENTA}🎵 {folder.upper()} STUDIO{Style.RESET_ALL} "
                f"{Fore.WHITE}[ARTIST: {model}]{Style.RESET_ALL} "
                f"{Fore.GREEN}REC: {status}{Style.RESET_ALL} "
                f"{Fore.CYAN}TRACK: {track_num}{Style.RESET_ALL} "
                f"{Fore.YELLOW}BPM: {bpm}{Style.RESET_ALL} "
                f"{Fore.BLUE}KEY: {key} MAJOR{Style.RESET_ALL} "
                f"{Fore.MAGENTA}TAKES: {msgs}{Style.RESET_ALL} "
                f"{Fore.RED}SAMPLES: {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}BUDGET: ${cost:.1f}K{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ SESSION {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🎧 {cpu} {memory}{Style.RESET_ALL}")
    
    def sports_format(self, data: Dict[str, Any]) -> str:
        """Sports broadcast/Stadium style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        team_name = f"{folder.upper()[:8]} FC"
        score = f"{session_num % 10}-{msgs % 10}"
        quarter = f"Q{session_num % 4 + 1}"
        
        return (f"{Fore.GREEN}⚽ {team_name}{Style.RESET_ALL} "
                f"{Fore.WHITE}[COACH: {model}]{Style.RESET_ALL} "
                f"{Fore.CYAN}GAME: {status}{Style.RESET_ALL} "
                f"{Fore.YELLOW}SCORE: {score}{Style.RESET_ALL} "
                f"{Fore.BLUE}PERIOD: {quarter}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}PLAYS: {msgs}{Style.RESET_ALL} "
                f"{Fore.RED}STATS: {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}REVENUE: ${cost:.1f}M{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ TIME {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}🏟️ HOME STADIUM{Style.RESET_ALL}")
    
    def news_format(self, data: Dict[str, Any]) -> str:
        """News broadcast/Newsroom style"""
        (model, status, msgs, tokens, cost, end_time, remaining, session_num, 
         git_branch, git_status, folder, cpu, memory, current_time, time_left) = self._get_data(data)
        
        edition = f"EDITION {session_num:02d}"
        story_count = msgs
        breaking = "🔴 BREAKING" if status == 'LIVE' else "📰 UPDATE"
        
        return (f"{Fore.RED}{breaking}{Style.RESET_ALL} "
                f"{Fore.WHITE}[ANCHOR: {model}]{Style.RESET_ALL} "
                f"{Fore.CYAN}{folder.upper()} NEWS{Style.RESET_ALL} "
                f"{Fore.YELLOW}{edition}{Style.RESET_ALL} "
                f"{Fore.BLUE}STORIES: {story_count}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}SOURCES: {tokens}{Style.RESET_ALL} "
                f"{Fore.GREEN}AD REVENUE: ${cost:.1f}K{Style.RESET_ALL} "
                f"{Fore.RED}RATINGS: {cpu}{Style.RESET_ALL} "
                f"{Fore.WHITE}⏰ LIVE {time_left} | {current_time}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}📡 ON AIR{Style.RESET_ALL}")