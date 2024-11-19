import Vapor

public struct RedocHandler {
    public static func registerRoutes(
        on app: Application,
        docsPath: String = "/docs",
        specPath: String = "/openapi.yml"
    ) {
        app.get(docsPath) { req -> View in
            return req.view.render("redoc", ["specUrl": specPath])
        }
    }
}
