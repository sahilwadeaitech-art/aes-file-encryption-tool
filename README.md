# AES File Encryption Utility

Desktop file encryption tool using AES-256-GCM. Built with Python and CustomTkinter.

![Dashboard](screenshots/dashboard-overview.png)

## What is this?

A local file encryption app with a proper UI. I wanted something that:
- Encrypts files with AES-256 (GCM mode, authenticated)
- Has a usable interface instead of just a CLI
- Tracks what I've encrypted/decrypted
- Generates strong passwords when I need them

Everything happens locally. No network calls, no cloud, no telemetry.

## Features

- **File encryption/decryption** — AES-256-GCM with PBKDF2 key derivation (600K iterations)
- **Password generator** — configurable length, charset, shows entropy
- **Operation history** — SQLite-backed log of all encrypt/decrypt operations
- **Dashboard** — quick stats and recent activity
- **Dark UI** — custom theme, sidebar nav, card-based layout

## Tech Stack

- Python 3.11+
- CustomTkinter (UI)
- `cryptography` library (AES-256-GCM, PBKDF2)
- SQLite (history tracking)
- Threading (non-blocking encryption)

## Setup

```bash
git clone https://github.com/sahilwadeaitech-art/aes-file-encryption-tool.git
cd aes-file-encryption-tool

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

## How it works

1. Pick a file to encrypt
2. Set a password
3. File gets encrypted with AES-256-GCM → outputs a `.enc` file
4. To decrypt, select the `.enc` file and enter the same password

The encrypted file format stores a version header, random salt, nonce, and the original filename so decryption can restore it properly.

## Project Structure

```
app/            — UI (main window, components, theme)
core/           — encryption engine, password generator
database/       — SQLite history tracking
modules/        — file utilities, report generation
docs/           — encryption format spec
tests/          — pytest suite
```

## Encryption Details

- AES-256-GCM (authenticated encryption)
- PBKDF2-HMAC-SHA256 key derivation, 600K iterations
- 32-byte random salt per file
- 12-byte random nonce per file
- Custom binary file format (magic bytes + versioned header)

More details in [docs/encryption-spec.md](docs/encryption-spec.md).

## Screenshots

*Screenshots coming — need to grab some fresh ones after the latest UI update.*

## TODO / Future

- [ ] Batch encrypt multiple files at once
- [ ] Secure file shredding (overwrite before delete)
- [ ] Export history as report
- [ ] Better large file handling (streaming)
- [ ] Drag and drop from explorer
- [ ] Linux font fallbacks

## Disclaimer

This is for personal/educational use. It's not audited, and I'm not a cryptographer — I just use standard primitives from the `cryptography` library correctly (I hope). Don't rely on this for anything critical without understanding the limitations.

## License

MIT
