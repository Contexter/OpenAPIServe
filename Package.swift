// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "OpenAPIServe",
    platforms: [
        .macOS(.v12)
    ],
    products: [
        .library(
            name: "OpenAPIServe",
            targets: ["OpenAPIServe"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),
        .package(url: "https://github.com/vapor/leaf.git", from: "4.0.0"),
    ],
    targets: [
        .target(
            name: "OpenAPIServe",
            dependencies: [
                .product(name: "Vapor", package: "vapor"),
                .product(name: "Leaf", package: "leaf"),
            ],
            resources: [
                .copy("Resources/Views/redoc.leaf"),
                .copy("Resources/OpenAPI/openapi.yml")
            ]
        ),
        .testTarget(
            name: "OpenAPIServeTests",
            dependencies: [
                .target(name: "OpenAPIServe"),
                .product(name: "XCTVapor", package: "vapor"),
            ]
        )
    ]
)
