import Vapor

public struct OpenAPIServe {
    public static func configure(
        _ app: Application,
        openapiPath: String = "Resources/OpenAPI/openapi.yml",
        docsPath: String = "/docs"
    ) throws {
        // Register OpenAPI Middleware
        app.middleware.use(OpenAPIMiddleware(filePath: openapiPath))
        
        // Register ReDoc Route
        RedocHandler.registerRoutes(on: app, docsPath: docsPath, specPath: "/openapi.yml")
    }
}
