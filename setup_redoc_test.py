import os
import subprocess
import shutil

# Paths
TESTS_DIR = "Tests/OpenAPIServeTests"
BACKUP_DIR = "Tests_Backup"
TEST_FILE = os.path.join(TESTS_DIR, "test_redoc_rendering.swift")

# Redoc Test Content
REDOC_TEST_CONTENT = """
import XCTVapor
@testable import OpenAPIServe

final class RedocRenderingTests: XCTestCase {
    func testRedocRendering() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Mock DataProvider returning valid OpenAPI spec content
        let mockProvider = MockDataProvider(mockContent: "openapi: 3.0.0")
        app.middleware.use(OpenAPIMiddleware(dataProvider: mockProvider))

        // Render ReDoc at `/docs`
        try app.test(.GET, "/docs", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertTrue(res.body.string.contains("<redoc"))
            XCTAssertTrue(res.body.string.contains("spec-url=\"/openapi.yml\""))
        })
    }
}

// MockDataProvider conforming to DataProvider protocol
struct MockDataProvider: DataProvider {
    let mockContent: String
    func getData() -> String {
        return mockContent
    }
}
"""

def backup_tests():
    """Backup existing tests directory."""
    if os.path.exists(BACKUP_DIR):
        print(f"Removing existing backup: {BACKUP_DIR}")
        shutil.rmtree(BACKUP_DIR)
    print(f"Creating backup at {BACKUP_DIR}")
    shutil.copytree(TESTS_DIR, BACKUP_DIR)

def reset_tests_directory():
    """Reset tests directory."""
    if os.path.exists(TESTS_DIR):
        print(f"Cleaning tests directory: {TESTS_DIR}")
        shutil.rmtree(TESTS_DIR)
    os.makedirs(TESTS_DIR)
    print(f"Clean tests directory created: {TESTS_DIR}")

def create_redoc_test():
    """Create ReDoc rendering test file."""
    with open(TEST_FILE, "w") as test_file:
        test_file.write(REDOC_TEST_CONTENT)
    print(f"Test file created: {TEST_FILE}")

def clean_build_directory():
    """Clean build directory."""
    print("Cleaning build directory...")
    subprocess.run(["swift", "package", "clean"], check=True)

def build_and_test():
    """Build and test the project."""
    print("Building and running tests...")
    subprocess.run(["swift", "build"], check=True)
    subprocess.run(["swift", "test"], check=True)

def main():
    print("Setting up test environment for ReDoc rendering...")
    backup_tests()
    reset_tests_directory()
    create_redoc_test()
    clean_build_directory()
    build_and_test()

if __name__ == "__main__":
    main()
