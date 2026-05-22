"""
Theme constants — colors, fonts, spacing, dimensions.
"""

# ─── Colors ────────────────────────────────────────────────────────────────────

# Backgrounds
BG_PRIMARY = "#0a0e1a"
BG_SECONDARY = "#0f1424"
BG_TERTIARY = "#151b2e"
BG_CARD = "#1a2138"
BG_CARD_HOVER = "#1f2844"
BG_SURFACE = "#1e2640"
BG_INPUT = "#131927"
BG_SIDEBAR = "#0c1020"

# Accents
ACCENT_PRIMARY = "#3b82f6"
ACCENT_SECONDARY = "#6366f1"
ACCENT_TERTIARY = "#8b5cf6"
ACCENT_CYAN = "#06b6d4"
ACCENT_BLUE_SOFT = "#60a5fa"

# Text
TEXT_PRIMARY = "#f1f5f9"
TEXT_SECONDARY = "#94a3b8"
TEXT_TERTIARY = "#64748b"
TEXT_ACCENT = "#93c5fd"
TEXT_HEADING = "#e2e8f0"

# Status
STATUS_SUCCESS = "#10b981"
STATUS_WARNING = "#f59e0b"
STATUS_ERROR = "#ef4444"
STATUS_INFO = "#3b82f6"

# Borders
BORDER_DEFAULT = "#1e293b"
BORDER_SUBTLE = "#1a2332"
BORDER_ACCENT = "#3b82f680"  # not used in tk directly, just reference
BORDER_FOCUS = "#3b82f6"

# Gradients (reference only, not usable in tk as-is)
GRADIENT_START = "#3b82f6"
GRADIENT_MID = "#6366f1"
GRADIENT_END = "#8b5cf6"

# Glow colors (conceptual, used for layered frame effects)
GLOW_BLUE = "#3b82f640"
GLOW_CYAN = "#06b6d430"
GLOW_PURPLE = "#8b5cf630"

# ─── Fonts ─────────────────────────────────────────────────────────────────────

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

# Font weights (CTkFont tuples)
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

# ─── Layout ────────────────────────────────────────────────────────────────────

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

# ─── Dimensions ────────────────────────────────────────────────────────────────

SIDEBAR_WIDTH = 220
SIDEBAR_COLLAPSED = 60
HEADER_HEIGHT = 56
CARD_MIN_HEIGHT = 120
BUTTON_HEIGHT = 38
INPUT_HEIGHT = 40
PROGRESS_HEIGHT = 6

# ─── Animations (ms) ──────────────────────────────────────────────────────────

ANIM_FAST = 120
ANIM_NORMAL = 220
ANIM_SLOW = 380
ANIM_VERY_SLOW = 550

# ─── Nav ───────────────────────────────────────────────────────────────────────

NAV_ITEMS = [
    {"id": "dashboard", "label": "Dashboard", "icon": "◉"},
    {"id": "encrypt", "label": "Encrypt", "icon": "🔒"},
    {"id": "decrypt", "label": "Decrypt", "icon": "🔓"},
    {"id": "password", "label": "Password Gen", "icon": "🔑"},
    {"id": "history", "label": "History", "icon": "📋"},
    {"id": "settings", "label": "Settings", "icon": "⚙"},
]
