# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.2.x   | ✅ Active  |
| 1.1.x   | ⚠️ Limited |
| < 1.0   | ❌ EOL     |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, reach out directly via email or private message with:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact assessment
4. Suggested fix (if any)

I take security seriously and will respond within 48 hours.

## Cryptographic Details

This application uses industry-standard cryptographic primitives:

- **Encryption:** AES-256-GCM (authenticated encryption)
- **Key Derivation:** PBKDF2-HMAC-SHA256 with 600,000 iterations
- **Salt:** 256-bit random (per-file unique)
- **Nonce:** 96-bit random (per-file unique)
- **Library:** Python `cryptography` (backed by OpenSSL)

## Security Considerations

- All encryption/decryption is performed locally — no network calls
- Passwords are never stored or logged
- Derived keys exist only in memory during operation
- Original file hashes are computed for integrity verification
- The application does not implement its own cryptographic primitives

## Limitations

- Password strength is the user's responsibility
- No secure memory wiping (Python limitation)
- File metadata (size, timestamps) is not hidden from the OS
- This is an educational project — not audited for production use

## Disclaimer

This tool is designed for educational purposes and personal file protection.
It has not undergone a formal security audit. Use at your own discretion.
