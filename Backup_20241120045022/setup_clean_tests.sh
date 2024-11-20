#!/bin/bash

echo "Starting repository cleanup and setup for OpenAPIServe tests..."

# Step 1: Backup existing files
BACKUP_DIR="Backup_$(date +%Y%m%d%H%M%S)"
mkdir -p $BACKUP_DIR

echo "Backing up existing files..."
mv Tests/OpenAPIServeTests/* $BACKUP_DIR/ 2>/dev/null
mv *.sh *.py $BACKUP_DIR/ 2>/dev/null
mv Resources/OpenAPI/openapi.yml Resources/Views/redoc.leaf $BACKUP_DIR/ 2>/dev/null

# Step 2: Clean existing test structure
echo "Cleaning existing test files and scripts..."
rm -rf Tests/OpenAPIServeTests/*
rm -f *.sh *.py

# Step 3: Create new testing structure
echo "Setting up new testing structure..."
mkdir -p Tests/OpenAPIServeTests

cat <<EOF > Tests/OpenAPIServeTests/testFileNotFound.swift
import XCTest
@testable import OpenAPIServe

final class TestFileNotFound: XCTestCase {
    func testOpenAPIMiddlewareFileNotFound() throws {
        let app = try Application.testable()
        defer { app.shutdown() }
        let response = try app.test(.GET, "/openapi.yml")
        XCTAssertEqual(response.status, .notFound)
    }
}
EOF

cat <<EOF > Tests/OpenAPIServeTests/testServeSpecFile.swift
import XCTest
@testable import OpenAPIServe

final class TestServeSpecFile: XCTestCase {
    func testOpenAPIMiddlewareServesSpecFile() throws {
        let app = try Application.testable()
        defer { app.shutdown() }
        let response = try app.test(.GET, "/openapi.yml")
        XCTAssertEqual(response.status, .ok)
        XCTAssertEqual(response.headers.contentType, .init(type: "application", subType: "x-yaml"))
        XCTAssertTrue(response.body.string.contains("openapi: 3.1.0"))
    }
}
EOF

cat <<EOF > Tests/OpenAPIServeTests/testRedocHandler.swift
import XCTest
@testable import OpenAPIServe

final class TestRedocHandler: XCTestCase {
    func testRedocHandlerRendersLeafTemplate() throws {
        let app = try Application.testable()
        defer { app.shutdown() }
        let response = try app.test(.GET, "/docs")
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains("<redoc spec-url='/openapi.yml'>"))
    }
}
EOF

# Step 4: Rebuild and reindex
echo "Updating Package.swift..."
cat <<EOF > Package.swift
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
EOF

echo "Cleaning and rebuilding the project..."
swift package clean
swift build

echo "Repository setup complete. Run tests individually to ensure each passes."

