import os

def write_to_file(file_path, content):
    """Write content to a file only if it differs from the current content."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            current_content = file.read()
        if current_content == content:
            print(f"No changes needed for {file_path}.")
            return
    with open(file_path, "w") as file:
        file.write(content)
    print(f"Updated {file_path} successfully.")

def update_redoc_handler():
    """Fix the RedocHandler.swift file."""
    handler_path = "Sources/OpenAPIServe/RedocHandler.swift"
    handler_content = '''import Vapor

public struct RedocHandler {
    public static func registerRoutes(
        on app: Application,
        docsPath: String = "/docs",
        specPath: String = "/openapi.yml"
    ) {
        app.get([PathComponent(stringLiteral: docsPath)]) { req -> EventLoopFuture<View> in
            let leafPath = app.directory.resourcesDirectory + "Views/redoc.leaf"
            print("Looking for Leaf template at:", leafPath)
            print("Template exists:", FileManager.default.fileExists(atPath: leafPath))
            guard FileManager.default.fileExists(atPath: leafPath) else {
                return req.eventLoop.future(error: Abort(.notFound, reason: "Template not found"))
            }
            return req.view.render("redoc", ["specUrl": specPath])
        }
    }
}
'''
    write_to_file(handler_path, handler_content)

def update_tests():
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
        // Create necessary directories
        let viewsPath = app.directory.resourcesDirectory + "Views"
        try? FileManager.default.createDirectory(atPath: viewsPath, withIntermediateDirectories: true)
        let openapiPath = app.directory.resourcesDirectory + "OpenAPI"
        try? FileManager.default.createDirectory(atPath: openapiPath, withIntermediateDirectories: true)

        // Write mock redoc.leaf template
        let redocLeafPath = viewsPath + "/redoc.leaf"
        let redocTemplate = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Documentation</title>
        </head>
        <body>
            <redoc spec-url="{{ specUrl }}"></redoc>
        </body>
        </html>
        """
        try? redocTemplate.write(toFile: redocLeafPath, atomically: true, encoding: .utf8)
    }

    override func tearDown() {
        app.shutdown()
    }

    func testOpenAPIMiddlewareServesSpecFile() throws {
        // Arrange
        let mockFilePath = app.directory.resourcesDirectory + "OpenAPI/openapi.yml"
        let mockContent = "openapi: 3.1.0\\ninfo:\\n  title: Test API\\n  version: 1.0.0\\npaths: {}"
        try mockContent.write(toFile: mockFilePath, atomically: true, encoding: .utf8)

        app.middleware.use(OpenAPIMiddleware(filePath: "OpenAPI/openapi.yml"))

        // Act
        try app.test(.GET, "/openapi.yml") { response in
            XCTAssertEqual(response.status, .ok)
            XCTAssertTrue(response.body.string.contains("openapi: 3.1.0"))
        }
    }

    func testOpenAPIMiddlewareFileNotFound() throws {
        // Arrange
        app.middleware.use(OpenAPIMiddleware(filePath: "OpenAPI/missing.yml"))

        // Act
        try app.test(.GET, "/openapi.yml") { response in
            XCTAssertEqual(response.status, .notFound)
            XCTAssertTrue(response.body.string.contains("File not found"))
        }
    }

    func testRedocHandlerRendersLeafTemplate() throws {
        // Arrange
        let redocLeafPath = app.directory.resourcesDirectory + "Views/redoc.leaf"
        let redocTemplate = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Documentation</title>
        </head>
        <body>
            <redoc spec-url="{{ specUrl }}"></redoc>
        </body>
        </html>
        """
        try? redocTemplate.write(toFile: redocLeafPath, atomically: true, encoding: .utf8)

        RedocHandler.registerRoutes(on: app, docsPath: "/docs", specPath: "/openapi.yml")

        // Act
        try app.test(.GET, "/docs") { response in
            XCTAssertEqual(response.status, .ok)
            XCTAssertTrue(response.body.string.contains("<redoc spec-url=\\"/openapi.yml\\">"))
        }
    }
}
'''
    write_to_file(test_path, test_content)

def main():
    """Apply fixes and ensure changes are applied successfully."""
    print("Starting the update process...")
    try:
        update_redoc_handler()
        update_tests()
        print("All updates applied successfully. You can now build and test the project.")
    except Exception as e:
        print(f"An error occurred during the update process: {e}")

if __name__ == "__main__":
    main()

