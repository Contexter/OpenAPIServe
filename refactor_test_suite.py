import os
import shutil
import subprocess

# Define constants for directories and file paths
PROJECT_DIR = "/Users/benedikteickhoff/Development/Github-Desktop/OpenAPIServe"
TESTS_DIR = os.path.join(PROJECT_DIR, "Tests/OpenAPIServeTests")
UTILITIES_DIR = os.path.join(TESTS_DIR, "Utilities")
BACKUP_DIR = os.path.join(PROJECT_DIR, "Tests_Backup")
TEST_FILES = [
    "RedocTests.swift",
    "OpenAPISpecTests.swift",
    "ErrorHandlingTests.swift"
]

# Utilities content
MOCK_DATA_PROVIDER = """\
import Vapor
import OpenAPIServe

struct MockDataProvider: DataProvider {
    let mockContent: String

    func getData() -> String {
        return mockContent
    }

    static func openAPI30() -> MockDataProvider {
        return MockDataProvider(mockContent: "openapi: 3.0.0")
    }

    static func openAPI31() -> MockDataProvider {
        return MockDataProvider(mockContent: "openapi: 3.1.0")
    }
}
"""

TEST_APP_CONFIGURATOR = """\
import Vapor
import OpenAPIServe

struct TestAppConfigurator {
    static func configureApp(
        with dataProvider: DataProvider
    ) -> Application {
        let app = Application(.testing)
        app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))
        return app
    }
}
"""

TEST_ASSERTIONS = """\
import XCTVapor

struct TestAssertions {
    static func assertOKResponse(
        _ response: XCTHTTPResponse,
        contains expectedContent: String
    ) {
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains(expectedContent))
    }
}
"""

# Test file content
REDOC_TESTS = """\
import XCTVapor
import OpenAPIServe

final class RedocTests: XCTestCase {
    func testRedocRenderingOpenAPI30() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider.openAPI30())
        defer { app.shutdown() }

        try app.test(.GET, "docs", afterResponse: { res in
            TestAssertions.assertOKResponse(res, contains: "<redoc")
        })
    }

    func testRedocRenderingOpenAPI31() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider.openAPI31())
        defer { app.shutdown() }

        try app.test(.GET, "docs", afterResponse: { res in
            TestAssertions.assertOKResponse(res, contains: "openapi: 3.1.0")
        })
    }
}
"""

OPENAPI_SPEC_TESTS = """\
import XCTVapor
import OpenAPIServe

final class OpenAPISpecTests: XCTestCase {
    func testOpenAPISpecParsing() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider.openAPI30())
        defer { app.shutdown() }

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            TestAssertions.assertOKResponse(res, contains: "openapi: 3.0.0")
        })
    }
}
"""

ERROR_HANDLING_TESTS = """\
import XCTVapor
import OpenAPIServe

final class ErrorHandlingTests: XCTestCase {
    func testMissingOpenAPIFile() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider(mockContent: ""))
        defer { app.shutdown() }

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .notFound)
        })
    }
}
"""

# Function to back up the existing test directory
def backup_tests():
    if os.path.exists(BACKUP_DIR):
        print(f"Removing existing backup: {BACKUP_DIR}")
        shutil.rmtree(BACKUP_DIR)
    print(f"Backing up existing tests to {BACKUP_DIR}")
    shutil.copytree(TESTS_DIR, BACKUP_DIR)

# Function to set up utilities
def setup_utilities():
    if not os.path.exists(UTILITIES_DIR):
        os.makedirs(UTILITIES_DIR)
    print(f"Creating utilities in {UTILITIES_DIR}")
    with open(os.path.join(UTILITIES_DIR, "MockDataProvider.swift"), "w") as f:
        f.write(MOCK_DATA_PROVIDER)
    with open(os.path.join(UTILITIES_DIR, "TestAppConfigurator.swift"), "w") as f:
        f.write(TEST_APP_CONFIGURATOR)
    with open(os.path.join(UTILITIES_DIR, "TestAssertions.swift"), "w") as f:
        f.write(TEST_ASSERTIONS)

# Function to create test files
def create_test_files():
    print(f"Creating test files in {TESTS_DIR}")
    for filename, content in [
        ("RedocTests.swift", REDOC_TESTS),
        ("OpenAPISpecTests.swift", OPENAPI_SPEC_TESTS),
        ("ErrorHandlingTests.swift", ERROR_HANDLING_TESTS),
    ]:
        with open(os.path.join(TESTS_DIR, filename), "w") as f:
            f.write(content)

# Function to clean the build directory
def clean_build_directory():
    build_dir = os.path.join(PROJECT_DIR, ".build")
    if os.path.exists(build_dir):
        print(f"Cleaning build directory: {build_dir}")
        shutil.rmtree(build_dir)

# Function to build and test
def build_and_test():
    print("Building and running tests...")
    try:
        subprocess.run(["swift", "test"], check=True, cwd=PROJECT_DIR)
        print("Tests passed successfully.")
    except subprocess.CalledProcessError:
        print("Error during build or test.")

# Main script execution
def main():
    backup_tests()
    setup_utilities()
    create_test_files()
    clean_build_directory()
    build_and_test()

if __name__ == "__main__":
    main()

