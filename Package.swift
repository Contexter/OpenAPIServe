// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "OpenAPIServe",
    platforms: [
        .macOS(.v12)
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),
        .package(url: "https://github.com/vapor/leaf.git", from: "4.0.0")
    ],
    targets: [
        .target(
            name: "OpenAPIServe",
            dependencies: [.product(name: "Vapor", package: "vapor"),
                           .product(name: "Leaf", package: "leaf")],
            resources: [
                .copy("Resources/OpenAPI/openapi.yml"),
                .copy("Resources/Views/redoc.leaf")
            ]
        ),
        .testTarget(
            name: "OpenAPIServeTests",
            dependencies: ["OpenAPIServe"],
            resources: []
        )
    ]
)
