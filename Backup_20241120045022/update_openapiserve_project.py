import os

def update_package_swift():
    """Update the Package.swift file."""
    package_path = "Package.swift"
    package_content = '''// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "OpenAPIServe",
    platforms: [
        .macOS(.v12)
    ],
    products: [
        .library(name: "OpenAPIServe", targets: ["OpenAPIServe"]),
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),
        .package(url: "https://github.com/vapor/leaf.git", from: "4.0.0")
    ],
    targets: [
        .target(name: "OpenAPIServe", dependencies: [
            .product(name: "Vapor", package: "vapor"),
            .product(name: "Leaf", package: "leaf")
        ]),
        .testTarget(name: "OpenAPIServeTests", dependencies: [
            .target(name: "OpenAPIServe"),
            .product(name: "XCTVapor", package: "vapor"),
        ]),
    ]
)
'''
    with open(package_path, "w") as file:
        file.write(package_content)
    print(f"Updated {package_path}.")

def update_openapi_middleware():
    """Update the OpenAPIMiddleware.swift file."""
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
            if FileManager.default.fileExists(atPath: file) {
                return request.eventLoop.makeSucceededFuture(request.fileio.streamFile(at: file))
            } else {
                return request.eventLoop.makeSucceededFuture(
                    Response(status: .notFound, body: "File not found")
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
    """Update the RedocHandler.swift file."""
    handler_path = "Sources/OpenAPIServe/RedocHandler.swift"
    handler_content = '''import Vapor

public struct RedocHandler {
    public static func registerRoutes(
        on app: Application,
        docsPath: String = "/docs",
        specPath: String = "/openapi.yml"
    ) {
        app.get([PathComponent(stringLiteral: docsPath)]) { req -> EventLoopFuture<View> in
            req.view.render("redoc", ["specUrl": specPath])
        }
    }
}
'''
    with open(handler_path, "w") as file:
        file.write(handler_content)
    print(f"Updated {handler_path}.")

def update_openapiserve_tests():
    """Update the OpenAPIServeTests.swift file."""
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
        app.leaf.configuration = LeafConfiguration(rootDirectory: app.directory.resourcesDirectory)
        try? FileManager.default.createDirectory(
            atPath: app.directory.resourcesDirectory + "Views",
            withIntermediateDirectories: true
        )
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
            XCTAssertTrue(response.body.string.contains("<redoc spec-url=\\\"/openapi.yml\\\">"))
        }
    }
}
'''
    with open(test_path, "w") as file:
        file.write(test_content)
    print(f"Updated {test_path}.")

def main():
    """Execute all updates."""
    update_package_swift()
    update_openapi_middleware()
    update_redoc_handler()
    update_openapiserve_tests()
    print("All updates applied. Run `swift test` to verify changes.")

if __name__ == "__main__":
    main()

