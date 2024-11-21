
import XCTVapor
import OpenAPIServe
import Utilities

func testRedocRenderingForOpenAPI31() throws {
    let app = Application(.testing)
    defer { app.shutdown() }

    // Configure Leaf to use Resources/Views
    app.views.use(.leaf)
    app.leaf.sources = .singleSource(NioLeafFiles(
        fileio: app.fileio,
        limits: .default,
        sandboxDirectory: "Resources/Views"
    ))

    // Add OpenAPI Middleware
    let dataProvider = MockDataProvider(mockContent: "openapi: 3.1.0")
    app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))

    // Add /docs route (simulating user configuration)
    app.get("docs") { req -> EventLoopFuture<View> in
        let context = ["specURL": "/openapi.yml"]
        return req.view.render("redoc", context)
    }

    // Simulate a request to the /docs route
    try app.test(.GET, "docs", afterResponse: { res in
        XCTAssertEqual(res.status, .ok, "Expected 200 OK response.")
        XCTAssertTrue(res.body.string.contains("<redoc"), "Response should include Redoc component.")
        XCTAssertTrue(res.body.string.contains("spec-url=\"/openapi.yml\""), "Response should include correct spec-url.")
        XCTAssertTrue(res.body.string.contains("openapi: 3.1.0"), "Response should indicate OpenAPI version 3.1.0.")
    })
}
