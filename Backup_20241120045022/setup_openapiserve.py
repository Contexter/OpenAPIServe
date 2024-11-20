import os

def setup_openapi_middleware():
    """
    Sets up the required files for the OpenAPIServe library:
    - Creates Sources/OpenAPIServe/OpenAPIMiddleware.swift.
    - Enforces the norm that the OpenAPI spec resides outside the library in a standard location.
    """

    # Define paths
    sources_dir = "Sources/OpenAPIServe"
    middleware_file = os.path.join(sources_dir, "OpenAPIMiddleware.swift")

    # Ensure the Sources directory exists
    os.makedirs(sources_dir, exist_ok=True)

    # Step 1: Create the OpenAPI middleware
    middleware_content = '''import Vapor

public struct OpenAPIMiddleware: Middleware {
    private let filePath: String

    public init(filePath: String = "../Resources/OpenAPI/openapi.yml") {
        self.filePath = filePath

        // Perform runtime check for the OpenAPI file's existence
        let fullPath = DirectoryConfiguration.detect().resourcesDirectory + filePath
        guard FileManager.default.fileExists(atPath: fullPath) else {
            fatalError("""
            ERROR: The OpenAPI specification file `openapi.yml` is missing.
            Please create the file at: \\(fullPath)
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
            throw Abort(.notFound, reason: "OpenAPI spec not found at \\(filePath)")
        }

        return request.fileio.streamFile(at: fullPath)
    }
}
'''
    if not os.path.exists(middleware_file):
        with open(middleware_file, "w") as file:
            file.write(middleware_content)
        print(f"Created OpenAPI middleware at: {middleware_file}")
    else:
        print(f"Middleware file already exists at: {middleware_file}")

    print("\nSetup complete! Ensure the Vapor project places the `openapi.yml` file in the correct location.")

# Execute the script
if __name__ == "__main__":
    setup_openapi_middleware()

