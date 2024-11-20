
import XCTVapor
import Leaf
@testable import OpenAPIServe

final class OpenAPIServeTests: XCTestCase {
    var app: Application!

    override func setUp() {
        app = Application(.testing)
        app.views.use(.leaf)

        // Log the Views path
        print("Leaf template directory:", app.directory.resourcesDirectory + "Views")

        // Ensure necessary directories exist
        let viewsPath = app.directory.resourcesDirectory + "Views"
        let openapiPath = app.directory.resourcesDirectory + "OpenAPI"
        try? FileManager.default.createDirectory(atPath: viewsPath, withIntermediateDirectories: true)
        try? FileManager.default.createDirectory(atPath: openapiPath, withIntermediateDirectories: true)

        // Write mock ReDoc Leaf template
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

        // Log all registered routes
        app.routes.all.forEach { route in
            print("Registered route: \(route.description)")
        }
    }

    override func tearDown() {
        app.shutdown()
    }

    func testOpenAPIMiddlewareFileNotFound() throws {
        app.middleware.use(OpenAPIMiddleware(filePath: "Resources/OpenAPI/missing.yml"))

        let response = try app.testable().test(.GET, "/openapi.yml")
        XCTAssertEqual(response.status, .notFound)
    }

    func testOpenAPIMiddlewareServesSpecFile() throws {
        let mockFilePath = app.directory.resourcesDirectory + "OpenAPI/openapi.yml"
        let openAPISpec = """
openapi: 3.1.0
info:
  title: Test API
  version: 1.0.0
paths: {}
"""
        try openAPISpec.write(toFile: mockFilePath, atomically: true, encoding: .utf8)

        app.middleware.use(OpenAPIMiddleware(filePath: "Resources/OpenAPI/openapi.yml"))

        let response = try app.testable().test(.GET, "/openapi.yml")
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains("openapi: 3.1.0"))
    }

    func testRedocHandlerRendersLeafTemplate() throws {
        RedocHandler.registerRoutes(on: app, docsPath: "/docs", specPath: "/openapi.yml")

        let response = try app.testable().test(.GET, "/docs")
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains("<redoc spec-url='/openapi.yml'>"))
    }
}
