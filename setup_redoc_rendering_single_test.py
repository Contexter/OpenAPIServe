import os
import shutil
import subprocess

# Paths and file locations
TESTS_DIR = "Tests/OpenAPIServeTests"
UTILITIES_DIR = os.path.join(TESTS_DIR, "Utilities")
MOCK_PROVIDER_FILE = os.path.join(UTILITIES_DIR, "MockDataProvider.swift")
TEST_FILE = os.path.join(TESTS_DIR, "test_redoc_rendering_single.swift")
RESOURCES_DIR = "Resources/Views"
LEAF_FILE = os.path.join(RESOURCES_DIR, "redoc.leaf")
MOCK_CONTENT = "openapi: 3.1.0"

# Shared MockDataProvider content
MOCK_PROVIDER_CONTENT = """
import OpenAPIServe

// MockDataProvider conforming to DataProvider protocol
public struct MockDataProvider: DataProvider {
    public let mockContent: String
    public init(mockContent: String) {
        self.mockContent = mockContent
    }
    public func getData() -> String {
        return mockContent
    }
}
"""

# Single test content
TEST_CONTENT = f"""
import XCTVapor
import OpenAPIServe
import Utilities

func testRedocRenderingForOpenAPI31() throws {{
    let app = Application(.testing)
    defer {{ app.shutdown() }}

    // Configure Leaf to use Resources/Views
    app.views.use(.leaf)
    app.leaf.sources = .singleSource(NioLeafFiles(
        fileio: app.fileio,
        limits: .default,
        sandboxDirectory: "{RESOURCES_DIR}"
    ))

    // Add OpenAPI Middleware
    let dataProvider = MockDataProvider(mockContent: "{MOCK_CONTENT}")
    app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))

    // Add /docs route (simulating user configuration)
    app.get("docs") {{ req -> EventLoopFuture<View> in
        let context = ["specURL": "/openapi.yml"]
        return req.view.render("redoc", context)
    }}

    // Simulate a request to the /docs route
    try app.test(.GET, "docs", afterResponse: {{ res in
        XCTAssertEqual(res.status, .ok, "Expected 200 OK response.")
        XCTAssertTrue(res.body.string.contains("<redoc"), "Response should include Redoc component.")
        XCTAssertTrue(res.body.string.contains("spec-url=\\"/openapi.yml\\""), "Response should include correct spec-url.")
        XCTAssertTrue(res.body.string.contains("openapi: 3.1.0"), "Response should indicate OpenAPI version 3.1.0.")
    }})
}}
"""

def create_mock_provider():
    """Create the MockDataProvider.swift file."""
    print(f"Creating MockDataProvider file at: {MOCK_PROVIDER_FILE}")
    os.makedirs(UTILITIES_DIR, exist_ok=True)
    with open(MOCK_PROVIDER_FILE, "w") as file:
        file.write(MOCK_PROVIDER_CONTENT)
    print(f"MockDataProvider file created: {MOCK_PROVIDER_FILE}")

def create_test_file():
    """Create the single test file."""
    print(f"Creating single test file at: {TEST_FILE}")
    os.makedirs(TESTS_DIR, exist_ok=True)
    with open(TEST_FILE, "w") as file:
        file.write(TEST_CONTENT)
    print(f"Test file created: {TEST_FILE}")

def check_and_setup_leaf_file():
    """Ensure the redoc.leaf file is present in the Resources/Views directory."""
    print(f"Ensuring Leaf file exists at: {LEAF_FILE}")
    os.makedirs(RESOURCES_DIR, exist_ok=True)
    if not os.path.exists(LEAF_FILE):
        with open(LEAF_FILE, "w") as file:
            file.write("<redoc spec-url=\"{{specURL}}\"></redoc>")
        print(f"Leaf file created: {LEAF_FILE}")
    else:
        print(f"Leaf file already exists: {LEAF_FILE}")

def clean_build():
    """Clean the build directory."""
    print("Cleaning build directory...")
    if os.path.exists(".build"):
        shutil.rmtree(".build")
        print("Build directory cleaned.")

def build_and_test():
    """Run the Swift build and test commands."""
    print("Building and running single test...")
    try:
        subprocess.run(["swift", "build"], check=True)
        subprocess.run(["swift", "test", "--filter", "testRedocRenderingForOpenAPI31"], check=True)
        print("Build and test completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during build or test: {e}")

def main():
    print("Setting up a single Redoc Rendering Test for OpenAPI 3.1...")
    create_mock_provider()
    create_test_file()
    check_and_setup_leaf_file()
    clean_build()
    build_and_test()

if __name__ == "__main__":
    main()
