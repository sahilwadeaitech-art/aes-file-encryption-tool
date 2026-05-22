# Security

## Crypto details

- **Encryption:** AES-256-GCM
- **Key derivation:** PBKDF2-HMAC-SHA256, 600,000 iterations
- **Salt:** 32 bytes random (unique per file)
- **Nonce:** 12 bytes random (unique per file)
- **Library:** Python `cryptography` (OpenSSL backend)

No custom crypto. Everything uses standard primitives.

## What this does right

- All processing is local, no network calls
- Passwords are never stored or logged
- Keys only exist in memory during the operation
- GCM mode provides both encryption and integrity checking
- Per-file unique salt and nonce

## Limitations

- Password strength is on you
- Python can't guarantee secure memory wiping
- File metadata (size, timestamps) is still visible to the OS
- Loads entire file into memory — not great for huge files
- **Not audited** — this is a personal/educational project

## Reporting issues

If you find a real security bug, please don't open a public issue. Reach out directly and I'll look into it.

## Disclaimer

This is an educational project. I use proper crypto primitives but I'm not claiming this is production-grade security software. Use at your own risk.
