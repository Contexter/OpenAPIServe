import os

def setup_redoc():
    """
    Sets up ReDoc integration for the OpenAPIServe library by creating:
    - redoc.leaf template
    - RedocHandler.swift file
    - Updates OpenAPIServe.swift for easy integration
    """

    # Define paths
    resources_dir = "Sources/OpenAPIServe/Resources"
    redoc_template_file = os.path.join(resources_dir, "redoc.leaf")
    redoc_handler_file = "Sources/OpenAPIServe/RedocHandler.swift"
    openapiserve_file = "Sources/OpenAPIServe/OpenAPIServe.swift"

    # Ensure the resources directory exists
    os.makedirs(resources_dir, exist_ok=True)

    # Step 1: Create the redoc.leaf template
    redoc_template_content = '''<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.css">
</head>
<body>
    <redoc spec-url="##specUrl##"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"></script>
</body>
</html>
'''
    with open(redoc_template_file, "w") as file:
        file.write(redoc_template_content)
    print(f"Created ReDoc template at: {redoc_template_file}")

    # Step 2: Create RedocHandler.swift
    redoc_handler_content = '''import Vapor

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
'''
    with open(redoc_handler_file, "w") as file:
        file.write(redoc_handler_content)
    print(f"Created RedocHandler.swift at: {redoc_handler_file}")

    # Step 3: Update OpenAPIServe.swift
    openapiserve_content = '''import Vapor

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
'''
    with open(openapiserve_file, "w") as file:
        file.write(openapiserve_content)
    print(f"Updated OpenAPIServe.swift at: {openapiserve_file}")

    print("\nReDoc integration setup complete!")

# Execute the script
if __name__ == "__main__":
    setup_redoc()

