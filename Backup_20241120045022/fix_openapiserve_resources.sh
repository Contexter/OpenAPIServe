#!/bin/bash

# Script Name: fix_openapiserve_resources.sh
# Description: Fix resource handling issues, update package settings, and ensure files are in correct locations.
# Usage: bash fix_openapiserve_resources.sh

set -e

# Paths
PACKAGE_SWIFT="Package.swift"
RESOURCE_DIR="Sources/OpenAPIServe/Resources"
VIEW_DIR="$RESOURCE_DIR/Views"
OPENAPI_DIR="$RESOURCE_DIR/OpenAPI"
REDOC_FILE="$VIEW_DIR/redoc.leaf"
OPENAPI_FILE="$OPENAPI_DIR/openapi.yml"

# Create necessary directories
echo "Creating necessary resource directories..."
mkdir -p "$VIEW_DIR"
mkdir -p "$OPENAPI_DIR"

# Create or overwrite the redoc.leaf file
echo "Ensuring $REDOC_FILE exists..."
cat > "$REDOC_FILE" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
</head>
<body>
    <redoc spec-url="{{ specUrl }}"></redoc>
</body>
</html>
EOF

# Create or overwrite the openapi.yml file
echo "Ensuring $OPENAPI_FILE exists..."
cat > "$OPENAPI_FILE" <<EOF
openapi: 3.1.0
info:
  title: Test API
  version: 1.0.0
paths: {}
EOF

# Update Package.swift to include resources explicitly
echo "Updating $PACKAGE_SWIFT to declare resources explicitly..."
if ! grep -q "resources:" "$PACKAGE_SWIFT"; then
    sed -i.bak '/name: "OpenAPIServe", dependencies: \[/a\
                resources: [\
                    .copy("Resources/Views/redoc.leaf"),\
                    .copy("Resources/OpenAPI/openapi.yml")\
                ],
    ' "$PACKAGE_SWIFT"
    echo "Resources added to $PACKAGE_SWIFT."
else
    echo "Resources already declared in $PACKAGE_SWIFT."
fi

# Remove backup file created by sed
rm -f "$PACKAGE_SWIFT.bak"

# Clean build directory
echo "Cleaning build directory..."
swift package clean

# Build the project
echo "Building the project..."
swift build

# Run tests
echo "Running tests..."
swift test

echo "Fix complete. Build and tests executed successfully!"

