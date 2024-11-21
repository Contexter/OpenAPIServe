
import XCTVapor
@testable import OpenAPIServe

final class ServeOpenAPISuccessTests: XCTestCase {
    func testServeOpenAPISpec() throws {
        let app = Application(.testing)
        defer { app.shutdown() }
        try configure(app)

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertEqual(res.headers.contentType, .init("application/x-yaml"))
            XCTAssertTrue(res.body.string.contains("openapi: 3.0.0"))
        })
    }
}
