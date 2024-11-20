# Script Name: fix_vapor_test_file.py
# Purpose: To update Vapor 4 test files for compatibility, ensuring proper syntax and creating a backup with a unique name.

import os
from datetime import datetime

# Define the original and updated test file paths
original_file = "Tests/OpenAPIServeTests/OpenAPIServeTests.swift"
backup_file = f"Tests/OpenAPIServeTests/OpenAPIServeTests_{datetime.now().strftime('%Y%m%d%H%M%S')}.swift"

def fix_vapor_tests(original_path, backup_path):
    """Fixes Vapor 4 test file issues and creates a backup with a unique name."""
    if not os.path.exists(original_path):
        print(f"Error: The file {original_path} does not exist.")
        return

    # Read the original file
    with open(original_path, "r") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        # Update response.status to HTTPStatus
        if "response.status" in line:
            line = line.replace("response.status", "response.statusCode")

        # Update .ok and .notFound to HTTPStatus.ok and HTTPStatus.notFound
        if ".ok" in line or ".notFound" in line:
            line = line.replace(".ok", "HTTPStatus.ok")
            line = line.replace(".notFound", "HTTPStatus.notFound")

        # Update response.body to safely access response.body.string
        if "response.body" in line and ".string" not in line:
            line = line.replace("response.body", "response.body.string")

        # Add to updated lines
        updated_lines.append(line)

    # Create a backup
    with open(backup_path, "w") as backup:
        backup.writelines(lines)
    print(f"Backup created: {backup_path}")

    # Write the updated content back to the original file
    with open(original_path, "w") as file:
        file.writelines(updated_lines)
    print(f"File updated: {original_path}")

# Run the script
fix_vapor_tests(original_file, backup_file)

