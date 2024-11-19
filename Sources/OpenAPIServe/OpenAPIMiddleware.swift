import Vapor

public struct OpenAPIMiddleware: Middleware {
    private let filePath: String

    public init(filePath: String = "../Resources/OpenAPI/openapi.yml") {
        self.filePath = filePath

        // Perform runtime check for the OpenAPI file's existence
        let fullPath = DirectoryConfiguration.detect().resourcesDirectory + filePath
        guard FileManager.default.fileExists(atPath: fullPath) else {
            fatalError("""
            ERROR: The OpenAPI specification file `openapi.yml` is missing.
            Please create the file at: \(fullPath)
            Example placeholder content:
            ---
            openapi: 3.1.0
            info:
              title: Example API
              version: 1.0.0
            paths: {{}}
            ---
            """)
        }
    }

    public func respond(to request: Request, chainingTo next: Responder) async throws -> Response {
        guard request.url.path == "/openapi.yml" else {
            return try await next.respond(to: request)
        }

        let fullPath = request.application.directory.workingDirectory + filePath
        guard FileManager.default.fileExists(atPath: fullPath) else {
            throw Abort(.notFound, reason: "OpenAPI spec not found at \(filePath)")
        }

        return request.fileio.streamFile(at: fullPath)
    }
}
