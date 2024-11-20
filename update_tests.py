import os

def update_openapiserve_tests():
    """Fix the OpenAPIServeTests.swift file."""
    test_path = "Tests/OpenAPIServeTests/OpenAPIServeTests.swift"
    test_content = '''import XCTest
import XCTVapor
import Leaf
@testable import OpenAPIServe

final class OpenAPIServeTests: XCTestCase {
    var app: Application!

    override func setUp() {
        app = Application(.testing)
        app.views.use(.leaf)
        // Ensure the Views directory exists
        let viewsPath = app.directory.resourcesDirectory + "Views"
        try? FileManager.default.createDirectory(atPath: viewsPath, withIntermediateDirectories: true)
    }

    override func tearDown() {
        app.shutdown()
    }

    func testOpenAPIMiddlewareServesSpecFile() throws {
        // Arrange: Mock the OpenAPI file
        let mockFilePath = app.directory.workingDirectory + "Resources/OpenAPI/openapi.yml"
        try FileManager.default.createDirectory(
            atPath: app.directory.resourcesDirectory + "OpenAPI",
            withIntermediateDirectories: true
        )
        try "openapi: 3.1.0\\ninfo:\\n  title: Test API\\n  version: 1.0.0\\npaths: {}".write(
            toFile: mockFilePath,
            atomically: true,
            encoding: .utf8
        )

        app.middleware.use(OpenAPIMiddleware(filePath: "Resources/OpenAPI/openapi.yml"))

        // Act: Simulate a request to /openapi.yml
        try app.test(.GET, "/openapi.yml") { response in
            // Assert: Ensure response contains the OpenAPI spec content
            XCTAssertEqual(response.status, .ok)
            XCTAssertTrue(response.body.string.contains("openapi: 3.1.0"))
        }
    }

    func testOpenAPIMiddlewareFileNotFound() throws {
        // Arrange: Middleware with missing file
        app.middleware.use(OpenAPIMiddleware(filePath: "Resources/OpenAPI/openapi.yml"))

        // Act: Simulate a request to /openapi.yml
        try app.test(.GET, "/openapi.yml") { response in
            // Assert: Expect a 404 Not Found response
            XCTAssertEqual(response.status, .notFound)
            XCTAssertTrue(response.body.string.contains("File not found"))
        }
    }

    func testRedocHandlerRendersLeafTemplate() throws {
        // Arrange: Add the ReDoc handler
        RedocHandler.registerRoutes(on: app, docsPath: "/docs", specPath: "/openapi.yml")

        // Create a mock Leaf template
        let redocLeafPath = app.directory.resourcesDirectory + "Views/redoc.leaf"
        try """
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Documentation</title>
        </head>
        <body>
            <redoc spec-url="{{ specUrl }}"></redoc>
        </body>
        </html>
        """.write(toFile: redocLeafPath, atomically: true, encoding: .utf8)

        // Act: Simulate a request to /docs
        try app.test(.GET, "/docs") { response in
            // Assert: Ensure ReDoc page is rendered
            XCTAssertEqual(response.status, .ok)
            XCTAssertTrue(response.body.string.contains("<redoc spec-url=\\"/openapi.yml\\">"))
        }
    }
}
'''
    # Write the updated content to the test file
    with open(test_path, "w") as file:
        file.write(test_content)
    print(f"Updated test file at: {test_path}")

def main():
    """Execute the test file update."""
    update_openapiserve_tests()
    print("Test file updated successfully. Run `swift test` to verify changes.")

if __name__ == "__main__":
    main()

