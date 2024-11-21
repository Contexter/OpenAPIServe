import XCTVapor
import OpenAPIServe

final class RedocTests: XCTestCase {
    func testRedocRenderingOpenAPI30() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider.openAPI30())
        defer { app.shutdown() }

        try app.test(.GET, "docs", afterResponse: { res in
            TestAssertions.assertOKResponse(res, contains: "<redoc")
        })
    }

    func testRedocRenderingOpenAPI31() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider.openAPI31())
        defer { app.shutdown() }

        try app.test(.GET, "docs", afterResponse: { res in
            TestAssertions.assertOKResponse(res, contains: "openapi: 3.1.0")
        })
    }
}
