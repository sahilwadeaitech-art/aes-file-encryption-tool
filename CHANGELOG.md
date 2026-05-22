# Changelog

## v1.2.0 (Jan 2025)

- Added password generator page (entropy display, strength meter, copy to clipboard)
- Encryption history page with table view and clear button
- Daily stats tracking in the database
- Settings page showing algorithm info
- Improved card hover effects
- Fixed Windows path issues during decryption
- Fixed history table cutting off long filenames

## v1.1.0 (Nov 2024)

- Dashboard with stats cards and quick actions
- Recent activity timeline
- File drop zone (click to browse, shows file info)
- Operation duration tracking
- Reworked sidebar styling
- Fixed threading issue with progress callbacks
- Fixed db init crash on first launch

## v1.0.0 (Sep 2024)

First proper release. Core functionality working:
- AES-256-GCM encrypt/decrypt with PBKDF2 key derivation
- Dark theme UI with sidebar navigation
- Encrypt and decrypt pages
- SQLite history logging
- File integrity checks (SHA-256)
- Threaded operations so UI doesn't freeze

## v0.2.0 (Jul 2024)

Early prototype. Basic window with file picker and password field. Encryption worked but UI was rough.

## v0.1.0 (Jun 2024)

Initial scaffolding. Got the encryption logic working in a script, started figuring out CustomTkinter.
