
# OpenAPIServe

OpenAPIServe is a reusable Swift library for serving OpenAPI specifications and interactive API documentation in Vapor projects. This library enforces a standardized location for your OpenAPI spec file and provides middleware to serve it dynamically.

---

## Features

- Serves OpenAPI specification files (`openapi.yml` or `openapi.json`) at customizable routes.
- Provides middleware integration for Vapor applications.
- Supports ReDoc for interactive API documentation.

---

## Installation

### Add OpenAPIServe to Your Project

Add the package to your `Package.swift` dependencies:

```swift
dependencies: [
    .package(url: "https://github.com/your-username/OpenAPIServe.git", from: "1.0.0")
]
```

Include `OpenAPIServe` in your target dependencies:

```swift
.target(
    name: "App",
    dependencies: [
        .product(name: "OpenAPIServe", package: "OpenAPIServe")
    ]
)
```

---

## Usage

### Step 1: Place the OpenAPI Specification

Ensure your OpenAPI specification file (`openapi.yml`) is located in the following path **relative to the Vapor project root**:

```
Sources/Resources/openapi.yml
```

---

### Step 2: Integrate OpenAPIServe Middleware

In your `configure.swift`, register the `OpenAPIMiddleware` with a file path to your spec file:

```swift
import OpenAPIServe

public func configure(_ app: Application) throws {
    // Middleware configuration
    let openapiFilePath = app.directory.resourcesDirectory + "openapi.yml"
    app.middleware.use(OpenAPIMiddleware(filePath: openapiFilePath))
}
```

---

### Step 3: Add a ReDoc Route

Register a route in your `routes.swift` to serve the ReDoc API documentation:

```swift
app.get("docs") { req -> EventLoopFuture<View> in
    let context = ["specURL": "/openapi.yml"]
    return req.view.render("redoc", context)
}
```

Ensure the ReDoc HTML template (`redoc.leaf`) is placed under the `Resources/Views` directory.

---

### Step 4: Build and Run

Compile your Vapor project:

```bash
swift build
swift run
```

Visit the following URLs:

- **OpenAPI Spec:** `http://localhost:8080/openapi.yml`
- **API Docs:** `http://localhost:8080/docs`

---

## Contributing

Contributions are welcome! Please fork the repository, make changes, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
