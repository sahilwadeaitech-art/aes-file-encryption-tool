"""
File utility helpers — validation, formatting, path generation.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Tuple


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} B"
    return f"{size:.1f} {units[unit_index]}"


def get_file_info(filepath: str) -> Optional[dict]:
    """Get file metadata."""
    path = Path(filepath)
    if not path.exists():
        return None
    
    stat = path.stat()
    return {
        "name": path.name,
        "stem": path.stem,
        "extension": path.suffix,
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "path": str(path.resolve()),
        "parent": str(path.parent),
        "is_file": path.is_file(),
        "modified": stat.st_mtime
    }


def validate_file_for_encryption(filepath: str) -> Tuple[bool, str]:
    """Check if a file can be encrypted. Returns (ok, message)."""
    path = Path(filepath)
    
    if not path.exists():
        return False, "File does not exist"
    
    if not path.is_file():
        return False, "Path is not a file"
    
    if path.stat().st_size == 0:
        return False, "File is empty"
    
    # Warn about very large files (>500MB)
    if path.stat().st_size > 500 * 1024 * 1024:
        return True, "Warning: Large file — encryption may take longer"
    
    # Check if already encrypted by this tool
    if path.suffix == ".enc":
        return False, "File appears to already be encrypted"
    
    return True, "File is ready for encryption"


def validate_file_for_decryption(filepath: str) -> Tuple[bool, str]:
    """Check if a file can be decrypted. Returns (ok, message)."""
    path = Path(filepath)
    
    if not path.exists():
        return False, "File does not exist"
    
    if not path.is_file():
        return False, "Path is not a file"
    
    if path.stat().st_size < 60:
        return False, "File too small to be a valid encrypted file"
    
    # Check magic bytes
    try:
        with open(filepath, "rb") as f:
            magic = f.read(8)
            if magic != b"AESUTIL1":
                return False, "Not a valid encrypted file (unrecognized format)"
    except IOError:
        return False, "Cannot read file"
    
    return True, "File is ready for decryption"


def generate_output_path(input_path: str, operation: str = "encrypt") -> str:
    """Generate an output file path for the encrypted/decrypted file."""
    path = Path(input_path)
    
    if operation == "encrypt":
        return str(path.with_suffix(path.suffix + ".enc"))
    elif operation == "decrypt":
        if path.suffix == ".enc":
            return str(path.with_suffix(""))
        return str(path.parent / f"decrypted_{path.name}")


def ensure_directory(dirpath: str) -> bool:
    """Ensure a directory exists, create if needed."""
    try:
        os.makedirs(dirpath, exist_ok=True)
        return True
    except OSError:
        return False


def get_available_space(path: str) -> int:
    """Get available disk space in bytes at the given path."""
    try:
        usage = shutil.disk_usage(path)
        return usage.free
    except OSError:
        return 0
