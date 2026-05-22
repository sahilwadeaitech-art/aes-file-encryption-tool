"""
AES File Encryption Utility — main entry point.
"""

import sys
import os
import logging
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Launch the app."""
    logger.info("Starting AES File Encryption Utility v1.2.0")

    try:
        from app.main_window import MainWindow

        app = MainWindow()
        app.mainloop()

    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print(f"\n[ERROR] Missing dependency: {e}")
        print("Run: pip install -r requirements.txt\n")
        sys.exit(1)

    except Exception as e:
        logger.critical(f"Application crashed: {e}", exc_info=True)
        print(f"\n[FATAL] Application error: {e}")
        sys.exit(1)

    logger.info("Application closed")


if __name__ == "__main__":
    main()
