import XCTest
@testable import OpenAPIServe

final class TestServeSpecFile: XCTestCase {
    func testOpenAPIMiddlewareServesSpecFile() throws {
        let app = try Application.testable()
        defer { app.shutdown() }
        let response = try app.test(.GET, "/openapi.yml")
        XCTAssertEqual(response.status, .ok)
        XCTAssertEqual(response.headers.contentType, .init(type: "application", subType: "x-yaml"))
        XCTAssertTrue(response.body.string.contains("openapi: 3.1.0"))
    }
}
