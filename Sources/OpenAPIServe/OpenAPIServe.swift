import Vapor

/// Configures the OpenAPIServe library within a Vapor application.
public func configure(_ app: Application) throws {
    // Path to the OpenAPI specification file
    let openapiFilePath = "path/to/your/openapi.yml"
    
    // Register OpenAPI Middleware with a FileDataProvider
    app.middleware.use(OpenAPIMiddleware(dataProvider: FileDataProvider(filePath: openapiFilePath)))
    
    // Register ReDoc route
    app.get("docs") { req -> EventLoopFuture<View> in
        let context = ["specURL": "/openapi.yml"]
        return req.view.render("redoc", context)
    }
}
