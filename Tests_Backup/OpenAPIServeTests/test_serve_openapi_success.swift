import XCTest
import XCTVapor
import Vapor
import OpenAPIServe

final class ServeOpenAPITests: XCTestCase {
    func testServeOpenAPISuccess() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Register the middleware with the correct absolute file path
        app.middleware.use(OpenAPIMiddleware(filePath: "/Users/benedikteickhoff/Development/Github-Desktop/OpenAPIServe/Tests/OpenAPIServeTests/Resources/spec.yml"))

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType(type: "application", subType: "x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
