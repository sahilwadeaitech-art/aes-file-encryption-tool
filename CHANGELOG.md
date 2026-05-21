# Changelog

All notable changes to this project will be documented here.

## [1.2.0] - 2025-01-15

### Added
- Password generator with entropy display and strength visualization
- Encryption history page with filterable table view
- Daily statistics tracking in SQLite
- Settings page with algorithm details

### Improved
- Dashboard card hover animations
- Sidebar navigation transitions
- File validation error messages
- Progress bar visual feedback

### Fixed
- File path handling on Windows
- Output directory auto-detection during decryption
- History table truncation for long filenames

---

## [1.1.0] - 2024-11-20

### Added
- Dashboard overview with quick action buttons
- Recent activity timeline on dashboard
- Security status display
- File drop zone component with click-to-browse
- Operation duration tracking

### Improved
- Sidebar design and brand section
- Card component border styling
- Color palette refinements (softer accent tones)
- Typography hierarchy consistency

### Fixed
- Progress callback thread safety
- Database initialization on first run
- Encrypted file header validation

---

## [1.0.0] - 2024-09-08

### Added
- AES-256-GCM file encryption and decryption
- PBKDF2-SHA256 key derivation (600K iterations)
- Modern dark-theme UI with CustomTkinter
- Sidebar navigation system
- Encrypt page with file selection and password input
- Decrypt page with output directory selection
- File integrity verification (SHA-256)
- SQLite operation history database
- Threaded encryption/decryption (non-blocking UI)
- Application logging system

### Technical
- Custom file format with magic bytes and version header
- Per-file unique salt and nonce generation
- GCM authenticated encryption (integrity + confidentiality)
- Modular project structure (core, app, database, modules)

---

## [0.2.0] - 2024-07-14

### Added
- Basic CustomTkinter window setup
- File selection dialog
- Simple password input
- Initial encryption logic (prototype)

---

## [0.1.0] - 2024-06-01

### Added
- Initial project scaffolding
- Basic AES encryption proof of concept
- Requirements and project structure
