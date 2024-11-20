import os

def update_openapi_middleware():
    """Fix the OpenAPIMiddleware.swift file."""
    middleware_path = "Sources/OpenAPIServe/OpenAPIMiddleware.swift"
    middleware_content = '''import Vapor

public struct OpenAPIMiddleware: Middleware {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func respond(to request: Request, chainingTo next: Responder) -> EventLoopFuture<Response> {
        if request.url.path == "/openapi.yml" {
            let file = request.application.directory.resourcesDirectory + filePath
            print("Looking for file at:", file)
            print("File exists:", FileManager.default.fileExists(atPath: file))
            if FileManager.default.fileExists(atPath: file) {
                return request.fileio.streamFile(at: file)
            } else {
                return request.eventLoop.makeSucceededFuture(
                    Response(status: .notFound, body: Response.Body(string: "File not found"))
                )
            }
        } else {
            return next.respond(to: request)
        }
    }
}
'''
    with open(middleware_path, "w") as file:
        file.write(middleware_content)
    print(f"Updated {middleware_path}.")

def update_redoc_handler():
    """Fix the RedocHandler.swift file."""
    handler_path = "Sources/OpenAPIServe/RedocHandler.swift"
    handler_content = '''import Vapor

public struct RedocHandler {
    public static func registerRoutes(
        on app: Application,
        docsPath: String = "/docs",
        specPath: String = "/openapi.yml"
    ) {
        app.get(PathComponent(stringLiteral: docsPath)) { req -> EventLoopFuture<View> in
            let leafPath = app.directory.resourcesDirectory + "Views/redoc.leaf"
            print("Looking for Leaf template at:", leafPath)
            print("Template exists:", FileManager.default.fileExists(atPath: leafPath))
            guard FileManager.default.fileExists(atPath: leafPath) else {
                return req.eventLoop.future(error: Abort(.notFound, reason: "Template not found"))
            }
            return req.view.render("redoc", ["specUrl": specPath])
        }
    }
}
'''
    with open(handler_path, "w") as file:
        file.write(handler_content)
    print(f"Updated {handler_path}.")

def main():
    """Apply fixes to OpenAPIServe files."""
    update_openapi_middleware()
    update_redoc_handler()
    print("Fixes applied. Run `swift build` and `swift test` to verify.")

if __name__ == "__main__":
    main()

