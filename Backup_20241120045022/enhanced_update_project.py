import os

def write_to_file(file_path, content):
    """Write content to a file only if it differs from the current content."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            current_content = file.read()
        if current_content == content:
            print(f"No changes needed for {file_path}.")
            return
    with open(file_path, "w") as file:
        file.write(content)
    print(f"Updated {file_path} successfully.")

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
                return request.eventLoop.makeSucceededFuture(
                    request.fileio.streamFile(at: file)
                )
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
    write_to_file(middleware_path, middleware_content)

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
    write_to_file(handler_path, handler_content)

def main():
    """Apply fixes and ensure changes are applied successfully."""
    print("Starting the update process...")
    try:
        update_openapi_middleware()
        update_redoc_handler()
        print("All updates applied successfully. You can now build and test the project.")
    except Exception as e:
        print(f"An error occurred during the update process: {e}")

if __name__ == "__main__":
    main()

