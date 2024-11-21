import os

def index_repository(repo_path):
    for root, dirs, files in os.walk(repo_path):
        level = root.replace(repo_path, "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 2 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

# Change this path to the root of your repository
repo_path = "/Users/benedikteickhoff/Development/Github-Desktop/OpenAPIServe"
index_repository(repo_path)


