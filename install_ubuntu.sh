#!/bin/bash
# Ubuntu installation script for L2F package
# This script ensures all required dependencies are installed

set -e

echo "🐧 Ubuntu L2F Installation Script"
echo "=================================="

# Check if running on Ubuntu/Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ This script is designed for Ubuntu/Linux systems"
    exit 1
fi

echo "📦 Installing system dependencies..."

# Update package list
sudo apt-get update

# Install essential build tools
sudo apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    libc6-dev \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config

echo "✅ System dependencies installed"

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel pybind11

echo "🔨 Building L2F package..."
pip install . -v

echo "✅ L2F package installed successfully!"
echo ""
echo "🧪 Testing installation..."
python3 -c "import l2f; import l2f.gym; print('✅ L2F package works correctly!')"

echo ""
echo "🎉 Installation complete!"
echo "You can now use: import l2f; import l2f.gym"
