import XCTVapor
@testable import OpenAPIServe

// MockDataProvider conforming to DataProvider protocol
struct MockDataProvider: DataProvider {
    let mockContent: String
    
    func getData() -> String {
        return mockContent
    }
}

final class ServeOpenAPITests: XCTestCase {
    func testServeOpenAPISuccess() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        let dataProvider = MockDataProvider(mockContent: "openapi: 3.0.0")
        app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, HTTPMediaType(type: "application", subType: "x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
