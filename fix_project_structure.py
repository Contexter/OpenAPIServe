import os
import shutil

ROOT_DIR = os.path.abspath(".")
RESOURCES_DIR = os.path.join(ROOT_DIR, "Sources/OpenAPIServe/Resources")
VIEWS_DIR = os.path.join(RESOURCES_DIR, "Views")
BACKUP_DIR = os.path.join(ROOT_DIR, "Tests_Backup")
UTILITIES_DIR = os.path.join(ROOT_DIR, "Tests/OpenAPIServeTests/Utilities")

def ensure_directories():
    """Ensure required directories exist."""
    if not os.path.exists(RESOURCES_DIR):
        os.makedirs(RESOURCES_DIR)
    if not os.path.exists(VIEWS_DIR):
        os.makedirs(VIEWS_DIR)

def move_resources():
    """Move resource files to their correct locations."""
    resource_files = [
        "Sources/OpenAPIServe/Resources/Views/redoc.leaf"
    ]
    for file in resource_files:
        src = os.path.join(ROOT_DIR, file)
        dest = os.path.join(VIEWS_DIR, os.path.basename(file))
        if os.path.exists(src) and src != dest:
            shutil.move(src, dest)
            print(f"Moved {src} to {dest}")

def clean_backups():
    """Remove backup files that conflict with the build."""
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)
        print(f"Removed backup directory: {BACKUP_DIR}")

def verify_test_utilities():
    """Verify utility files are properly located."""
    expected_utilities = [
        "MockDataProvider.swift",
        "TestAppConfigurator.swift",
        "TestAssertions.swift"
    ]
    for utility in expected_utilities:
        utility_path = os.path.join(UTILITIES_DIR, utility)
        if not os.path.exists(utility_path):
            print(f"Missing utility file: {utility_path}")

def main():
    print("Fixing project structure...")
    ensure_directories()
    move_resources()
    clean_backups()
    verify_test_utilities()
    print("Project structure fixed. Run `swift build` to compile.")

if __name__ == "__main__":
    main()
