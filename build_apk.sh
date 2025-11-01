#!/bin/bash
# Build script for PyBar Android APK

echo "========================================"
echo "PyBar Android APK Build Script"
echo "========================================"
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "⚠ Buildozer not found. Installing..."
    pip install buildozer
    if [ $? -ne 0 ]; then
        echo "✗ Failed to install buildozer"
        exit 1
    fi
fi

echo "✓ Buildozer found"
echo ""

# Check for required system dependencies
echo "Checking system dependencies..."
MISSING_DEPS=()

for cmd in git zip unzip java; do
    if ! command -v $cmd &> /dev/null; then
        MISSING_DEPS+=($cmd)
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "⚠ Missing dependencies: ${MISSING_DEPS[*]}"
    echo "Please install them before building."
    exit 1
fi

echo "✓ All required dependencies found"
echo ""

# Clean previous builds
if [ -d ".buildozer" ]; then
    echo "Cleaning previous build artifacts..."
    rm -rf .buildozer/android/platform/build-*
    echo "✓ Cleaned"
    echo ""
fi

# Build APK
echo "========================================"
echo "Starting APK build..."
echo "========================================"
echo ""
echo "This may take 30-60 minutes on first build"
echo "(downloads Android SDK, NDK, and dependencies)"
echo ""

buildozer android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Build successful!"
    echo "========================================"
    echo ""
    echo "APK location: bin/pybar-1.0-arm64-v8a-debug.apk"
    echo ""
    echo "To install on device:"
    echo "  adb install bin/pybar-1.0-arm64-v8a-debug.apk"
    echo ""
else
    echo ""
    echo "========================================"
    echo "✗ Build failed"
    echo "========================================"
    echo ""
    echo "Check the logs above for errors."
    echo "Common issues:"
    echo "  - Missing system dependencies"
    echo "  - SDK/NDK download failures"
    echo "  - Insufficient disk space"
    echo ""
    exit 1
fi
