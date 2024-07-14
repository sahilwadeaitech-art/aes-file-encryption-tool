"""
Secure Password Generator
Cryptographically secure random password generation with entropy calculation.

Author: Sahil Wade
"""

import math
import secrets
import string
from typing import Optional
from dataclasses import dataclass


@dataclass
class PasswordResult:
    """Result of password generation with metadata."""
    password: str
    entropy: float
    strength: str
    length: int
    charset_size: int


# Character sets
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"
AMBIGUOUS = "il1Lo0O"


def calculate_entropy(length: int, charset_size: int) -> float:
    """Calculate password entropy in bits."""
    if charset_size <= 0 or length <= 0:
        return 0.0
    return length * math.log2(charset_size)


def assess_strength(entropy: float) -> str:
    """Assess password strength based on entropy."""
    if entropy >= 128:
        return "Excellent"
    elif entropy >= 80:
        return "Strong"
    elif entropy >= 60:
        return "Good"
    elif entropy >= 40:
        return "Fair"
    else:
        return "Weak"


def generate_password(
    length: int = 20,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
    custom_chars: Optional[str] = None
) -> PasswordResult:
    """
    Generate a cryptographically secure random password.
    
    Args:
        length: Password length (minimum 4)
        use_uppercase: Include uppercase letters
        use_lowercase: Include lowercase letters
        use_digits: Include digits
        use_symbols: Include special characters
        exclude_ambiguous: Exclude ambiguous characters (i, l, 1, L, o, 0, O)
        custom_chars: Optional custom character set (overrides other options)
    
    Returns:
        PasswordResult with password, entropy, and strength info
    """
    if length < 4:
        length = 4

    # Build character set
    if custom_chars:
        charset = custom_chars
    else:
        charset = ""
        if use_lowercase:
            charset += LOWERCASE
        if use_uppercase:
            charset += UPPERCASE
        if use_digits:
            charset += DIGITS
        if use_symbols:
            charset += SYMBOLS

        if not charset:
            charset = LOWERCASE + DIGITS

        if exclude_ambiguous:
            charset = "".join(c for c in charset if c not in AMBIGUOUS)

    # Generate password ensuring at least one char from each selected category
    charset_list = list(set(charset))
    charset_size = len(charset_list)

    # Generate random password
    password_chars = [secrets.choice(charset_list) for _ in range(length)]

    # Ensure minimum category representation (if not using custom chars)
    if not custom_chars and length >= 4:
        required = []
        if use_lowercase:
            required.append(LOWERCASE)
        if use_uppercase:
            required.append(UPPERCASE)
        if use_digits:
            required.append(DIGITS)
        if use_symbols:
            required.append(SYMBOLS)

        # Replace random positions with required characters
        positions = list(range(length))
        secrets.SystemRandom().shuffle(positions)

        for i, category in enumerate(required[:length]):
            filtered = category
            if exclude_ambiguous:
                filtered = "".join(c for c in category if c not in AMBIGUOUS)
            if filtered:
                password_chars[positions[i]] = secrets.choice(filtered)

    password = "".join(password_chars)
    entropy = calculate_entropy(length, charset_size)
    strength = assess_strength(entropy)

    return PasswordResult(
        password=password,
        entropy=round(entropy, 1),
        strength=strength,
        length=length,
        charset_size=charset_size
    )


def generate_passphrase(
    word_count: int = 5,
    separator: str = "-",
    capitalize: bool = True
) -> PasswordResult:
    """
    Generate a random passphrase from a wordlist.
    
    Uses a built-in list of common English words for memorable passphrases.
    """
    # Compact wordlist (EFF-inspired short list subset)
    words = [
        "anchor", "apple", "arrow", "basin", "blade", "bloom", "brave",
        "brisk", "cabin", "cedar", "chain", "chase", "cider", "cliff",
        "cloud", "coral", "crane", "crisp", "crown", "delta", "drift",
        "ember", "fable", "flame", "forge", "frost", "gleam", "globe",
        "grace", "grain", "grove", "haven", "hazel", "heron", "ivory",
        "lance", "latch", "lunar", "maple", "marsh", "medal", "mirth",
        "noble", "ocean", "olive", "orbit", "pearl", "phase", "piano",
        "plume", "prism", "quail", "raven", "ridge", "robin", "rover",
        "sage", "shard", "sigma", "slate", "solar", "spire", "steel",
        "stone", "storm", "swift", "thorn", "tiger", "torch", "trail",
        "tulip", "umbra", "vault", "vigor", "vivid", "warden", "wheat",
        "willow", "zenith", "birch", "blaze", "brook", "cairn", "chess",
        "climb", "coast", "dawn", "depth", "eagle", "earth", "field",
        "flint", "glade", "hawk", "helm", "jade", "knoll", "linen",
        "lotus", "mesa", "north", "oaken", "palm", "petal", "quartz",
        "river", "rustic", "shore", "silk", "spark", "summit", "terra",
        "thyme", "tower", "unity", "vale", "waves", "wind", "wren"
    ]

    chosen = [secrets.choice(words) for _ in range(word_count)]

    if capitalize:
        chosen = [w.capitalize() for w in chosen]

    passphrase = separator.join(chosen)

    # Entropy: log2(wordlist_size) * word_count
    entropy = word_count * math.log2(len(words))
    strength = assess_strength(entropy)

    return PasswordResult(
        password=passphrase,
        entropy=round(entropy, 1),
        strength=strength,
        length=len(passphrase),
        charset_size=len(words)
    )
