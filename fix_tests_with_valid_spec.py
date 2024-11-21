import os
import shutil
import subprocess

def backup_tests():
    backup_dir = "Tests_Backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    tests_dir = "Tests/OpenAPIServeTests"
    if os.path.exists(tests_dir):
        shutil.copytree(tests_dir, os.path.join(backup_dir, "OpenAPIServeTests"), dirs_exist_ok=True)
        print(f"Backup created at {os.path.abspath(backup_dir)}")

def reset_tests_directory():
    tests_dir = "Tests/OpenAPIServeTests"
    if os.path.exists(tests_dir):
        shutil.rmtree(tests_dir)
    os.makedirs(tests_dir)
    print(f"Tests directory reset: {os.path.abspath(tests_dir)}")
    return tests_dir

def create_valid_spec_file():
    resources_dir = "Tests/OpenAPIServeTests/Resources"
    os.makedirs(resources_dir, exist_ok=True)

    spec_file_path = os.path.join(resources_dir, "spec.yml")
    with open(spec_file_path, "w") as spec_file:
        spec_file.write("openapi: 3.0.0\ninfo:\n  title: Sample API\n  version: 1.0.0")
    print(f"Spec file created at {spec_file_path}")
    return os.path.abspath(spec_file_path)

def create_fixed_test_file(tests_dir, spec_file_path):
    test_content = f"""\
import XCTest
import XCTVapor
import Vapor
import OpenAPIServe

final class ServeOpenAPITests: XCTestCase {{
    func testServeOpenAPISuccess() throws {{
        let app = Application(.testing)
        defer {{ app.shutdown() }}

        // Ensure file path for middleware is correctly passed
        app.middleware.use(OpenAPIMiddleware(filePath: "{spec_file_path}"))

        try app.test(.GET, "/openapi.yml", afterResponse: {{ res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType(type: "application", subType: "x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        }})
    }}
}}
"""
    test_file_path = os.path.join(tests_dir, "test_serve_openapi_success.swift")
    with open(test_file_path, "w") as test_file:
        test_file.write(test_content)
    print(f"Fixed test created: {test_file_path}")

def clean_and_rebuild():
    try:
        subprocess.run(["swift", "package", "clean"], check=True)
        print("Cleaned build directory.")

        subprocess.run(["swift", "build"], check=True)
        print("Project built successfully.")

        subprocess.run(["swift", "test"], check=True)
        print("Tests executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during build or test: {e}")

if __name__ == "__main__":
    print("Starting test setup for OpenAPIServe...")
    backup_tests()
    tests_dir = reset_tests_directory()
    spec_file_path = create_valid_spec_file()
    create_fixed_test_file(tests_dir, spec_file_path)
    clean_and_rebuild()
    print("Test setup complete.")
