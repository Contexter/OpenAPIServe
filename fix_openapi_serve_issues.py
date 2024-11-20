import os

def fix_openapi_middleware():
    """
    Fixes the OpenAPIMiddleware implementation to conform to Vapor's Middleware protocol.
    """
    file_path = "Sources/OpenAPIServe/OpenAPIMiddleware.swift"
    middleware_content = '''import Vapor

public struct OpenAPIMiddleware: Middleware {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func respond(to request: Request, chainingTo next: Responder) -> EventLoopFuture<Response> {
        if request.url.path == "/openapi.yml" {
            let file = request.application.directory.resourcesDirectory + filePath
            return request.eventLoop.makeSucceededFuture(request.fileio.streamFile(at: file))
        } else {
            return next.respond(to: request)
        }
    }
}
'''

    with open(file_path, "w") as f:
        f.write(middleware_content)
    print(f"Fixed OpenAPIMiddleware at: {file_path}")


def fix_redoc_handler():
    """
    Fixes the RedocHandler implementation to properly handle routes with PathComponent.
    """
    file_path = "Sources/OpenAPIServe/RedocHandler.swift"
    redoc_content = '''import Vapor

public struct RedocHandler {
    public static func registerRoutes(
        on app: Application,
        docsPath: String = "/docs",
        specPath: String = "/openapi.yml"
    ) {
        app.get([PathComponent(stringLiteral: docsPath)]) { req -> EventLoopFuture<View> in
            req.view.render("redoc", ["specUrl": specPath])
        }
    }
}
'''

    with open(file_path, "w") as f:
        f.write(redoc_content)
    print(f"Fixed RedocHandler at: {file_path}")


def main():
    """
    Executes the fixes for OpenAPIMiddleware and RedocHandler.
    """
    fix_openapi_middleware()
    fix_redoc_handler()
    print("Fixes applied successfully. Rebuild the project using 'swift build'.")

if __name__ == "__main__":
    main()

