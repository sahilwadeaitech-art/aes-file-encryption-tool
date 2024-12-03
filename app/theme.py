"""
Application Theme & Design System
Color palette, typography, and styling constants for the UI.

Author: Sahil Wade
"""

# ─── Color Palette ────────────────────────────────────────────────────────────

# Base colors - deep space dark theme
BG_PRIMARY = "#0a0e1a"          # Deep space black
BG_SECONDARY = "#0f1424"        # Midnight navy
BG_TERTIARY = "#151b2e"         # Dark indigo
BG_CARD = "#1a2138"             # Card background
BG_CARD_HOVER = "#1f2844"       # Card hover state
BG_SURFACE = "#1e2640"          # Surface elements
BG_INPUT = "#131927"            # Input field background
BG_SIDEBAR = "#0c1020"          # Sidebar background

# Accent colors
ACCENT_PRIMARY = "#3b82f6"      # Electric blue
ACCENT_SECONDARY = "#6366f1"    # Indigo
ACCENT_TERTIARY = "#8b5cf6"     # Purple
ACCENT_CYAN = "#06b6d4"         # Cyan glow
ACCENT_BLUE_SOFT = "#60a5fa"    # Soft blue

# Text colors
TEXT_PRIMARY = "#f1f5f9"         # Primary text - clean white
TEXT_SECONDARY = "#94a3b8"      # Secondary text - muted
TEXT_TERTIARY = "#64748b"       # Tertiary text - dimmed
TEXT_ACCENT = "#93c5fd"         # Accent text - blue tint
TEXT_HEADING = "#e2e8f0"        # Heading text

# Status colors
STATUS_SUCCESS = "#10b981"      # Green - secure/success
STATUS_WARNING = "#f59e0b"      # Orange - warning
STATUS_ERROR = "#ef4444"        # Red - error/failed
STATUS_INFO = "#3b82f6"         # Blue - information

# Border and divider colors
BORDER_DEFAULT = "#1e293b"      # Default border
BORDER_SUBTLE = "#1a2332"       # Subtle border
BORDER_ACCENT = "#3b82f680"     # Accent border (with alpha)
BORDER_FOCUS = "#3b82f6"        # Focused element border

# Gradient stops (for labels/descriptions)
GRADIENT_START = "#3b82f6"
GRADIENT_MID = "#6366f1"
GRADIENT_END = "#8b5cf6"

# Shadow/glow effects (conceptual - applied via frame layering)
GLOW_BLUE = "#3b82f640"
GLOW_CYAN = "#06b6d430"
GLOW_PURPLE = "#8b5cf630"

# ─── Typography ───────────────────────────────────────────────────────────────

FONT_FAMILY = "Segoe UI"
FONT_FAMILY_MONO = "Consolas"

# Font sizes
FONT_SIZE_XS = 10
FONT_SIZE_SM = 11
FONT_SIZE_BASE = 12
FONT_SIZE_MD = 13
FONT_SIZE_LG = 15
FONT_SIZE_XL = 18
FONT_SIZE_2XL = 22
FONT_SIZE_3XL = 28
FONT_SIZE_HERO = 36

# Font weights (tuples for CTkFont)
FONT_REGULAR = (FONT_FAMILY, FONT_SIZE_BASE)
FONT_MEDIUM = (FONT_FAMILY, FONT_SIZE_MD, "bold")
FONT_BOLD = (FONT_FAMILY, FONT_SIZE_BASE, "bold")
FONT_HEADING = (FONT_FAMILY, FONT_SIZE_XL, "bold")
FONT_SUBHEADING = (FONT_FAMILY, FONT_SIZE_LG, "bold")
FONT_TITLE = (FONT_FAMILY, FONT_SIZE_2XL, "bold")
FONT_HERO = (FONT_FAMILY, FONT_SIZE_HERO, "bold")
FONT_MONO = (FONT_FAMILY_MONO, FONT_SIZE_BASE)
FONT_MONO_SM = (FONT_FAMILY_MONO, FONT_SIZE_SM)
FONT_CAPTION = (FONT_FAMILY, FONT_SIZE_XS)

# ─── Spacing ──────────────────────────────────────────────────────────────────

SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 12
SPACING_LG = 16
SPACING_XL = 24
SPACING_2XL = 32
SPACING_3XL = 48

# Padding
PAD_CARD = 20
PAD_SECTION = 24
PAD_SIDEBAR = 16
PAD_INPUT = 12

# Border radius
RADIUS_SM = 6
RADIUS_MD = 8
RADIUS_LG = 12
RADIUS_XL = 16
RADIUS_FULL = 50

# ─── Component Dimensions ─────────────────────────────────────────────────────

SIDEBAR_WIDTH = 220
SIDEBAR_COLLAPSED = 60
HEADER_HEIGHT = 56
CARD_MIN_HEIGHT = 120
BUTTON_HEIGHT = 38
INPUT_HEIGHT = 40
PROGRESS_HEIGHT = 6

# ─── Animation Timing (ms) ────────────────────────────────────────────────────

ANIM_FAST = 120
ANIM_NORMAL = 220
ANIM_SLOW = 380
ANIM_VERY_SLOW = 550

# ─── Navigation Items ─────────────────────────────────────────────────────────

NAV_ITEMS = [
    {"id": "dashboard", "label": "Dashboard", "icon": "◉"},
    {"id": "encrypt", "label": "Encrypt", "icon": "🔒"},
    {"id": "decrypt", "label": "Decrypt", "icon": "🔓"},
    {"id": "password", "label": "Password Gen", "icon": "🔑"},
    {"id": "history", "label": "History", "icon": "📋"},
    {"id": "settings", "label": "Settings", "icon": "⚙"},
]
