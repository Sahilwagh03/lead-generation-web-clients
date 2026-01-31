import os

EXCLUDE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
    ".next",
    "ig_session"
}

OUTPUT_FILE = "project_structure.txt"


def generate_tree(root_dir, file):
    for root, dirs, files in os.walk(root_dir):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        level = root.replace(root_dir, "").count(os.sep)
        indent = "│   " * level
        folder_name = os.path.basename(root) or root_dir

        file.write(f"{indent}├── {folder_name}/\n")

        sub_indent = "│   " * (level + 1)
        for filename in files:
            file.write(f"{sub_indent}├── {filename}\n")


if __name__ == "__main__":
    base_dir = os.path.abspath(".")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"{os.path.basename(base_dir)}/\n")
        generate_tree(base_dir, f)

    print(f"✅ Project structure saved to {OUTPUT_FILE}")
