"""
SQLite-backed history for tracking encrypt/decrypt operations.
"""

import sqlite3
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "encryption_history.db"


class HistoryDB:
    """Manages encryption operation history in SQLite."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(DB_PATH)
        self._ensure_db_dir()
        self._init_db()

    def _ensure_db_dir(self):
        """Ensure the database directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    operation_type TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    filepath TEXT,
                    file_size INTEGER,
                    status TEXT NOT NULL,
                    algorithm TEXT DEFAULT 'AES-256-GCM',
                    duration_ms INTEGER,
                    file_hash TEXT,
                    notes TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    encryptions INTEGER DEFAULT 0,
                    decryptions INTEGER DEFAULT 0,
                    total_bytes_processed INTEGER DEFAULT 0,
                    failures INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_operations_timestamp 
                ON operations(timestamp DESC)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_operations_type 
                ON operations(operation_type)
            """)
            conn.commit()
        logger.debug(f"Database initialized at {self.db_path}")

    def record_operation(
        self,
        operation_type: str,
        filename: str,
        filepath: str = "",
        file_size: int = 0,
        status: str = "success",
        algorithm: str = "AES-256-GCM",
        duration_ms: int = 0,
        file_hash: str = "",
        notes: str = ""
    ) -> int:
        """Log an encrypt/decrypt operation to the database."""
        timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO operations 
                (timestamp, operation_type, filename, filepath, file_size, 
                 status, algorithm, duration_ms, file_hash, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, operation_type, filename, filepath, file_size,
                status, algorithm, duration_ms, file_hash, notes
            ))

            # Update daily statistics
            today = datetime.now().strftime("%Y-%m-%d")
            existing = conn.execute(
                "SELECT id FROM statistics WHERE date = ?", (today,)
            ).fetchone()

            if existing:
                if operation_type == "encrypt":
                    conn.execute("""
                        UPDATE statistics SET encryptions = encryptions + 1,
                        total_bytes_processed = total_bytes_processed + ?
                        WHERE date = ?
                    """, (file_size, today))
                elif operation_type == "decrypt":
                    conn.execute("""
                        UPDATE statistics SET decryptions = decryptions + 1,
                        total_bytes_processed = total_bytes_processed + ?
                        WHERE date = ?
                    """, (file_size, today))
                if status == "failed":
                    conn.execute("""
                        UPDATE statistics SET failures = failures + 1 WHERE date = ?
                    """, (today,))
            else:
                enc = 1 if operation_type == "encrypt" else 0
                dec = 1 if operation_type == "decrypt" else 0
                fail = 1 if status == "failed" else 0
                conn.execute("""
                    INSERT INTO statistics (date, encryptions, decryptions, 
                    total_bytes_processed, failures)
                    VALUES (?, ?, ?, ?, ?)
                """, (today, enc, dec, file_size, fail))

            conn.commit()
            return cursor.lastrowid

    def get_recent_operations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get the most recent operations."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM operations ORDER BY timestamp DESC LIMIT ?
            """, (limit,)).fetchall()
            return [dict(row) for row in rows]

    def get_operations_by_type(
        self, operation_type: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get operations filtered by type."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM operations 
                WHERE operation_type = ? 
                ORDER BY timestamp DESC LIMIT ?
            """, (operation_type, limit)).fetchall()
            return [dict(row) for row in rows]

    def get_statistics(self) -> Dict[str, Any]:
        """Get aggregate statistics."""
        with sqlite3.connect(self.db_path) as conn:
            total_ops = conn.execute(
                "SELECT COUNT(*) FROM operations"
            ).fetchone()[0]
            
            total_encryptions = conn.execute(
                "SELECT COUNT(*) FROM operations WHERE operation_type = 'encrypt'"
            ).fetchone()[0]
            
            total_decryptions = conn.execute(
                "SELECT COUNT(*) FROM operations WHERE operation_type = 'decrypt'"
            ).fetchone()[0]
            
            total_failures = conn.execute(
                "SELECT COUNT(*) FROM operations WHERE status = 'failed'"
            ).fetchone()[0]
            
            total_bytes = conn.execute(
                "SELECT COALESCE(SUM(file_size), 0) FROM operations WHERE status = 'success'"
            ).fetchone()[0]

            success_rate = 0.0
            if total_ops > 0:
                success_rate = ((total_ops - total_failures) / total_ops) * 100

            return {
                "total_operations": total_ops,
                "total_encryptions": total_encryptions,
                "total_decryptions": total_decryptions,
                "total_failures": total_failures,
                "total_bytes_processed": total_bytes,
                "success_rate": round(success_rate, 1)
            }

    def get_daily_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get daily statistics for the last N days."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM statistics ORDER BY date DESC LIMIT ?
            """, (days,)).fetchall()
            return [dict(row) for row in rows]

    def clear_history(self) -> None:
        """Clear all operation history (for testing/reset)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM operations")
            conn.execute("DELETE FROM statistics")
            conn.commit()
        logger.info("History cleared")

    def get_total_count(self) -> int:
        """Get total number of operations recorded."""
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM operations"
            ).fetchone()[0]
