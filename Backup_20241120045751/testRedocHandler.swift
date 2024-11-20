import XCTest
@testable import OpenAPIServe

final class TestRedocHandler: XCTestCase {
    func testRedocHandlerRendersLeafTemplate() throws {
        let app = try Application.testable()
        defer { app.shutdown() }
        let response = try app.test(.GET, "/docs")
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains("<redoc spec-url='/openapi.yml'>"))
    }
}
