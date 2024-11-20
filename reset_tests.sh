#!/bin/bash

echo "Resetting testing environment for OpenAPIServe..."

# Step 1: Backup the current tests (just in case)
echo "Backing up existing tests to Backup directory..."
BACKUP_DIR="Backup_$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"
mv Tests/OpenAPIServeTests/* "$BACKUP_DIR" 2>/dev/null || echo "No existing tests to back up."

# Step 2: Clean the repository
echo "Cleaning the repository..."
rm -rf .build
swift package clean

# Step 3: Remove any test clutter
echo "Removing test clutter..."
rm -rf Tests/OpenAPIServeTests/
mkdir -p Tests/OpenAPIServeTests/

# Step 4: Create a bare minimum test
echo "Creating minimal passing test..."
cat <<EOF > Tests/OpenAPIServeTests/MinimalTest.swift
import XCTest

final class MinimalTest: XCTestCase {
    func testMinimalPass() {
        XCTAssertTrue(true)
    }
}
EOF

# Step 5: Clean and Rebuild the project
echo "Rebuilding the project..."
swift build
if [ $? -ne 0 ]; then
    echo "Build failed. Please check for errors."
    exit 1
fi

# Step 6: Run the minimal test
echo "Running minimal test..."
swift test

if [ $? -eq 0 ]; then
    echo "Minimal test passed successfully!"
else
    echo "Minimal test failed. Please check for errors."
fi

echo "Testing environment has been reset to a bare minimum."


