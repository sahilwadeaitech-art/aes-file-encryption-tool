# Encryption Specification

## File Format (v1)

```
Offset  Size   Field
------  -----  -----
0       8B     Magic bytes: "AESUTIL1"
8       1B     Format version (currently 1)
9       32B    Salt (random, unique per file)
41      12B    Nonce (random, unique per file)
53      4B     Original filename length (little-endian uint32)
57      NB     Original filename (UTF-8 encoded)
57+N    ...    Ciphertext + GCM authentication tag (16B)
```

## Key Derivation

- **Function:** PBKDF2-HMAC-SHA256
- **Iterations:** 600,000 (aligned with OWASP 2023 recommendations)
- **Salt length:** 256 bits
- **Output key length:** 256 bits

## Encryption

- **Algorithm:** AES-256 in GCM mode
- **Nonce:** 96 bits (randomly generated)
- **Authentication:** GCM provides authenticated encryption
- **Tag size:** 128 bits (appended to ciphertext by AESGCM)

## Security Properties

1. **Confidentiality** — AES-256 provides computational security
2. **Integrity** — GCM tag detects any modification
3. **Authentication** — GCM authenticates the ciphertext
4. **Key uniqueness** — Random salt ensures unique keys per file
5. **Nonce uniqueness** — Random nonce per operation

## Limitations

- No associated data (AAD) is currently used
- Entire file is loaded into memory for encryption
- No streaming/chunked encryption for large files
- Python does not guarantee secure memory erasure
