import os
from pathlib import Path

def ensure_directory(directory_path: str):
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def save_text(filename: str, content: str, output_dir: str):
    output_path = Path(output_dir) / f"{filename}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Exported: {output_path.name}")