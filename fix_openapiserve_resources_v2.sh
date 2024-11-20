#!/bin/bash

echo "Starting resource fix process for OpenAPIServe..."

# Set resource directories
RESOURCE_DIR="Sources/OpenAPIServe/Resources"
VIEWS_DIR="$RESOURCE_DIR/Views"
OPENAPI_DIR="$RESOURCE_DIR/OpenAPI"

# Create necessary directories if they don't exist
echo "Creating necessary resource directories..."
mkdir -p "$VIEWS_DIR"
mkdir -p "$OPENAPI_DIR"

# Ensure redoc.leaf exists
REDOC_FILE="$VIEWS_DIR/redoc.leaf"
if [ ! -f "$REDOC_FILE" ]; then
    echo "Creating $REDOC_FILE..."
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
else
    echo "$REDOC_FILE already exists."
fi

# Ensure openapi.yml exists
OPENAPI_FILE="$OPENAPI_DIR/openapi.yml"
if [ ! -f "$OPENAPI_FILE" ]; then
    echo "Creating $OPENAPI_FILE..."
    cat > "$OPENAPI_FILE" <<EOF
openapi: 3.1.0
info:
  title: Test API
  version: 1.0.0
paths: {}
EOF
else
    echo "$OPENAPI_FILE already exists."
fi

# Update Package.swift to include resources
echo "Updating Package.swift to declare resources explicitly..."
if ! grep -q ".copy(\"Resources/Views/redoc.leaf\")" Package.swift; then
    sed -i '' '/dependencies: \[/a\
           resources: [
               .copy("Resources/Views/redoc.leaf"),
               .copy("Resources/OpenAPI/openapi.yml")
           ],
    ' Package.swift
    echo "Resources declaration added to Package.swift."
else
    echo "Resources already declared in Package.swift."
fi

# Clean and rebuild the project
echo "Cleaning build directory..."
swift package clean

echo "Building the project..."
swift build

echo "Running tests..."
swift test

echo "Resource fix process complete."

