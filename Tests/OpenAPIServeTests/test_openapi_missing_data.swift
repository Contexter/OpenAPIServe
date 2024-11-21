import XCTest
import XCTVapor
@testable import OpenAPIServe

final class MissingDataTests: XCTestCase {
    func testMissingOpenAPIData() throws {
        let app = Application(.testing)
        defer { app.shutdown() }
        
        // Mock DataProvider that provides empty data
        struct EmptyDataProvider: DataProvider {
            func getData() -> String {
                return ""
            }
        }
        
        // Register middleware with EmptyDataProvider
        app.middleware.use(OpenAPIMiddleware(dataProvider: EmptyDataProvider()))
        
        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .notFound, "Expected 404 Not Found for missing OpenAPI data")
            XCTAssertTrue(res.body.string.contains("OpenAPI specification not found"), 
                          "Expected error message in response body")
        })
    }
}
