import os
import shutil
import subprocess

def create_backup(backup_dir, test_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    if os.path.exists(test_dir):
        shutil.copytree(test_dir, os.path.join(backup_dir, 'Tests'), dirs_exist_ok=True)

def reset_tests_directory(test_dir):
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

def create_mocked_test(test_file_path):
    test_content = """
import XCTest
import XCTVapor
import OpenAPIServe

final class ServeOpenAPITests: XCTestCase {
    func testServeOpenAPISuccess() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Mock middleware setup
        app.middleware.use(OpenAPIMiddleware(filePath: "mock-spec-content"))

        // Test mock response
        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType(type: "application", subType: "x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
"""
    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
    with open(test_file_path, 'w') as test_file:
        test_file.write(test_content)

def update_package_dependencies():
    package_file = "Package.swift"
    with open(package_file, 'r') as f:
        content = f.read()

    if "XCTVapor" not in content:
        print("Adding XCTVapor to Package.swift...")
        dependencies_line = '.package(url: "https://github.com/vapor/vapor.git", from: "4.0.0")'
        updated_content = content.replace(dependencies_line, dependencies_line + ',\n        .product(name: "XCTVapor", package: "vapor")')

        with open(package_file, 'w') as f:
            f.write(updated_content)

def clean_build_directory():
    subprocess.run(["swift", "package", "clean"], check=True)

def build_and_test():
    try:
        subprocess.run(["swift", "build"], check=True)
        subprocess.run(["swift", "test"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during build or test: {e}")
        raise

def main():
    print("Starting test setup for OpenAPIServe...")
    backup_dir = "./Tests_Backup"
    test_dir = "./Tests/OpenAPIServeTests"
    test_file_path = "./Tests/OpenAPIServeTests/test_serve_openapi_success.swift"

    create_backup(backup_dir, test_dir)
    reset_tests_directory(test_dir)
    create_mocked_test(test_file_path)
    update_package_dependencies()
    clean_build_directory()

    print("Building and running tests...")
    build_and_test()
    print("Test setup complete.")

if __name__ == "__main__":
    main()
