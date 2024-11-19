// swift-tools-version:5.8

import PackageDescription

let package = Package(
    name: "OpenAPIServe",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .library(name: "OpenAPIServe", targets: ["OpenAPIServe"]),
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor", from: "4.0.0"),
        .package(url: "https://github.com/vapor/leaf", from: "4.0.0")
    ],
    targets: [
        .target(
            name: "OpenAPIServe",
            dependencies: [
                .product(name: "Vapor", package: "vapor"),
                .product(name: "Leaf", package: "leaf")
            ],
            resources: [
                .process("Resources")
            ]
        ),
        .testTarget(
            name: "OpenAPIServeTests",
            dependencies: ["OpenAPIServe"]
        ),
    ]
)
