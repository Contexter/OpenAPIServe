import os
import shutil

def fetch_project_tree():
    """
    Retrieve the current project structure.
    """
    structure = {}
    for root, dirs, files in os.walk("."):
        structure[root] = files
    return structure

def ensure_resource_folder(structure, project_root):
    """
    Ensure Resources folder exists under Sources and migrate files there.
    """
    resource_path = os.path.join(project_root, "Sources", "Resources")
    if not os.path.exists(resource_path):
        print(f"Creating Resources directory at {resource_path}")
        os.makedirs(resource_path)

    # Look for misplaced resources
    for folder, files in structure.items():
        for file in files:
            if file.endswith(".leaf") or file.endswith(".yml"):
                src_path = os.path.join(folder, file)
                dst_path = os.path.join(resource_path, file)
                print(f"Moving {src_path} to {dst_path}")
                try:
                    shutil.move(src_path, dst_path)
                except FileNotFoundError:
                    print(f"Error: {src_path} not found. Skipping.")

def ensure_test_utilities_folder(structure, project_root):
    """
    Ensure Utilities folder exists within the Tests folder and files are correctly placed.
    """
    utilities_path = os.path.join(project_root, "Tests", "OpenAPIServeTests", "Utilities")
    if not os.path.exists(utilities_path):
        print(f"Creating Utilities directory at {utilities_path}")
        os.makedirs(utilities_path)

    # Move utility files to the Utilities folder
    for folder, files in structure.items():
        for file in files:
            if "TestAssertions" in file or "MockDataProvider" in file or "TestAppConfigurator" in file:
                src_path = os.path.join(folder, file)
                dst_path = os.path.join(utilities_path, file)
                print(f"Moving {src_path} to {dst_path}")
                try:
                    shutil.move(src_path, dst_path)
                except FileNotFoundError:
                    print(f"Error: {src_path} not found. Skipping.")

def main():
    """
    Main script function.
    """
    print("Fetching project structure...")
    project_root = os.getcwd()
    structure = fetch_project_tree()

    print("Patching Resources...")
    ensure_resource_folder(structure, project_root)

    print("Patching Test Utilities...")
    ensure_test_utilities_folder(structure, project_root)

    print("\nProject structure fixed. Please run the following commands manually to verify:")
    print("\n\t1. swift package clean")
    print("\t2. swift package resolve")
    print("\t3. swift build")
    print("\t4. swift test\n")

if __name__ == "__main__":
    main()

