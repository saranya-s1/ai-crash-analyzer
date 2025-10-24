# ...existing code...
import os
from datetime import datetime
import json
from pathlib import Path

from history_learning.dataset_manager import append_rows

CLASS_PATTERNS = {
    "NullPointerException": {
        "classification": "EventService",
        "root_cause": "Null pointer in event dispatch",
        "suggested_fix": "Add null checks before dereference."
    },
    "UnsupportedOperationException": {
        "classification": "ServiceRouting",
        "root_cause": "Unsupported API call",
        "suggested_fix": "Validate API availability / implementation."
    },
}

def analyze_log(log_text: str) -> dict:
    for key, data in CLASS_PATTERNS.items():
        if key in log_text:
            return {**data, "matched": key}
    return {
        "classification": "Unknown",
        "root_cause": "Insufficient info",
        "suggested_fix": "Manual investigation",
        "matched": None
    }

def extract_simple_features(log_text: str) -> dict:
    lower = log_text.lower()
    return {
        "is_crash": int("exception" in lower or "error" in lower),
        "has_null": int("null" in lower),
        "line_count": len([l for l in log_text.splitlines() if l.strip()]),
        "char_len": len(log_text),
    }

def process_log_file(file_path: Path) -> dict:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    analysis = analyze_log(text)
    feats = extract_simple_features(text)
    return {
        "file": file_path.name,
        **analysis,
        **feats,
        "timestamp_processed": datetime.utcnow().isoformat()
    }

def save_analysis(result: dict):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_txt = Path("analysis") / f"analysis_{ts}_{result['file']}.txt"
    out_json = Path("analysis") / f"analysis_{ts}_{result['file']}.json"
    out_txt.parent.mkdir(exist_ok=True)
    out_txt.write_text(
        "\n".join([
            f"File: {result['file']}",
            f"Classification: {result['classification']}",
            f"Root Cause: {result['root_cause']}",
            f"Suggested Fix: {result['suggested_fix']}",
            f"Matched Pattern: {result['matched']}",
            f"Lines: {result['line_count']}",
            f"Chars: {result['char_len']}",
            f"Processed UTC: {result['timestamp_processed']}",
        ]),
        encoding="utf-8"
    )
    out_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"[✓] Saved {out_txt.name} and JSON.")

def append_learning_row(result: dict):
    row = {
        "timestamp": result["timestamp_processed"],
        "service": "unknown",
        "is_crash": result["is_crash"],
        "is_restart": 0,
        "has_exception": int(result["classification"] != "Unknown"),
        "length": result["char_len"],
    }
    append_rows([row])

def main():
    log_dir = Path("crash_logs")
    files = [p for p in log_dir.glob("*") if p.suffix in (".log", ".txt")]
    if not files:
        print("[!] No crash logs found.")
        return
    for fp in files:
        print(f"[*] Analyzing: {fp.name}")
        result = process_log_file(fp)
        save_analysis(result)
        append_learning_row(result)

if __name__ == "__main__":
    main()
# ...existing code...