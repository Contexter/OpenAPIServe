
import XCTest
import XCTVapor
import OpenAPIServe

/// Mock data provider for testing.
struct MockDataProvider: DataProvider {
    func getData() -> String {
        return """
openapi: 3.0.0
info:
  title: Mock API
  version: 1.0.0
paths: {}
        """
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
