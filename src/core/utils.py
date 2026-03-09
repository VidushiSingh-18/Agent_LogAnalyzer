"""Utility functions for file and JSON handling."""

import json
from pathlib import Path
from typing import List, Dict


def pick_requirement(file_path: str = None, req_dir: str = "data/requirements") -> Path:
    """Select requirement file - either specific path or first .txt in directory."""

    # If specific file given, use it
    if file_path:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path

    # Otherwise, pick first .txt file
    txt_files = sorted(Path(req_dir).glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {req_dir}")

    return txt_files[0]



def parse_json_safely(text: str, raw_file: Path) -> List[Dict]:
    """Parse LLM text as JSON, handling markdown fences."""

    # Always save raw output for debugging
    raw_file.parent.mkdir(parents=True, exist_ok=True)
    raw_file.write_text(text, encoding="utf-8")

    if not text or not text.strip():
        raise ValueError("LLM returned empty response.")

    # ── Attempt 1: parse as-is ──────────────────────────────
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # ── Attempt 2: extract JSON array using bracket search ──
    # Handles cases where LLM adds text before/after JSON
    try:
        start = text.index("[")
        end = text.rindex("]") + 1
        data = json.loads(text[start:end])
        if isinstance(data, list):
            return data
    except (ValueError, json.JSONDecodeError):
        pass

    # ── Attempt 3: strip markdown fences ────────────────────
    try:
        cleaned = text.strip()
        # Remove opening fence (```json or ```)
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]           # remove opening ```
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]       # remove language tag
            # Remove closing ```
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # ── All attempts failed ──────────────────────────────────
    print(f"\n❌ Could not parse JSON. Raw response was:\n{text[:500]}\n")
    raise ValueError("Could not extract valid JSON array from LLM response.")


def pick_log_file(file_path: str = None, log_dir: str = "data/logs") -> Path:
    """Select log file - specific path or first .log file."""

    if file_path:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {file_path}")
        return path

    # Auto-pick first .log file
    log_files = sorted(Path(log_dir).glob("*.log"))
    if not log_files:
        raise FileNotFoundError(f"No .log files in {log_dir}")

    return log_files[0]