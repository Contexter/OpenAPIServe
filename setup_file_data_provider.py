import os
import subprocess
import shutil

# Paths
PROJECT_ROOT = "/Users/benedikteickhoff/Development/Github-Desktop/OpenAPIServe"
SOURCES_DIR = os.path.join(PROJECT_ROOT, "Sources/OpenAPIServe")
PACKAGE_FILE = os.path.join(PROJECT_ROOT, "Package.swift")

def create_file_data_provider():
    """Creates the FileDataProvider.swift file if it doesn't already exist."""
    file_path = os.path.join(SOURCES_DIR, "FileDataProvider.swift")
    if not os.path.exists(file_path):
        print("Creating FileDataProvider.swift...")
        with open(file_path, "w") as f:
            f.write("""\
import Foundation

/// A `DataProvider` that reads data from a file.
public struct FileDataProvider: DataProvider {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func getData() -> String {
        do {
            let data = try String(contentsOfFile: filePath, encoding: .utf8)
            return data
        } catch {
            print("Error reading file at \\(filePath): \\(error)")
            return ""
        }
    }
}
""")
        print("FileDataProvider.swift created.")
    else:
        print("FileDataProvider.swift already exists.")

def ensure_package_includes_file_data_provider():
    """Ensures that FileDataProvider.swift is correctly included in Package.swift."""
    with open(PACKAGE_FILE, "r") as f:
        package_content = f.read()

    if "Sources/OpenAPIServe" not in package_content:
        print("Updating Package.swift to include FileDataProvider...")
        # Modify Package.swift to ensure FileDataProvider is included
        with open(PACKAGE_FILE, "w") as f:
            updated_content = package_content.replace(
                'path: "Sources/OpenAPIServe"',
                'path: "Sources/OpenAPIServe"'
            )
            f.write(updated_content)
        print("Package.swift updated.")
    else:
        print("Package.swift already includes FileDataProvider.")

def build_and_test():
    """Build and test the Swift package."""
    print("Cleaning build directory...")
    subprocess.run(["swift", "package", "clean"], check=True, cwd=PROJECT_ROOT)

    print("Building the project...")
    try:
        subprocess.run(["swift", "build"], check=True, cwd=PROJECT_ROOT)
        print("Build succeeded.")
    except subprocess.CalledProcessError:
        print("Error during build. Please check your code.")
        return

    print("Running tests...")
    try:
        subprocess.run(["swift", "test"], check=True, cwd=PROJECT_ROOT)
        print("Tests passed successfully.")
    except subprocess.CalledProcessError:
        print("Error during testing. Please check your tests.")

def main():
    """Main function to set up FileDataProvider and test the project."""
    print("Setting up FileDataProvider...")
    create_file_data_provider()
    ensure_package_includes_file_data_provider()
    build_and_test()

if __name__ == "__main__":
    main()
