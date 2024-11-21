import XCTVapor
import OpenAPIServe

final class ErrorHandlingTests: XCTestCase {
    func testMissingOpenAPIFile() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider(mockContent: ""))
        defer { app.shutdown() }

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            XCTAssertEqual(res.status, .notFound)
        })
    }
}
