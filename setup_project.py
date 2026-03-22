# Utility script to initialize the project directory structure.

import os
import shutil

def setup_structure():
    # 1. Define the directory structure we need
    dirs = [
        "src/agents/nodes",
        "src/tools",
        "src/core"
    ]
    
    # 2. Create directories and __init__.py files
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Create init in the leaf and all parents up to src to ensure they are packages
        parts = d.split("/")
        current_path = ""
        for part in parts:
            current_path = os.path.join(current_path, part) if current_path else part
            init_file = os.path.join(current_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    pass

    # 3. Map files to their new destinations
    moves = {
        "scout.py": "src/agents/nodes/scout.py",
        "strategist.py": "src/agents/nodes/strategist.py",
        "state.py": "src/agents/state.py",
    }

    for filename, dest in moves.items():
        if os.path.exists(filename):
            shutil.move(filename, dest)
            print(f"Moved {filename} -> {dest}")
        elif os.path.exists(dest):
            print(f"{filename} is already in place.")
        else:
            print(f"Warning: Could not find {filename} in root to move.")

if __name__ == "__main__":
    setup_structure()
    print("\nProject structure organized successfully!")
    print("You can now run: python main.py")