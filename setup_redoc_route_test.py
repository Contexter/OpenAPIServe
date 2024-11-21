import os
import shutil
import subprocess

# Paths
PROJECT_ROOT = "/Users/benedikteickhoff/Development/Github-Desktop/OpenAPIServe"
TESTS_DIR = os.path.join(PROJECT_ROOT, "Tests/OpenAPIServeTests")
REDOC_TEMPLATE = os.path.join(PROJECT_ROOT, "Sources/OpenAPIServe/Resources/redoc.leaf")

def check_redoc_template():
    """Ensure the redoc.leaf template exists."""
    if not os.path.exists(REDOC_TEMPLATE):
        print("redoc.leaf template is missing. Creating a minimal template...")
        with open(REDOC_TEMPLATE, "w") as f:
            f.write(
                """\
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
  </head>
  <body>
    <redoc spec-url="{{ specURL }}"></redoc>
  </body>
</html>
"""
            )
        print(f"Created redoc.leaf template at {REDOC_TEMPLATE}")
    else:
        print("redoc.leaf template already exists.")

def create_redoc_test():
    """Create a test file for the ReDoc route."""
    test_file_path = os.path.join(TESTS_DIR, "test_redoc_rendering.swift")
    if not os.path.exists(test_file_path):
        print("Creating test file for ReDoc route...")
        with open(test_file_path, "w") as f:
            f.write(
                """\
import XCTest
import XCTVapor
@testable import OpenAPIServe

final class RedocRenderingTests: XCTestCase {
    func testRedocRendering() throws {
        let app = Application(.testing)
        defer { app.shutdown() }
        
        try configure(app)
        
        try app.test(.GET, "/docs", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertTrue(res.body.string.contains("<redoc"))
            XCTAssertTrue(res.body.string.contains("spec-url=\"/openapi.yml\""))
        })
    }
}
"""
            )
        print(f"Test file created at {test_file_path}")
    else:
        print("Test file for ReDoc route already exists.")

def clean_build_directory():
    """Clean the build directory to ensure a fresh build."""
    print("Cleaning build directory...")
    subprocess.run(["swift", "package", "clean"], check=True)

def build_and_test():
    """Build the project and run tests."""
    print("Building the project...")
    subprocess.run(["swift", "build"], check=True)
    print("Running tests...")
    subprocess.run(["swift", "test"], check=True)

def main():
    print("Setting up ReDoc route test environment...")
    check_redoc_template()
    create_redoc_test()
    clean_build_directory()
    try:
        build_and_test()
        print("Tests passed successfully.")
    except subprocess.CalledProcessError:
        print("Error during build or test.")

if __name__ == "__main__":
    main()
