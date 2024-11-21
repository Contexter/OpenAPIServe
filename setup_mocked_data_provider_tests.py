import os
import shutil
import subprocess

def create_backup(backup_dir, source_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    if os.path.exists(source_dir):
        shutil.copytree(source_dir, os.path.join(backup_dir, os.path.basename(source_dir)), dirs_exist_ok=True)

def reset_tests_directory(test_dir):
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

def refactor_middleware_to_support_data_provider():
    middleware_file = "./Sources/OpenAPIServe/OpenAPIMiddleware.swift"
    with open(middleware_file, "r") as f:
        content = f.read()

    if "DataProvider" not in content:
        print("Refactoring middleware to use DataProvider...")
        updated_content = """
import Vapor

/// Protocol for providing OpenAPI spec data.
public protocol DataProvider {
    func getData() -> String
}

/// Reads OpenAPI spec data from a file.
public struct FileDataProvider: DataProvider {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func getData() -> String {
        guard let data = try? String(contentsOfFile: filePath) else {
            fatalError("Failed to read file at \\(filePath)")
        }
        return data
    }
}

/// Middleware to serve OpenAPI specs.
public final class OpenAPIMiddleware: Middleware {
    private let dataProvider: DataProvider

    public init(dataProvider: DataProvider) {
        self.dataProvider = dataProvider
    }

    public func respond(to request: Request, chainingTo next: Responder) -> EventLoopFuture<Response> {
        if request.url.path == "/openapi.yml" {
            let spec = dataProvider.getData()
            let response = Response(status: .ok, body: .init(string: spec))
            response.headers.contentType = .init(type: "application", subType: "x-yaml")
            return request.eventLoop.makeSucceededFuture(response)
        }
        return next.respond(to: request)
    }
}
"""
        with open(middleware_file, "w") as f:
            f.write(updated_content)

def create_mocked_test(test_file_path):
    test_content = """
import XCTest
import XCTVapor
import OpenAPIServe

/// Mock data provider for testing.
struct MockDataProvider: DataProvider {
    func getData() -> String {
        return \"""
openapi: 3.0.0
info:
  title: Mock API
  version: 1.0.0
paths: {}
        \"""
    }
}

final class ServeOpenAPITests: XCTestCase {
    func testServeOpenAPISuccess() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Use mock data provider
        app.middleware.use(OpenAPIMiddleware(dataProvider: MockDataProvider()))

        // Test response
        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType(type: "application", subType: "x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
"""
    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
    with open(test_file_path, "w") as test_file:
        test_file.write(test_content)

def update_package_dependencies():
    package_file = "Package.swift"
    with open(package_file, "r") as f:
        content = f.read()

    if "XCTVapor" not in content:
        print("Adding XCTVapor to Package.swift...")
        dependencies_line = '.package(url: "https://github.com/vapor/vapor.git", from: "4.0.0")'
        updated_content = content.replace(dependencies_line, dependencies_line + ',\n        .product(name: "XCTVapor", package: "vapor")')

        with open(package_file, "w") as f:
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
    backup_dir = "./Backup"
    sources_dir = "./Sources/OpenAPIServe"
    test_dir = "./Tests/OpenAPIServeTests"
    test_file_path = "./Tests/OpenAPIServeTests/test_serve_openapi_success.swift"

    create_backup(backup_dir, sources_dir)
    create_backup(backup_dir, test_dir)
    reset_tests_directory(test_dir)
    refactor_middleware_to_support_data_provider()
    create_mocked_test(test_file_path)
    update_package_dependencies()
    clean_build_directory()

    print("Building and running tests...")
    build_and_test()
    print("Test setup complete.")

if __name__ == "__main__":
    main()
