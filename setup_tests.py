import os
import shutil
import subprocess

# Constants
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
TESTS_DIR = os.path.join(REPO_ROOT, "Tests", "OpenAPIServeTests")
BACKUP_DIR = os.path.join(REPO_ROOT, "Tests_Backup")
PACKAGE_FILE = os.path.join(REPO_ROOT, "Package.swift")
INITIAL_TEST_CONTENT = """
import XCTVapor
@testable import OpenAPIServe

final class ServeOpenAPISuccessTests: XCTestCase {
    func testServeOpenAPISpec() throws {
        let app = Application(.testing)
        defer { app.shutdown() }
        try configure(app)

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, .init("application/x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
"""

# Utility Functions
def backup_existing_tests():
    if os.path.exists(BACKUP_DIR):
        print("Backup directory already exists. Skipping backup.")
    else:
        print("Creating backup directory...")
        shutil.copytree(TESTS_DIR, BACKUP_DIR)
        print(f"Backup created at {BACKUP_DIR}")

def clean_tests_directory():
    if os.path.exists(TESTS_DIR):
        print(f"Cleaning existing tests directory: {TESTS_DIR}")
        shutil.rmtree(TESTS_DIR)
    os.makedirs(TESTS_DIR, exist_ok=True)
    print(f"Tests directory reset: {TESTS_DIR}")

def add_minimal_test():
    print("Adding initial minimal test...")
    test_file_path = os.path.join(TESTS_DIR, "test_serve_openapi_success.swift")
    with open(test_file_path, "w") as f:
        f.write(INITIAL_TEST_CONTENT)
    print(f"Minimal test created: {test_file_path}")

def update_package_file():
    if os.path.exists(PACKAGE_FILE):
        print("Ensuring Package.swift includes necessary dependencies...")
        with open(PACKAGE_FILE, "r") as f:
            content = f.read()
        if "XCTVapor" not in content:
            print("Adding XCTVapor dependency...")
            content = content.replace(
                'dependencies: [',
                'dependencies: [\n        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),'
            )
            with open(PACKAGE_FILE, "w") as f:
                f.write(content)
            print("Package.swift updated.")
        else:
            print("XCTVapor dependency already exists. No changes made.")
    else:
        print("Package.swift not found. Skipping.")

def build_and_test():
    print("Building the project...")
    subprocess.run(["swift", "build"], check=True)
    print("Running tests...")
    subprocess.run(["swift", "test"], check=True)

# Main Script Execution
if __name__ == "__main__":
    print("Starting test setup for OpenAPIServe...")
    backup_existing_tests()
    clean_tests_directory()
    add_minimal_test()
    update_package_file()
    build_and_test()
    print("Test setup complete.")
