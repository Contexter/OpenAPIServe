import os

def setup_unit_tests():
    """
    Sets up unit tests for the OpenAPIServe library:
    - Creates Tests/OpenAPIServeTests/OpenAPIServeTests.swift with tests for middleware and handlers.
    """

    # Define paths
    tests_dir = "Tests/OpenAPIServeTests"
    test_file = os.path.join(tests_dir, "OpenAPIServeTests.swift")

    # Ensure the Tests directory exists
    os.makedirs(tests_dir, exist_ok=True)

    # Unit test content
    test_content = '''import XCTest
import Vapor
import Leaf
@testable import OpenAPIServe

final class OpenAPIServeTests: XCTestCase {
    var app: Application!

    override func setUp() async throws {
        app = Application(.testing)
        app.views.use(.leaf) // Use Leaf for rendering templates
        try await super.setUp()
    }

    override func tearDown() async throws {
        app.shutdown()
        try await super.tearDown()
    }

    func testOpenAPIMiddlewareServesSpecFile() async throws {
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
        let response = try await app.testable().test(.GET, "/openapi.yml")

        // Assert: Ensure response contains the OpenAPI spec content
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains("openapi: 3.1.0"))
    }

    func testOpenAPIMiddlewareFileNotFound() async throws {
        // Arrange: Middleware with missing file
        app.middleware.use(OpenAPIMiddleware(filePath: "Resources/OpenAPI/openapi.yml"))

        // Act: Simulate a request to /openapi.yml
        let response = try await app.testable().test(.GET, "/openapi.yml")

        // Assert: Expect a 404 Not Found response
        XCTAssertEqual(response.status, .notFound)
    }

    func testRedocHandlerRendersLeafTemplate() async throws {
        // Arrange: Add the ReDoc handler
        RedocHandler.registerRoutes(on: app, docsPath: "/docs", specPath: "/openapi.yml")

        // Act: Simulate a request to /docs
        let response = try await app.testable().test(.GET, "/docs")

        // Assert: Ensure ReDoc page is rendered
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains("<redoc spec-url=\\"/openapi.yml\\">"))
    }
}
'''

    # Write the test content
    with open(test_file, "w") as file:
        file.write(test_content)
    print(f"Created unit test file at: {test_file}")

# Execute the script
if __name__ == "__main__":
    setup_unit_tests()

