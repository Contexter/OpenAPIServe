#!/usr/bin/env python3

import os
import subprocess
import shutil
import json

def activate_project_env():
    """Activate the Python virtual environment in the project."""
    venv_path = os.path.join(os.getcwd(), ".venv", "bin", "activate")
    if not os.path.exists(venv_path):
        print("No virtual environment found in the project. Please set it up first.")
        return False
    return True

def run_in_venv(command):
    """Run a command within the project's Python virtual environment."""
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print(f"Command failed: {' '.join(command)}")
        print(result.stderr)
    return result.stdout

def fetch_project_structure():
    """Fetch and analyze the project's structure."""
    print("Fetching project structure...")
    command = ["tree", "-J"]
    output = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    if output.returncode != 0:
        print("Error: Unable to fetch project structure.")
        return None
    return json.loads(output.stdout)

def ensure_correct_paths(tree_structure):
    """Ensure resources and utilities are correctly placed."""
    resources_dir = "Sources/Resources"
    if not os.path.exists(resources_dir):
        print(f"Creating resources directory: {resources_dir}")
        os.makedirs(resources_dir, exist_ok=True)

    for node in tree_structure:
        if isinstance(node, dict) and node.get("type") == "file":
            if "redoc.leaf" in node["name"]:
                file_path = node["name"]
                target_path = os.path.join(resources_dir, "redoc.leaf")
                print(f"Moving {file_path} to {target_path}")
                shutil.move(file_path, target_path)

def main():
    if not activate_project_env():
        return

    print("Running in the project environment.")
    
    # Fetch and analyze tree
    tree_structure = fetch_project_structure()
    if not tree_structure:
        print("Error analyzing tree structure.")
        return

    # Process resources and utilities
    ensure_correct_paths(tree_structure)

    # Run build and test commands
    print("Running Swift build...")
    run_in_venv(["swift", "build"])

    print("Running Swift tests...")
    run_in_venv(["swift", "test"])

if __name__ == "__main__":
    main()

