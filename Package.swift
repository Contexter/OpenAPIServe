// swift-tools-version:5.5
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
        .package(url: "https://github.com/apple/swift-algorithms.git", from: "1.0.0")
    ],
    targets: [
        // Main OpenAPIServe target
        .target(
            name: "OpenAPIServe",
            dependencies: [
                .product(name: "Vapor", package: "vapor"),
                .product(name: "Leaf", package: "leaf"),
                .product(name: "Algorithms", package: "swift-algorithms")
            ],
            path: "Sources/OpenAPIServe",
            resources: [
                .process("Resources")
            ]
        ),
        
        // Utilities for testing
        .target(
            name: "Utilities",
            dependencies: [
                .product(name: "Vapor", package: "vapor"),
                "OpenAPIServe"
            ],
            path: "Tests/OpenAPIServeTests/Utilities"
        ),

        // Test target
        .testTarget(
            name: "OpenAPIServeTests",
            dependencies: ["OpenAPIServe", "Utilities"],
            path: "Tests/OpenAPIServeTests",
            exclude: ["Utilities"],
            resources: [
                .process("Resources/Views")
            ]
        )
    ]
)
