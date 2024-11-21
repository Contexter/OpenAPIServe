import os
import subprocess

# Define the test directory and file path
TESTS_DIR = "Tests/OpenAPIServeTests"
TEST_FILE = os.path.join(TESTS_DIR, "test_redoc_rendering.swift")

# Content for the Redoc rendering test
TEST_CONTENT = """\
import XCTVapor
import OpenAPIServe

final class RedocRenderingTests: XCTestCase {
    func testRedocRendering() throws {
        let app = Application(.testing)
        defer { app.shutdown() }

        // Add OpenAPI Middleware
        let dataProvider = MockDataProvider(mockContent: "openapi: 3.0.0")
        app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))

        // Add /docs route (simulating user configuration)
        app.get("docs") { req -> EventLoopFuture<View> in
            let context = ["specURL": "/openapi.yml"]
            return req.view.render("redoc", context)
        }

        // Simulate a request to the /docs route
        try app.test(.GET, "docs", afterResponse: { res in
            XCTAssertEqual(res.status, .ok)
            XCTAssertTrue(res.body.string.contains("<redoc"))
            XCTAssertTrue(res.body.string.contains("spec-url=\\"/openapi.yml\\""))
        })
    }
}
"""

# Function to create the test file
def create_test_file():
    os.makedirs(TESTS_DIR, exist_ok=True)
    with open(TEST_FILE, "w") as f:
        f.write(TEST_CONTENT)
    print(f"Test file created: {TEST_FILE}")

# Function to build and run the tests
def build_and_test():
    print("Building the project...")
    subprocess.run(["swift", "build"], check=True)
    print("Build succeeded.")
    
    print("Running tests...")
    subprocess.run(["swift", "test"], check=True)
    print("Tests passed successfully.")

def main():
    print("Setting up the Redoc rendering test...")
    create_test_file()
    build_and_test()

if __name__ == "__main__":
    main()
