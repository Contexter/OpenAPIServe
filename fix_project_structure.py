import os
import shutil
import subprocess

# Define the project directories
PROJECT_ROOT = os.path.abspath(".")
SOURCES_DIR = os.path.join(PROJECT_ROOT, "Sources", "OpenAPIServe")
RESOURCES_DIR = os.path.join(SOURCES_DIR, "Resources")
VIEWS_DIR = os.path.join(RESOURCES_DIR, "Views")
TESTS_DIR = os.path.join(PROJECT_ROOT, "Tests", "OpenAPIServeTests")
UTILITIES_DIR = os.path.join(TESTS_DIR, "Utilities")

# Function to create directories if they don't exist
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to move resources to the correct location
def move_resources():
    old_resources = os.path.join(PROJECT_ROOT, "Resources")
    if os.path.exists(old_resources):
        print(f"Moving resources from {old_resources} to {RESOURCES_DIR}")
        shutil.move(old_resources, RESOURCES_DIR)
    else:
        print("No resources found to move.")

# Function to fix Package.swift
def update_package_swift():
    package_swift_path = os.path.join(PROJECT_ROOT, "Package.swift")
    updated_package_content = f"""
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
            resources: [
                .process("Resources")
            ]
        ),
        .target(
            name: "Utilities",
            dependencies: [],
            path: "Tests/OpenAPIServeTests/Utilities",
            exclude: []
        ),
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
"""
    with open(package_swift_path, "w") as f:
        f.write(updated_package_content)
    print("Updated Package.swift")

# Function to ensure utilities are properly set up
def setup_utilities():
    create_dir(UTILITIES_DIR)
    utilities_files = ["MockDataProvider.swift", "TestAppConfigurator.swift", "TestAssertions.swift"]
    for utility in utilities_files:
        source_path = os.path.join(TESTS_DIR, utility)
        dest_path = os.path.join(UTILITIES_DIR, utility)
        if os.path.exists(source_path):
            print(f"Moving {utility} to {UTILITIES_DIR}")
            shutil.move(source_path, dest_path)
        elif os.path.exists(dest_path):
            print(f"{utility} is already in the correct location.")

# Function to clean the build environment
def clean_build():
    print("Cleaning build environment...")
    subprocess.run(["swift", "package", "clean"], check=True)
    subprocess.run(["swift", "package", "reset"], check=True)

# Function to build and test the package
def build_and_test():
    print("Building the package...")
    subprocess.run(["swift", "build"], check=True)
    print("Running tests...")
    subprocess.run(["swift", "test"], check=True)

# Main function to orchestrate the fixes
def main():
    create_dir(RESOURCES_DIR)
    create_dir(VIEWS_DIR)
    move_resources()
    update_package_swift()
    setup_utilities()
    clean_build()
    build_and_test()

if __name__ == "__main__":
    main()

