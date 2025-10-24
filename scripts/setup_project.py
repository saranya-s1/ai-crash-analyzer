# scripts/setup_project.py

import os

# Project root (one level above scripts/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folders to create
folders = [
    "crash_logs",          # Put raw crash logs here
    "analysis",            # Analysis output will go here
    "history_learning",    # Labeled logs for training the classifier
    "ai_model"             # AI models (trained) can be stored here
]

def create_folders():
    for folder in folders:
        folder_path = os.path.join(project_root, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"[✓] Created folder: {folder_path}")
        else:
            print(f"[!] Folder already exists: {folder_path}")

def create_sample_files():
    # Sample crash log
    sample_log = os.path.join(project_root, "crash_logs", "sample_nullpointer.log")
    if not os.path.exists(sample_log):
        with open(sample_log, "w") as f:
            f.write("NullPointerException: Something went wrong in EventService\n")
        print(f"[✓] Created sample crash log: {sample_log}")

    # Sample labeled CSV
    labeled_csv = os.path.join(project_root, "history_learning", "labeled_logs.csv")
    if not os.path.exists(labeled_csv):
        with open(labeled_csv, "w") as f:
            f.write("log_text,class\n")
            f.write("NullPointerException: Something went wrong in EventService,EventService\n")
            f.write("UnsupportedOperationException: API call failed,ServiceRouting\n")
        print(f"[✓] Created sample labeled CSV: {labeled_csv}")

if __name__ == "__main__":
    print("Setting up AI Crash Analyzer project structure...")
    create_folders()
    create_sample_files()
    print("[✓] Setup complete.")
