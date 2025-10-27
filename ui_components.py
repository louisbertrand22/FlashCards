"""
UI components and utilities for the Flashcard application.
Provides colors, formatting, and visual enhancements for CLI.
"""
import os
import sys


class Colors:
    """ANSI color codes for terminal output."""
    
    # Basic colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @staticmethod
    def is_supported():
        """Check if terminal supports colors."""
        # Check if output is a terminal
        if not hasattr(sys.stdout, 'isatty'):
            return False
        if not sys.stdout.isatty():
            return False
        # Check if running on Windows without colorama
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except:
                return False
        return True


class UI:
    """UI utilities for enhanced display."""
    
    def __init__(self):
        """Initialize UI with color support detection."""
        self.colors_enabled = Colors.is_supported()
    
    def colorize(self, text, color):
        """Apply color to text if colors are supported."""
        if self.colors_enabled:
            return f"{color}{text}{Colors.RESET}"
        return text
    
    def success(self, text):
        """Format text as success message."""
        return self.colorize(f"✓ {text}", Colors.BRIGHT_GREEN)
    
    def error(self, text):
        """Format text as error message."""
        return self.colorize(f"✗ {text}", Colors.BRIGHT_RED)
    
    def warning(self, text):
        """Format text as warning message."""
        return self.colorize(f"⚠ {text}", Colors.BRIGHT_YELLOW)
    
    def info(self, text):
        """Format text as info message."""
        return self.colorize(f"ℹ {text}", Colors.BRIGHT_CYAN)
    
    def bold(self, text):
        """Make text bold."""
        if self.colors_enabled:
            return f"{Colors.BOLD}{text}{Colors.RESET}"
        return text
    
    def dim(self, text):
        """Make text dim."""
        if self.colors_enabled:
            return f"{Colors.DIM}{text}{Colors.RESET}"
        return text
    
    def header(self, text, width=60):
        """Create a header with borders."""
        border = "=" * width
        title = text.center(width)
        return f"\n{self.colorize(border, Colors.BRIGHT_CYAN)}\n{self.colorize(self.bold(title), Colors.BRIGHT_CYAN)}\n{self.colorize(border, Colors.BRIGHT_CYAN)}\n"
    
    def subheader(self, text, width=60):
        """Create a subheader with lighter borders."""
        border = "-" * width
        return f"\n{self.colorize(border, Colors.CYAN)}\n{self.colorize(self.bold(text), Colors.BRIGHT_WHITE)}\n{self.colorize(border, Colors.CYAN)}"
    
    def separator(self, width=60):
        """Create a visual separator."""
        return self.colorize("-" * width, Colors.DIM)
    
    def difficulty_badge(self, difficulty_name):
        """Create a colored badge for difficulty level."""
        badges = {
            'EASY': ('🟢 EASY', Colors.BRIGHT_GREEN),
            'MEDIUM': ('🟡 MEDIUM', Colors.BRIGHT_YELLOW),
            'HARD': ('🔴 HARD', Colors.BRIGHT_RED)
        }
        badge_text, color = badges.get(difficulty_name, (difficulty_name, Colors.WHITE))
        return self.colorize(self.bold(badge_text), color)
    
    def progress_bar(self, current, total, width=30):
        """Create a progress bar."""
        if total == 0:
            return ""
        
        percentage = current / total
        filled = int(width * percentage)
        bar = "█" * filled + "░" * (width - filled)
        percent_text = f"{int(percentage * 100)}%"
        
        if self.colors_enabled:
            bar_colored = f"{Colors.BRIGHT_GREEN}{bar}{Colors.RESET}"
            return f"[{bar_colored}] {percent_text}"
        return f"[{bar}] {percent_text}"
    
    def menu_option(self, number, text, icon=""):
        """Format a menu option."""
        if icon:
            formatted = f"[{self.colorize(str(number), Colors.BRIGHT_CYAN)}] {icon} {text}"
        else:
            formatted = f"[{self.colorize(str(number), Colors.BRIGHT_CYAN)}] {text}"
        return formatted
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def prompt(self, text, default=None):
        """Create a colored prompt."""
        prompt_text = self.colorize("➤ ", Colors.BRIGHT_CYAN) + text
        if default:
            prompt_text += self.colorize(f" [default: {default}]", Colors.DIM)
        return prompt_text + ": "
    
    def stat_line(self, label, value, color=Colors.BRIGHT_WHITE):
        """Format a statistics line."""
        label_colored = self.colorize(f"{label}:", Colors.CYAN)
        value_colored = self.colorize(str(value), color)
        return f"  {label_colored} {value_colored}"


# Create a global UI instance
ui = UI()
