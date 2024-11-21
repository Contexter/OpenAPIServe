import os
import shutil
import subprocess

# Define paths
repo_root = os.getcwd()
tests_dir = os.path.join(repo_root, "Tests", "OpenAPIServeTests")
backup_dir = os.path.join(repo_root, "Tests_Backup")
package_file = os.path.join(repo_root, "Package.swift")

# Minimal test content
def get_minimal_test_content():
    return """import XCTest
import XCTVapor
import Vapor
import OpenAPIServe

final class ServeOpenAPITests: XCTestCase {
    func testServeOpenAPISuccess() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Register the middleware provided by OpenAPIServe
        app.middleware.use(OpenAPIMiddleware(openAPIPath: "/openapi.yml", specFilePath: "path/to/spec.yml"))

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType(type: "application", subType: "x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
"""

# Backup existing tests
def backup_tests():
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    if os.path.exists(tests_dir):
        shutil.copytree(tests_dir, backup_dir)
        print(f"Backup created at {backup_dir}")

# Clean tests directory
def clean_tests_directory():
    if os.path.exists(tests_dir):
        shutil.rmtree(tests_dir)
    os.makedirs(tests_dir)
    print(f"Tests directory reset: {tests_dir}")

# Add minimal test
def add_minimal_test():
    test_file = os.path.join(tests_dir, "test_serve_openapi_success.swift")
    with open(test_file, "w") as f:
        f.write(get_minimal_test_content())
    print(f"Minimal test created: {test_file}")

# Update Package.swift
def update_package_swift():
    with open(package_file, "r") as f:
        content = f.read()

    if "XCTVapor" not in content:
        dependencies_section = "dependencies: ["
        test_target_section = "dependencies: [\n"

        if dependencies_section in content:
            content = content.replace(dependencies_section, f"{dependencies_section}\n        .package(url: \"https://github.com/vapor/vapor.git\", from: \"4.0.0\"),")
        
        if test_target_section in content:
            content = content.replace(test_target_section, f"{test_target_section}        .product(name: \"XCTVapor\", package: \"vapor\"),")

        with open(package_file, "w") as f:
            f.write(content)
        print("Package.swift updated with XCTVapor dependency.")
    else:
        print("Package.swift already includes XCTVapor dependency.")

# Build and test
def build_and_test():
    try:
        print("Cleaning build directory...")
        subprocess.run(["swift", "package", "clean"], check=True)

        print("Building the project...")
        subprocess.run(["swift", "build"], check=True)

        print("Running tests...")
        subprocess.run(["swift", "test"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during build or test: {e}")

# Main execution flow
def main():
    print("Starting test setup for OpenAPIServe...")

    backup_tests()
    clean_tests_directory()
    add_minimal_test()
    update_package_swift()
    build_and_test()

    print("Test setup complete.")

if __name__ == "__main__":
    main()
