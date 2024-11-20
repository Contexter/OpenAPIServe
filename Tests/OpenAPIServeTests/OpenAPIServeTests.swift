import XCTVapor
import Leaf
@testable import OpenAPIServe

final class OpenAPIServeTests: XCTestCase {
    var app: Application!

    override func setUp() {
        super.setUp()
        app = Application(.testing)
        app.views.use(.leaf)

        // Define paths
        let resourcesPath = app.directory.resourcesDirectory
        let viewsPath = resourcesPath + "Views/"
        let openapiPath = resourcesPath + "OpenAPI/"

        // Print paths for debugging
        print("Resources Directory: \(resourcesPath)")

        // Ensure directories exist
        try? FileManager.default.createDirectory(atPath: viewsPath, withIntermediateDirectories: true)
        try? FileManager.default.createDirectory(atPath: openapiPath, withIntermediateDirectories: true)

        // Write ReDoc template if not already written
        let redocLeafPath = viewsPath + "redoc.leaf"
        if !FileManager.default.fileExists(atPath: redocLeafPath) {
            print("Writing ReDoc template to: \(redocLeafPath)")
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
            assert(FileManager.default.fileExists(atPath: redocLeafPath), "ReDoc template not written.")
        }

        // Write OpenAPI spec if not already written
        let openapiSpecPath = openapiPath + "openapi.yml"
        if !FileManager.default.fileExists(atPath: openapiSpecPath) {
            print("Writing OpenAPI spec to: \(openapiSpecPath)")
            let openAPISpec = """
            openapi: 3.1.0
            info:
              title: Test API
              version: 1.0.0
            paths: {}
            """
            try? openAPISpec.write(toFile: openapiSpecPath, atomically: true, encoding: .utf8)
            assert(FileManager.default.fileExists(atPath: openapiSpecPath), "OpenAPI spec not written.")
        }
    }

    override func tearDown() {
        app.shutdown()
        super.tearDown()
    }

    func testOpenAPIMiddlewareFileNotFound() throws {
        let missingFilePath = app.directory.resourcesDirectory + "OpenAPI/missing.yml"
        print("Testing with missing file path: \(missingFilePath)")
        app.middleware.use(OpenAPIMiddleware(filePath: missingFilePath))

        try app.test(.GET, "/openapi.yml") { response in
            XCTAssertEqual(response.status, .notFound)
        }
    }

    func testOpenAPIMiddlewareServesSpecFile() throws {
        let openapiFilePath = app.directory.resourcesDirectory + "OpenAPI/openapi.yml"
        print("Testing with OpenAPI file path: \(openapiFilePath)")
        app.middleware.use(OpenAPIMiddleware(filePath: openapiFilePath))

        try app.test(.GET, "/openapi.yml") { response in
            XCTAssertEqual(response.status, .ok)
            XCTAssertEqual(response.headers.contentType, .yaml)
            XCTAssertTrue(response.body.string.contains("openapi: 3.1.0"))
        }
    }

    func testRedocHandlerRendersLeafTemplate() throws {
        RedocHandler.registerRoutes(on: app, docsPath: "/docs", specPath: "/openapi.yml")

        try app.test(.GET, "/docs") { response in
            XCTAssertEqual(response.status, .ok)
            XCTAssertEqual(response.headers.contentType, .html)
            XCTAssertTrue(response.body.string.contains("<redoc spec-url='/openapi.yml'>"))
        }
    }
}

extension HTTPMediaType {
    static var yaml: HTTPMediaType {
        HTTPMediaType(type: "application", subType: "x-yaml")
    }
}
