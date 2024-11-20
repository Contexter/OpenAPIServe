import os

def update_openapi_middleware():
    """Fix the OpenAPIMiddleware.swift file."""
    middleware_path = "Sources/OpenAPIServe/OpenAPIMiddleware.swift"
    middleware_content = '''import Vapor

public struct OpenAPIMiddleware: Middleware {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func respond(to request: Request, chainingTo next: Responder) -> EventLoopFuture<Response> {
        if request.url.path == "/openapi.yml" {
            let file = request.application.directory.resourcesDirectory + filePath
            print("Looking for file at:", file)
            print("File exists:", FileManager.default.fileExists(atPath: file))
            if FileManager.default.fileExists(atPath: file) {
                return request.fileio.streamFile(at: file).map { Response(status: .ok, body: $0.body) }
            } else {
                return request.eventLoop.makeSucceededFuture(
                    Response(status: .notFound, body: Response.Body(string: "File not found"))
                )
            }
        } else {
            return next.respond(to: request)
        }
    }
}
'''
    with open(middleware_path, "w") as file:
        file.write(middleware_content)
    print(f"Updated {middleware_path}.")

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
        app.get(docsPath) { req -> EventLoopFuture<View> in
            let leafPath = app.directory.resourcesDirectory + "Views/redoc.leaf"
            print("Looking for Leaf template at:", leafPath)
            print("Template exists:", FileManager.default.fileExists(atPath: leafPath))
            guard FileManager.default.fileExists(atPath: leafPath) else {
                return req.eventLoop.makeSucceededFuture(Response(status: .notFound, body: "Template not found"))
            }
            return req.view.render("redoc", ["specUrl": specPath])
        }
    }
}
'''
    with open(handler_path, "w") as file:
        file.write(handler_content)
    print(f"Updated {handler_path}.")

def update_openapiserve_tests():
    """Fix the OpenAPIServeTests.swift file with proper debugging."""
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
        let viewsPath = app.directory.resourcesDirectory + "Views"
        try? FileManager.default.createDirectory(atPath: viewsPath, withIntermediateDirectories: true)
        let openapiPath = app.directory.resourcesDirectory + "OpenAPI"
        try? FileManager.default.createDirectory(atPath: openapiPath, withIntermediateDirectories: true)
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
        try redocTemplate.write(toFile: redocLeafPath, atomically: true, encoding: .utf8)

        RedocHandler.registerRoutes(on: app, docsPath: "/docs", specPath: "/openapi.yml")

        // Act
        try app.test(.GET, "/docs") { response in
            XCTAssertEqual(response.status, .ok)
            XCTAssertTrue(response.body.string.contains("<redoc spec-url=\\"/openapi.yml\\">"))
        }
    }
}
'''
    with open(test_path, "w") as file:
        file.write(test_content)
    print(f"Updated {test_path}.")

def main():
    """Execute all updates."""
    update_openapi_middleware()
    update_redoc_handler()
    update_openapiserve_tests()
    print("All updates applied. Run `swift test` to verify changes.")

if __name__ == "__main__":
    main()

