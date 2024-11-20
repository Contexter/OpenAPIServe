import XCTest
import Vapor
@testable import OpenAPIServe

final class TestFileNotFound: XCTestCase {
    func testOpenAPIMiddlewareFileNotFound() throws {
        // Initialize the application in testing mode
        let app = Application(.testing)
        defer { app.shutdown() }
        
        // Perform GET request to "/openapi.yml"
        let response = try app.testable().test(.GET, "/openapi.yml")
        
        // Assert that the response status is HTTP 404 Not Found
        XCTAssertEqual(response.status, .notFound)
    }
}
