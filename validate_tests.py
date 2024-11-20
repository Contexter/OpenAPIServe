import os

def validate_test_setup():
    """Check test setup and print debugging information."""
    test_path = "Tests/OpenAPIServeTests/OpenAPIServeTests.swift"
    if not os.path.exists(test_path):
        print(f"Error: Test file not found at {test_path}")
        return
    
    with open(test_path, "r") as file:
        content = file.read()
        if "class OpenAPIServeTests" not in content:
            print("Error: Test class 'OpenAPIServeTests' not defined in test file.")
        elif "func test" not in content:
            print("Error: No test methods starting with 'test' found in test file.")
        else:
            print("Test file appears correctly configured.")

def main():
    print("Validating test setup...")
    validate_test_setup()
    print("Validation complete. Run `swift test` to verify test execution.")

if __name__ == "__main__":
    main()

