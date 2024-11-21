import os
import shutil
import subprocess

# Paths
PROJECT_DIR = os.getcwd()
TESTS_DIR = os.path.join(PROJECT_DIR, "Tests/OpenAPIServeTests")
BACKUP_DIR = os.path.join(PROJECT_DIR, "Tests_Backup")

# Test files to be created
TEST_FILES = [
    {
        "name": "test_serve_openapi_success.swift",
        "content": """\
import XCTVapor
@testable import OpenAPIServe

// MockDataProvider conforming to DataProvider protocol
struct MockDataProvider: DataProvider {
    let mockContent: String
    
    func getData() -> String {
        return mockContent
    }
}

final class ServeOpenAPITests: XCTestCase {
    func testServeOpenAPISuccess() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        let dataProvider = MockDataProvider(mockContent: "openapi: 3.0.0")
        app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType(type: "application", subType: "x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
"""
    }
]

def create_backup():
    """Create a backup of the current tests directory."""
    if os.path.exists(BACKUP_DIR):
        print(f"Removing existing backup: {BACKUP_DIR}")
        shutil.rmtree(BACKUP_DIR)
    print(f"Backup created at {BACKUP_DIR}")
    shutil.copytree(TESTS_DIR, BACKUP_DIR)

def clean_test_directory():
    """Clean and recreate the tests directory."""
    if os.path.exists(TESTS_DIR):
        shutil.rmtree(TESTS_DIR)
    os.makedirs(TESTS_DIR)
    print(f"Clean test directory created: {TESTS_DIR}")

def create_test_files():
    """Create test files in the clean test directory."""
    for test in TEST_FILES:
        file_path = os.path.join(TESTS_DIR, test["name"])
        with open(file_path, "w") as file:
            file.write(test["content"])
        print(f"Test file created: {file_path}")

def clean_build_directory():
    """Clean the build directory."""
    print("Cleaning build directory...")
    subprocess.run(["swift", "package", "clean"], check=True)
    print("Build directory cleaned.")

def build_and_test():
    """Build and run the tests."""
    print("Building and running tests...")
    try:
        subprocess.run(["swift", "build"], check=True)
        subprocess.run(["swift", "test"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during build or test: {e}")
        raise

def main():
    print("Setting up test environment...")
    create_backup()
    clean_test_directory()
    create_test_files()
    clean_build_directory()
    build_and_test()

if __name__ == "__main__":
    main()
