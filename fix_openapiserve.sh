#!/bin/bash

# Script Name: fix_openapiserve.sh
# Description: Fixes resource declaration issues, ensures required files exist, and runs tests for OpenAPIServe.
# Author: Your Name
# Usage: bash fix_openapiserve.sh

set -e

# Paths
PACKAGE_SWIFT="Package.swift"
RESOURCE_DIR="Sources/OpenAPIServe/Resources"
VIEW_DIR="$RESOURCE_DIR/Views"
OPENAPI_DIR="$RESOURCE_DIR/OpenAPI"
REDOC_FILE="$VIEW_DIR/redoc.leaf"
OPENAPI_FILE="$OPENAPI_DIR/openapi.yml"

# Ensure Resources Directories Exist
echo "Ensuring resource directories exist..."
mkdir -p "$VIEW_DIR"
mkdir -p "$OPENAPI_DIR"

# Write redoc.leaf
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

# Write openapi.yml
echo "Ensuring $OPENAPI_FILE exists..."
cat > "$OPENAPI_FILE" <<EOF
openapi: 3.1.0
info:
  title: Test API
  version: 1.0.0
paths: {}
EOF

# Update Package.swift
echo "Updating $PACKAGE_SWIFT to include resources..."
if ! grep -q ".copy(\"Resources\")" "$PACKAGE_SWIFT"; then
    sed -i.bak '/name: "OpenAPIServe", dependencies: \[/a\
                resources: [\
                    .copy("Resources")\
                ],
    ' "$PACKAGE_SWIFT"
    echo "Resources declaration added to $PACKAGE_SWIFT."
else
    echo "Resources already declared in $PACKAGE_SWIFT."
fi

# Clean up backup file from sed
rm -f "$PACKAGE_SWIFT.bak"

# Build the project
echo "Building the project..."
swift build

# Run the tests
echo "Running tests..."
swift test

echo "Fix complete. Tests executed successfully!"

