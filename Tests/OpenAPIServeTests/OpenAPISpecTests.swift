import XCTVapor
import OpenAPIServe

final class OpenAPISpecTests: XCTestCase {
    func testOpenAPISpecParsing() throws {
        let app = TestAppConfigurator.configureApp(with: MockDataProvider.openAPI30())
        defer { app.shutdown() }

        try app.test(.GET, "/openapi.yml", afterResponse: { res in
            TestAssertions.assertOKResponse(res, contains: "openapi: 3.0.0")
        })
    }
}
