import XCTest
import XCTVapor
@testable import OpenAPIServe

// MockDataProvider that returns no content
struct EmptyDataProvider: DataProvider {
    func getData() -> String {
        return ""
    }
}

final class MissingDataTests: XCTestCase {
    func testMissingOpenAPIData() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Use EmptyDataProvider
        let dataProvider = EmptyDataProvider()
        app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .notFound, "Expected 404 Not Found for missing OpenAPI data")
            XCTAssertTrue(res.body.string.contains("OpenAPI specification not found"))
        })
    }
}
