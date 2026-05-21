# Contributing

Thanks for your interest in contributing to the AES File Encryption Utility.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Test thoroughly
7. Commit with a clear message
8. Push and open a Pull Request

## Development Setup

```bash
# Clone
git clone https://github.com/your-username/aes-file-encryption-tool.git
cd aes-file-encryption-tool

# Virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Code Style

- Follow PEP 8 conventions
- Use type hints where practical
- Keep functions focused and well-documented
- Write clear docstrings for public functions
- Use meaningful variable names

## Commit Messages

Use clear, descriptive commit messages:

```
feat: add batch encryption support
fix: resolve file path handling on Windows
refactor: simplify key derivation logic
docs: update installation instructions
style: improve dashboard card spacing
```

## What to Contribute

Useful contributions include:

- Bug fixes
- Performance improvements
- UI/UX improvements
- Documentation clarity
- Cross-platform compatibility fixes
- Test coverage

## What to Avoid

- Breaking changes without discussion
- Adding unnecessary dependencies
- Offensive security features or exploit code
- Changes that compromise security guarantees

## Questions?

Open an issue for discussion before starting significant changes.
