#!/bin/bash
# Build and publish NWO-AGI to PyPI

set -e

echo "🚀 Building NWO-AGI package for PyPI..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade build twine setuptools wheel

# Build the package
echo "🔨 Building package..."
python -m build

# Check the package
echo "🔍 Checking package..."
twine check dist/*

# Show package info
echo "📊 Package info:"
ls -lh dist/

echo ""
echo "✅ Build complete!"
echo ""
echo "To publish to PyPI:"
echo "  twine upload dist/*"
echo ""
echo "To publish to TestPyPI first:"
echo "  twine upload --repository testpypi dist/*"
echo ""
echo "To install locally:"
echo "  pip install dist/nwo_agi-1.0.0-py3-none-any.whl"
