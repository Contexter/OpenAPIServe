import os
import json

# Paths to key directories
BASE_DIR = os.getcwd()
PACKAGE_FILE = os.path.join(BASE_DIR, "Package.swift")
TESTS_DIR = os.path.join(BASE_DIR, "Tests/OpenAPIServeTests")
UTILITIES_DIR = os.path.join(TESTS_DIR, "Utilities")
RESOURCES_DIR = os.path.join(BASE_DIR, "Resources")
VIEWS_DIR = os.path.join(RESOURCES_DIR, "Views")


def index_repository():
    """Index the repository and return paths for Utilities and Resources."""
    paths = {
        "utilities": UTILITIES_DIR if os.path.exists(UTILITIES_DIR) else None,
        "views": VIEWS_DIR if os.path.exists(VIEWS_DIR) else None,
        "resources": RESOURCES_DIR if os.path.exists(RESOURCES_DIR) else None,
    }
    return paths


def validate_package(paths):
    """Validate and update the Package.swift based on the repository structure."""
    if not os.path.exists(PACKAGE_FILE):
        print(f"Error: {PACKAGE_FILE} not found!")
        return

    # Load the Package.swift file
    with open(PACKAGE_FILE, "r") as f:
        package_content = f.readlines()

    # Updated Package.swift
    updated_content = []
    for line in package_content:
        if "Utilities" in line and paths["utilities"] is None:
            print("Skipping Utilities, as the folder does not exist.")
            continue
        if "Resources/Views" in line and paths["views"] is None:
            print("Skipping Resources/Views, as the folder does not exist.")
            continue
        updated_content.append(line)

    # Write back to Package.swift
    with open(PACKAGE_FILE, "w") as f:
        f.writelines(updated_content)
    print("Package.swift updated based on the repository structure.")


def configure_package(paths):
    """Update the Package.swift file with proper paths."""
    print("Configuring Package.swift...")

    utilities_include = (
        f"""
        .target(
            name: "Utilities",
            dependencies: [],
            path: "{paths['utilities']}",
            sources: ["."]
        ),
        """
        if paths["utilities"]
        else ""
    )

    views_resource = (
        f"""
            .process("{os.path.relpath(paths['views'], BASE_DIR)}")
        """
        if paths["views"]
        else ""
    )

    # Rewrite Package.swift with valid configurations
    package_content = f"""
// swift-tools-version:5.6
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
        .package(url: "https://github.com/vapor/leaf.git", from: "4.0.0")
    ],
    targets: [
        .target(
            name: "OpenAPIServe",
            dependencies: [
                .product(name: "Vapor", package: "vapor"),
                .product(name: "Leaf", package: "leaf")
            ],
            resources: [.process("Resources")]
        ),
        .testTarget(
            name: "OpenAPIServeTests",
            dependencies: [
                "OpenAPIServe",
                .product(name: "XCTVapor", package: "vapor"),
                "Utilities"
            ],
            path: "{TESTS_DIR}",
            exclude: ["Utilities"],
            resources: [
                {views_resource}
            ]
        ),
        {utilities_include}
    ]
)
    """

    # Write updated Package.swift
    with open(PACKAGE_FILE, "w") as f:
        f.write(package_content)
    print("Package.swift configured successfully!")


def main():
    """Main entry point for the script."""
    print("Indexing repository...")
    paths = index_repository()
    print(json.dumps(paths, indent=4))

    print("\nValidating Package.swift...")
    validate_package(paths)

    print("\nConfiguring Package.swift...")
    configure_package(paths)

    print("\nDone! Run `swift build` and `swift test` to verify.")


if __name__ == "__main__":
    main()

