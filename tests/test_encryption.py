"""
Basic encryption/decryption tests.
Run with: python -m pytest tests/ -v
"""

import os
import tempfile
import pytest
from pathlib import Path

from core.encryption import encrypt_file, decrypt_file, EncryptionError, DecryptionError


@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary test file."""
    filepath = tmp_path / "test_document.txt"
    filepath.write_text("This is a test file for encryption verification.\n" * 50)
    return str(filepath)


@pytest.fixture
def password():
    return "TestPassword123!"


class TestEncryption:
    """Test suite for AES-256-GCM encryption."""

    def test_encrypt_creates_output(self, sample_file, password, tmp_path):
        output = str(tmp_path / "encrypted.enc")
        result = encrypt_file(sample_file, output, password)

        assert os.path.exists(output)
        assert result["original_size"] > 0
        assert result["encrypted_size"] > 0
        assert result["algorithm"] == "AES-256-GCM"

    def test_encrypt_decrypt_roundtrip(self, sample_file, password, tmp_path):
        encrypted_path = str(tmp_path / "encrypted.enc")
        encrypt_file(sample_file, encrypted_path, password)

        output_dir = str(tmp_path / "decrypted")
        os.makedirs(output_dir)
        result = decrypt_file(encrypted_path, output_dir, password)

        assert os.path.exists(result["output_path"])

        original_content = Path(sample_file).read_text()
        decrypted_content = Path(result["output_path"]).read_text()
        assert original_content == decrypted_content

    def test_wrong_password_fails(self, sample_file, password, tmp_path):
        encrypted_path = str(tmp_path / "encrypted.enc")
        encrypt_file(sample_file, encrypted_path, password)

        output_dir = str(tmp_path / "decrypted")
        os.makedirs(output_dir)

        with pytest.raises(DecryptionError):
            decrypt_file(encrypted_path, output_dir, "WrongPassword!")

    def test_empty_file_fails(self, tmp_path, password):
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        output = str(tmp_path / "encrypted.enc")

        with pytest.raises(EncryptionError):
            encrypt_file(str(empty_file), output, password)

    def test_nonexistent_file_fails(self, password, tmp_path):
        output = str(tmp_path / "encrypted.enc")
        with pytest.raises(EncryptionError):
            encrypt_file("/nonexistent/path.txt", output, password)

    def test_encrypted_file_larger_than_original(self, sample_file, password, tmp_path):
        output = str(tmp_path / "encrypted.enc")
        result = encrypt_file(sample_file, output, password)

        # Encrypted file includes header overhead + GCM tag
        assert result["encrypted_size"] > result["original_size"]
