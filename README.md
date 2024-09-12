# 🛡️ AES File Encryption Utility

A modern desktop application for secure local file encryption using AES-256-GCM.
Built with Python, CustomTkinter, and the `cryptography` library.

![Dashboard Overview](screenshots/dashboard-overview.png)

---

## Overview

This is a practical encryption tool designed for secure local file protection. It provides a clean, modern interface for encrypting and decrypting files using industry-standard AES-256 with authenticated encryption (GCM mode).

The project combines modern Python desktop engineering with cryptographic best practices — built as both a learning exercise in encryption engineering and a genuinely useful security utility.

**Key principles:**
- Everything runs locally — no network calls, no telemetry
- Industry-standard cryptography (no custom primitives)
- Clean, maintainable codebase
- Modern UI that doesn't feel like a terminal emulator

---

## Features

### 🔒 AES-256-GCM Encryption
- Authenticated encryption with integrity verification
- PBKDF2-SHA256 key derivation (600K iterations)
- Per-file unique salt and nonce generation
- Custom file format with version headers

### 🔓 Secure Decryption
- Password-based file restoration
- Automatic integrity checking
- Original filename preservation
- Clear error handling for wrong passwords

### 🔑 Password Generator
- Cryptographically secure random generation
- Configurable length and character sets
- Real-time entropy calculation
- Strength assessment visualization
- One-click clipboard copy

### 📊 Dashboard
- Operation statistics at a glance
- Recent activity timeline
- Quick action shortcuts
- Security status overview

### 📋 Encryption History
- Complete operation log with timestamps
- Success/failure tracking
- File size and duration metrics
- Filterable and clearable

---

## Screenshots

| Dashboard | Encryption | Password Generator |
|-----------|-----------|-------------------|
| ![Dashboard](screenshots/dashboard-overview.png) | ![Encrypt](screenshots/encryption-workflow.png) | ![Password](screenshots/password-generator.png) |

---

## Installation

### Requirements
- Python 3.11 or higher
- Windows 10/11 (primary), macOS, or Linux

### Setup

```bash
# Clone the repository
git clone https://github.com/sahilwadeaitech-art/aes-file-encryption-tool.git
cd aes-file-encryption-tool

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `customtkinter` | Modern UI framework |
| `cryptography` | AES-256-GCM encryption |
| `Pillow` | Image handling for UI assets |

---

## Usage

### Encrypting a File

1. Navigate to the **Encrypt** page
2. Click the drop zone or browse to select a file
3. Enter a strong password (and confirm it)
4. Click **Encrypt File**
5. The encrypted file is saved alongside the original with a `.enc` extension

### Decrypting a File

1. Navigate to the **Decrypt** page
2. Select an encrypted `.enc` file
3. Enter the password used during encryption
4. Choose an output directory (defaults to the file's location)
5. Click **Decrypt File**

### Generating Passwords

1. Navigate to the **Password Gen** page
2. Adjust length and character options
3. Click **Generate** for a new password
4. Click **Copy** to copy to clipboard
5. Use entropy/strength indicators to assess quality

---

## Project Structure

```
aes-file-encryption-tool/
│
├── app/                    # UI application layer
│   ├── main_window.py     # Primary window controller
│   ├── components.py      # Reusable UI components
│   └── theme.py           # Design system & color palette
│
├── core/                   # Cryptographic core
│   ├── encryption.py      # AES-256-GCM engine
│   └── password_generator.py  # Secure password generation
│
├── modules/                # Utility modules
│   └── file_utils.py      # File operations & validation
│
├── database/               # Data persistence
│   └── history.py         # SQLite operation history
│
├── assets/                 # Static assets
│   ├── icons/
│   ├── banner/
│   └── ui/
│
├── screenshots/            # Application screenshots
├── docs/                   # Additional documentation
├── tests/                  # Test suite
├── logs/                   # Application logs (gitignored)
├── reports/                # Generated reports (gitignored)
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── CHANGELOG.md            # Version history
├── CONTRIBUTING.md         # Contribution guidelines
├── SECURITY.md             # Security policy & details
└── .gitignore
```

---

## Technical Details

### Encryption Scheme

```
Algorithm:       AES-256-GCM (Galois/Counter Mode)
Key Derivation:  PBKDF2-HMAC-SHA256
Iterations:      600,000
Salt:            256-bit (random, per-file)
Nonce:           96-bit (random, per-file)
Authentication:  GCM tag (128-bit)
```

### File Format

Encrypted files use a custom binary format:

```
[8B magic: "AESUTIL1"] [1B version] [32B salt] [12B nonce]
[4B filename_len] [NB filename] [ciphertext + GCM tag]
```

This allows the utility to verify file validity and restore original filenames during decryption.

---

## Roadmap

Planned features for future releases:

- [ ] Batch encryption (multi-file operations)
- [ ] Secure file shredding (overwrite before delete)
- [ ] Exportable audit reports (PDF/HTML)
- [ ] Cloud backup integration (encrypted sync)
- [ ] Advanced analytics dashboard
- [ ] Linux compatibility improvements
- [ ] Drag-and-drop from system file explorer
- [ ] Custom encryption profiles/presets

---

## Limitations

- Large files (>500MB) may be slow due to in-memory processing
- No streaming encryption yet (planned for batch operations)
- Passwords cannot be recovered — if forgotten, the file is unrecoverable
- Not formally audited — use for personal/educational purposes
- Python's memory model doesn't guarantee secure key wiping

---

## Disclaimer

This project is intended for **educational purposes** and **secure local file protection** workflows only.

It is not designed for, and should not be used for, any malicious purpose including but not limited to ransomware, unauthorized access to others' data, or circumvention of security controls.

The author takes no responsibility for misuse.

---

## Developer

Built and maintained by **Sahil Wade**.

This project started as a way to learn practical cryptographic engineering and modern desktop UI development. It's grown into a useful personal tool that I continue to refine.

If you find it useful or have suggestions, feel free to open an issue or contribute.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
