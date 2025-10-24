# scripts/analyze_crash.py

import os
from datetime import datetime

# Project root (one level above scripts/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def analyze_log(log_text):
    """Basic simulation of crash classification."""
    if "NullPointerException" in log_text:
        return {
            "classification": "EventService",
            "root_cause": "Null pointer encountered in event dispatch",
            "suggested_fix": "Add null checks before using the object."
        }
    elif "UnsupportedOperationException" in log_text:
        return {
            "classification": "ServiceRouting",
            "root_cause": "Unsupported API call attempted",
            "suggested_fix": "Check if the API is available or correctly implemented."
        }
    elif "TimeoutException" in log_text:
        return {
            "classification": "DatabaseService",
            "root_cause": "Database timeout while waiting for response",
            "suggested_fix": "Optimize query or increase timeout threshold."
        }
    else:
        return {
            "classification": "Unknown",
            "root_cause": "Could not determine from log",
            "suggested_fix": "Further manual investigation required."
        }

def process_log_file(file_path):
    with open(file_path, "r") as f:
        log_text = f.read()
    return analyze_log(log_text)

def save_analysis(result, original_filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    output_file = os.path.join(project_root, "analysis", f"analysis_{timestamp}.txt")
    with open(output_file, "w") as f:
        f.write(f"Original File: {original_filename}\n")
        f.write(f"Classification: {result['classification']}\n")
        f.write(f"Root Cause: {result['root_cause']}\n")
        f.write(f"Suggested Fix: {result['suggested_fix']}\n")
    print(f"[✓] Analysis saved to {output_file}")

if __name__ == "__main__":
    log_dir = os.path.join(project_root, "crash_logs")
    if not os.path.exists(log_dir):
        print("[!] crash_logs folder not found — run setup_project.py first.")
        exit()

    logs = [f for f in os.listdir(log_dir) if f.endswith(".log") or f.endswith(".txt")]

    if not logs:
        print("[!] No crash logs found in crash_logs/ folder.")
    else:
        for log_file in logs:
            log_path = os.path.join(log_dir, log_file)
            print(f"[*] Analyzing: {log_file}")
            result = process_log_file(log_path)
            save_analysis(result, log_file)
