
# **OpenAPIServe**

OpenAPIServe is a reusable Swift library for serving OpenAPI specifications and interactive API documentation in Vapor projects. This library enforces a standardized location for your OpenAPI spec file and provides middleware to serve it dynamically.

---

## **Features**

- Serves OpenAPI specification files (`openapi.yml` or `openapi.json`) at customizable routes.
- Enforces a standard location for the OpenAPI specification in your Vapor project.
- Lightweight middleware integration for Vapor applications.

---

## **Installation**

### **Add OpenAPIServe to Your Project**

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

## **Usage**

### **Step 1: Place the OpenAPI Specification**

Ensure your OpenAPI specification file (`openapi.yml`) is located in the following path **relative to the Vapor project root**:

```
Resources/OpenAPI/openapi.yml
```

> **Example Placeholder Content**:
```yaml
openapi: 3.1.0
info:
  title: Example API
  version: 1.0.0
paths: {}
```

If the file is missing, the middleware will throw a runtime error with instructions to create it.

---

### **Step 2: Add Middleware**

Import and use the `OpenAPIMiddleware` in your Vapor project:

```swift
import Vapor
import OpenAPIMiddleware

public func configure(_ app: Application) throws {
    app.middleware.use(OpenAPIMiddleware(filePath: "../Resources/OpenAPI/openapi.yml"))
}
```

---

## **Testing**

Run your Vapor app and test the following endpoints:

### **1. OpenAPI Specification**
Access the OpenAPI spec at:
```
http://localhost:8080/openapi.yml
```

Example with `curl`:
```bash
curl http://localhost:8080/openapi.yml
```

If the file is properly configured, it will return the content of `openapi.yml`. If not, an error will indicate the missing file.

---

## **Development Roadmap**

- [x] Middleware for serving OpenAPI specs.
- [x] Runtime validation for `openapi.yml` location.
- [ ] Integration with ReDoc for interactive documentation.
- [ ] Unit tests for middleware and handlers.
- [ ] Support for Swagger UI as an alternative to ReDoc.

---

## **Contribution**

Contributions are welcome! Please submit a pull request or open an issue to get involved.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Author**

Developed and maintained by [Contexter](https://github.com/Contexter).

---


