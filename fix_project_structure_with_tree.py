import os
import shutil
import subprocess

def get_repository_tree(project_root):
    """Generate and parse the repository tree structure."""
    print("Generating repository tree...")
    result = subprocess.run(["tree", "-a", project_root], stdout=subprocess.PIPE, text=True)
    tree_structure = result.stdout
    print("Parsing tree structure...")
    return tree_structure

def find_file_in_tree(tree_structure, filename):
    """Search for a file within the parsed tree structure."""
    for line in tree_structure.splitlines():
        # Clean up any tree formatting from the output
        cleaned_line = line.strip().lstrip("│├└─ ")
        if filename in cleaned_line:
            return cleaned_line
    return None

def ensure_correct_resource_path(tree_structure, project_root):
    """Ensure resources are correctly placed in the project."""
    resources_dir = os.path.join(project_root, "Sources", "Resources")
    if not os.path.exists(resources_dir):
        print("No Resources directory found. Creating one in Sources...")
        os.makedirs(resources_dir)
    
    redoc_path = find_file_in_tree(tree_structure, "redoc.leaf")
    if redoc_path:
        file_path = os.path.join(project_root, redoc_path)
        target_path = os.path.join(resources_dir, "redoc.leaf")
        print(f"Moving {file_path} to {target_path}")
        try:
            shutil.move(file_path, target_path)
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
    else:
        print("Error: 'redoc.leaf' not found in repository tree.")

def main():
    project_root = os.getcwd()  # Assume the script is run from the project root
    tree_structure = get_repository_tree(project_root)
    ensure_correct_resource_path(tree_structure, project_root)
    print("Resource paths fixed.")

if __name__ == "__main__":
    main()
