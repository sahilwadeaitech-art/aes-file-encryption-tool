"""
Report Generator
Generate encryption activity reports in plain text format.

Author: Sahil Wade
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from database.history import HistoryDB
from modules.file_utils import format_file_size


REPORTS_DIR = Path(__file__).parent.parent / "reports"


def generate_activity_report(
    db: Optional[HistoryDB] = None,
    output_dir: Optional[str] = None
) -> str:
    """
    Generate a plain-text activity report summarizing encryption operations.
    
    Args:
        db: HistoryDB instance (creates new one if not provided)
        output_dir: Directory to save report (defaults to reports/)
    
    Returns:
        Path to the generated report file
    """
    if db is None:
        db = HistoryDB()

    if output_dir is None:
        output_dir = str(REPORTS_DIR)

    os.makedirs(output_dir, exist_ok=True)

    stats = db.get_statistics()
    recent = db.get_recent_operations(limit=25)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"encryption_report_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    lines = []
    lines.append("=" * 60)
    lines.append("  AES FILE ENCRYPTION UTILITY — ACTIVITY REPORT")
    lines.append("=" * 60)
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  SUMMARY")
    lines.append("-" * 60)
    lines.append(f"  Total Operations:    {stats['total_operations']}")
    lines.append(f"  Encryptions:         {stats['total_encryptions']}")
    lines.append(f"  Decryptions:         {stats['total_decryptions']}")
    lines.append(f"  Failures:            {stats['total_failures']}")
    lines.append(f"  Success Rate:        {stats['success_rate']}%")
    lines.append(f"  Data Processed:      {format_file_size(stats['total_bytes_processed'])}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  RECENT OPERATIONS (last 25)")
    lines.append("-" * 60)

    if recent:
        for op in recent:
            ts = op["timestamp"][:19].replace("T", " ")
            op_type = op["operation_type"].upper().ljust(8)
            status = "OK" if op["status"] == "success" else "FAIL"
            size = format_file_size(op["file_size"]) if op["file_size"] else "—"
            lines.append(f"  [{ts}] {op_type} {status}  {op['filename']}  ({size})")
    else:
        lines.append("  No operations recorded.")

    lines.append("")
    lines.append("-" * 60)
    lines.append("  SECURITY CONFIGURATION")
    lines.append("-" * 60)
    lines.append("  Algorithm:       AES-256-GCM")
    lines.append("  Key Derivation:  PBKDF2-HMAC-SHA256 (600K iterations)")
    lines.append("  Processing:      Local only (no network)")
    lines.append("")
    lines.append("=" * 60)
    lines.append("  End of Report")
    lines.append("=" * 60)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath
