# Encrypted File Format

## Layout (v1)

```
Offset  Size   Field
------  -----  -----
0       8B     Magic: "AESUTIL1"
8       1B     Version (1)
9       32B    Salt
41      12B    Nonce
53      4B     Filename length (uint32 LE)
57      NB     Original filename (UTF-8)
57+N    ...    Ciphertext + 16B GCM tag
```

## Key Derivation

PBKDF2-HMAC-SHA256, 600K iterations, 32-byte salt → 32-byte key.

## Encryption

AES-256-GCM with 12-byte random nonce. The GCM tag (16 bytes) is appended to the ciphertext automatically by the `cryptography` library.

## Known Limitations

- No AAD (associated data) used currently
- Whole file loaded into memory (no streaming)
- Python doesn't guarantee secure memory erasure of the key
