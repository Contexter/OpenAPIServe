import os
import subprocess
import shutil

# Paths for directories and files
TESTS_DIR = "Tests/OpenAPIServeTests"
BACKUP_DIR = "Tests_Backup"
MISSING_DATA_TEST_FILE = os.path.join(TESTS_DIR, "test_openapi_missing_data.swift")

def create_missing_data_test():
    """
    Create a test file for handling missing OpenAPI data.
    """
    print(f"Creating missing data test: {MISSING_DATA_TEST_FILE}")
    test_content = '''import XCTest
import XCTVapor
@testable import OpenAPIServe

final class MissingDataTests: XCTestCase {
    func testMissingOpenAPIData() throws {
        let app = Application(.testing)
        defer { app.shutdown() }
        
        // Mock DataProvider that provides empty data
        struct EmptyDataProvider: DataProvider {
            func getData() -> String {
                return ""
            }
        }
        
        // Register middleware with EmptyDataProvider
        app.middleware.use(OpenAPIMiddleware(dataProvider: EmptyDataProvider()))
        
        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .notFound, "Expected 404 Not Found for missing OpenAPI data")
            XCTAssertTrue(res.body.string.contains("OpenAPI specification not found"), 
                          "Expected error message in response body")
        })
    }
}
'''
    with open(MISSING_DATA_TEST_FILE, "w") as test_file:
        test_file.write(test_content)
    print(f"Test file created: {MISSING_DATA_TEST_FILE}")

def clean_build_directory():
    """
    Clean the Swift build directory.
    """
    print("Cleaning build directory...")
    if os.path.exists(".build"):
        shutil.rmtree(".build")
    print("Build directory cleaned.")

def build_and_test():
    """
    Run the Swift build and test commands.
    """
    print("Building and running tests...")
    try:
        subprocess.run(["swift", "build"], check=True)
        subprocess.run(["swift", "test"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during build or test: {e}")
        raise

def main():
    """
    Main function to set up and run the missing data test.
    """
    print("Setting up missing data test...")
    
    # Backup the existing tests directory if it exists
    if os.path.exists(TESTS_DIR):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        backup_path = os.path.join(BACKUP_DIR, "OpenAPIServeTests")
        if os.path.exists(backup_path):
            print(f"Removing existing backup: {backup_path}")
            shutil.rmtree(backup_path)
        shutil.move(TESTS_DIR, backup_path)
        print(f"Backup created at {BACKUP_DIR}")

    # Create a fresh test directory
    os.makedirs(TESTS_DIR, exist_ok=True)
    print(f"Clean test directory created: {TESTS_DIR}")
    
    # Create the missing data test
    create_missing_data_test()
    
    # Clean the build directory
    clean_build_directory()
    
    # Build and run tests
    build_and_test()
    print("Missing data test setup complete.")

if __name__ == "__main__":
    main()
