"""
AES-256-GCM file encryption/decryption.

Uses PBKDF2 for key derivation and a custom binary format
for storing encrypted files with metadata.
"""

import os
import struct
import hashlib
import logging
from pathlib import Path
from typing import Tuple, Optional, Callable

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

# Constants
SALT_SIZE = 32
NONCE_SIZE = 12
KEY_SIZE = 32  # 256 bits
ITERATIONS = 600_000  # OWASP 2023 recommendation for PBKDF2-SHA256
CHUNK_SIZE = 64 * 1024  # 64KB chunks for streaming
MAGIC_BYTES = b"AESUTIL1"  # File format identifier
VERSION = 1


class EncryptionError(Exception):
    """Raised when encryption fails."""
    pass


class DecryptionError(Exception):
    """Raised when decryption fails (wrong password, corrupted file, etc.)."""
    pass


class IntegrityError(Exception):
    """Raised when file integrity check fails."""
    pass


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from password + salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode("utf-8"))


def compute_file_hash(filepath: str) -> str:
    """Compute SHA-256 hash of a file for integrity verification."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()


def encrypt_file(
    input_path: str,
    output_path: str,
    password: str,
    progress_callback: Optional[Callable[[float], None]] = None
) -> dict:
    """
    Encrypt a file with AES-256-GCM.
    
    Output format:
        [8B magic][1B version][32B salt][12B nonce]
        [4B filename_len][filename][ciphertext + GCM tag]
    """
    try:
        input_file = Path(input_path)
        if not input_file.exists():
            raise EncryptionError(f"Input file not found: {input_path}")

        file_size = input_file.stat().st_size
        if file_size == 0:
            raise EncryptionError("Cannot encrypt empty file")

        # Generate cryptographic parameters
        salt = os.urandom(SALT_SIZE)
        nonce = os.urandom(NONCE_SIZE)
        key = derive_key(password, salt)

        # Compute original file hash for integrity
        original_hash = compute_file_hash(input_path)

        # Read plaintext (streaming for large files would need chunked AEAD)
        with open(input_path, "rb") as f:
            plaintext = f.read()

        if progress_callback:
            progress_callback(0.3)

        # Encrypt with AES-256-GCM
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        if progress_callback:
            progress_callback(0.7)

        # Encode original filename
        original_name = input_file.name.encode("utf-8")
        name_length = struct.pack("<I", len(original_name))

        # Write encrypted file
        with open(output_path, "wb") as f:
            f.write(MAGIC_BYTES)
            f.write(struct.pack("<B", VERSION))
            f.write(salt)
            f.write(nonce)
            f.write(name_length)
            f.write(original_name)
            f.write(ciphertext)

        if progress_callback:
            progress_callback(1.0)

        output_size = Path(output_path).stat().st_size

        logger.info(f"Encrypted: {input_path} -> {output_path} ({file_size} -> {output_size} bytes)")

        return {
            "original_hash": original_hash,
            "original_size": file_size,
            "encrypted_size": output_size,
            "output_path": output_path,
            "algorithm": "AES-256-GCM",
            "kdf": "PBKDF2-HMAC-SHA256",
            "iterations": ITERATIONS
        }

    except EncryptionError:
        raise
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise EncryptionError(f"Encryption failed: {str(e)}")


def decrypt_file(
    input_path: str,
    output_dir: str,
    password: str,
    progress_callback: Optional[Callable[[float], None]] = None
) -> dict:
    """Decrypt a file that was encrypted with this tool."""
    try:
        input_file = Path(input_path)
        if not input_file.exists():
            raise DecryptionError(f"Encrypted file not found: {input_path}")

        with open(input_path, "rb") as f:
            # Validate magic bytes
            magic = f.read(8)
            if magic != MAGIC_BYTES:
                raise DecryptionError("Not a valid encrypted file (invalid header)")

            # Read version
            version = struct.unpack("<B", f.read(1))[0]
            if version != VERSION:
                raise DecryptionError(f"Unsupported file format version: {version}")

            # Read crypto parameters
            salt = f.read(SALT_SIZE)
            nonce = f.read(NONCE_SIZE)

            # Read original filename
            name_length = struct.unpack("<I", f.read(4))[0]
            if name_length > 1024:
                raise DecryptionError("Invalid filename length in header")
            original_name = f.read(name_length).decode("utf-8")

            # Read ciphertext
            ciphertext = f.read()

        if progress_callback:
            progress_callback(0.3)

        # Derive key from password
        key = derive_key(password, salt)

        if progress_callback:
            progress_callback(0.5)

        # Decrypt
        aesgcm = AESGCM(key)
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        except Exception:
            raise DecryptionError("Decryption failed — incorrect password or corrupted file")

        if progress_callback:
            progress_callback(0.8)

        # Write decrypted file
        output_path = Path(output_dir) / original_name
        
        # Handle filename conflicts
        counter = 1
        while output_path.exists():
            stem = Path(original_name).stem
            suffix = Path(original_name).suffix
            output_path = Path(output_dir) / f"{stem}_{counter}{suffix}"
            counter += 1

        with open(output_path, "wb") as f:
            f.write(plaintext)

        if progress_callback:
            progress_callback(1.0)

        decrypted_hash = compute_file_hash(str(output_path))
        file_size = output_path.stat().st_size

        logger.info(f"Decrypted: {input_path} -> {output_path} ({file_size} bytes)")

        return {
            "output_path": str(output_path),
            "original_name": original_name,
            "file_size": file_size,
            "file_hash": decrypted_hash
        }

    except DecryptionError:
        raise
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise DecryptionError(f"Decryption failed: {str(e)}")


def verify_encrypted_file(filepath: str) -> dict:
    """Check if a file is a valid encrypted file from this tool. Returns metadata."""
    try:
        with open(filepath, "rb") as f:
            magic = f.read(8)
            if magic != MAGIC_BYTES:
                raise IntegrityError("Not a valid encrypted file")

            version = struct.unpack("<B", f.read(1))[0]
            f.read(SALT_SIZE)  # salt
            f.read(NONCE_SIZE)  # nonce

            name_length = struct.unpack("<I", f.read(4))[0]
            original_name = f.read(name_length).decode("utf-8")

            remaining = f.read()
            ciphertext_size = len(remaining)

        return {
            "valid": True,
            "version": version,
            "original_name": original_name,
            "ciphertext_size": ciphertext_size,
            "algorithm": "AES-256-GCM"
        }

    except IntegrityError:
        raise
    except Exception as e:
        raise IntegrityError(f"File verification failed: {str(e)}")
