import os

# Run this script from inside ai-crash-analyzer-poc
folders = [
    "crash_logs",
    "analysis",
    "history_learning",
    "ai_model",
    "scripts"
]

files = [
    "README.md",
    "requirements.txt"
]

# Create subfolders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create empty files
for file in files:
    with open(file, 'w') as f:
        f.write("")

print("Subfolders and files created inside ai-crash-analyzer-poc.")
