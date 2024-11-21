
import XCTest
import XCTVapor
import OpenAPIServe

final class ServeOpenAPITests: XCTestCase {
    func testServeOpenAPISuccess() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Mock middleware setup
        app.middleware.use(OpenAPIMiddleware(filePath: "mock-spec-content"))

        // Test mock response
        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType("application/x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
