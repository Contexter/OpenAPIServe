import os
import shutil
import subprocess

# Paths
PROJECT_ROOT = os.getcwd()
TESTS_DIR = os.path.join(PROJECT_ROOT, "Tests", "OpenAPIServeTests")
TEST_FILE = os.path.join(TESTS_DIR, "test_valid_openapi_spec.swift")
BUILD_DIR = os.path.join(PROJECT_ROOT, ".build")

def create_test_environment():
    """Ensures the test environment is ready."""
    if not os.path.exists(TESTS_DIR):
        os.makedirs(TESTS_DIR)
        print(f"Created test directory: {TESTS_DIR}")

def clean_build_directory():
    """Cleans the build directory."""
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
        print("Build directory cleaned.")

def create_valid_openapi_test():
    """Creates the test file for valid OpenAPI spec handling."""
    test_content = """
    import XCTVapor
    import OpenAPIServe

    final class ValidOpenAPITests: XCTestCase {
        func testValidOpenAPISpec() throws {
            let app = Application(.testing)
            defer { app.shutdown() }

            // Mocked FileDataProvider with valid OpenAPI spec
            let dataProvider = MockDataProvider(mockContent: "openapi: 3.0.0")
            app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))

            try app.test(.GET, "/openapi.yml", afterResponse: { res in
                XCTAssertEqual(res.status, .ok, "Expected 200 OK for valid OpenAPI data")
                XCTAssertEqual(res.headers.contentType, .init(type: "application", subType: "x-yaml"))
                XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
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
    with open(TEST_FILE, "w") as file:
        file.write(test_content)
    print(f"Test file created: {TEST_FILE}")

def build_and_test():
    """Builds the project and runs the tests."""
    try:
        subprocess.run(["swift", "build"], check=True)
        print("Build succeeded.")
        subprocess.run(["swift", "test"], check=True)
        print("Tests passed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during build or test: {e}")

def main():
    """Main function to set up the test environment."""
    print("Setting up test environment...")
    create_test_environment()
    create_valid_openapi_test()
    clean_build_directory()
    print("Building and running tests...")
    build_and_test()

if __name__ == "__main__":
    main()
