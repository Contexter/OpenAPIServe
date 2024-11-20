# Script Name: fix_vapor_test_file_with_cleanup.py
# Purpose: Update Vapor 4 test files, handle duplicates, and ensure compatibility.

import os
from datetime import datetime
import shutil

# File paths and backup settings
original_file = "Tests/OpenAPIServeTests/OpenAPIServeTests.swift"
backup_folder = "Backups"
backup_file = f"{backup_folder}/OpenAPIServeTests_{datetime.now().strftime('%Y%m%d%H%M%S')}.swift"

def ensure_backup_folder():
    """Ensure the backup folder exists."""
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

def move_existing_backups():
    """Move any existing backup files out of the test directory."""
    test_dir = "Tests/OpenAPIServeTests/"
    for file in os.listdir(test_dir):
        if file.startswith("OpenAPIServeTests_") and file.endswith(".swift"):
            shutil.move(os.path.join(test_dir, file), backup_folder)
            print(f"Moved backup file: {file} to {backup_folder}/")

def fix_test_file(original_path, backup_path):
    """Fix Vapor 4 test file issues and create a backup."""
    if not os.path.exists(original_path):
        print(f"Error: The file {original_path} does not exist.")
        return

    # Read the original file
    with open(original_path, "r") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        # Update response.statusCode to response.status
        if "response.statusCode" in line:
            line = line.replace("response.statusCode", "response.status")

        # Update .ok and .notFound to HTTPStatus.ok and HTTPStatus.notFound
        if ".ok" in line or ".notFound" in line:
            line = line.replace(".ok", "HTTPStatus.ok")
            line = line.replace(".notFound", "HTTPStatus.notFound")

        # Ensure response.body.string is accessed safely
        if "response.body" in line and ".string" not in line:
            line = line.replace("response.body", "response.body.string")

        updated_lines.append(line)

    # Create a backup
    with open(backup_path, "w") as backup:
        backup.writelines(lines)
    print(f"Backup created: {backup_path}")

    # Write the updated content back to the original file
    with open(original_path, "w") as file:
        file.writelines(updated_lines)
    print(f"File updated: {original_path}")

def main():
    """Main script logic."""
    ensure_backup_folder()
    move_existing_backups()
    fix_test_file(original_file, backup_file)

if __name__ == "__main__":
    main()

