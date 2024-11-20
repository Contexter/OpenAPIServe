import Vapor

public struct RedocHandler {
    public static func registerRoutes(
        on app: Application,
        docsPath: String = "/docs",
        specPath: String = "/openapi.yml"
    ) {
        app.logger.info("Registering ReDoc route at: \(docsPath)")
        
        app.get("docs") { req -> EventLoopFuture<View> in
            let leafPath = app.directory.resourcesDirectory + "Views/redoc.leaf"
            app.logger.info("Looking for Leaf template at: \(leafPath)")
            
            guard FileManager.default.fileExists(atPath: leafPath) else {
                return req.eventLoop.future(error: Abort(.notFound, reason: "Template not found"))
            }
            return req.view.render("redoc", ["specUrl": specPath])
        }
    }
}
