#!/usr/bin/env python3
"""
Debug build script for l2f package.
This script helps diagnose build issues in different environments.
"""

import sys
import os
import subprocess
import platform

def check_environment():
    """Check the build environment and print useful information."""
    print("=== Environment Information ===")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    
    # Check for common environment variables
    env_vars = ['CI', 'COLAB_GPU', 'GITHUB_ACTIONS', 'TRAVIS', 'CIRCLECI']
    print("\n=== Environment Variables ===")
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"{var}: {value}")
    
    # Check compiler availability
    print("\n=== Compiler Information ===")
    try:
        result = subprocess.run(['gcc', '--version'], capture_output=True, text=True)
        print(f"GCC: {result.stdout.split()[0] if result.returncode == 0 else 'Not available'}")
    except FileNotFoundError:
        print("GCC: Not found")
    
    try:
        result = subprocess.run(['clang', '--version'], capture_output=True, text=True)
        print(f"Clang: {result.stdout.split()[0] if result.returncode == 0 else 'Not available'}")
    except FileNotFoundError:
        print("Clang: Not found")
    
    # Check Python packages
    print("\n=== Python Packages ===")
    try:
        import setuptools
        print(f"setuptools: {setuptools.__version__}")
    except ImportError:
        print("setuptools: Not installed")
    
    try:
        import pybind11
        print(f"pybind11: {pybind11.__version__}")
    except ImportError:
        print("pybind11: Not installed")

def test_compiler_flags():
    """Test if compiler flags work in the current environment."""
    print("\n=== Testing Compiler Flags ===")
    
    test_code = """
#include <iostream>
int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""
    
    # Test basic compilation
    with open('test_compile.cpp', 'w') as f:
        f.write(test_code)
    
    try:
        result = subprocess.run(['g++', '-std=c++17', 'test_compile.cpp', '-o', 'test_compile'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Basic C++17 compilation works")
            os.remove('test_compile')
        else:
            print("✗ Basic C++17 compilation failed")
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"✗ Compiler test failed: {e}")
    finally:
        if os.path.exists('test_compile.cpp'):
            os.remove('test_compile.cpp')
        if os.path.exists('test_compile'):
            os.remove('test_compile')

def main():
    """Main function to run all checks."""
    print("L2F Build Environment Debugger")
    print("=" * 40)
    
    check_environment()
    test_compiler_flags()
    
    print("\n=== Recommendations ===")
    if os.environ.get('CI') or os.environ.get('COLAB_GPU'):
        print("- Running in CI/Colab environment - using conservative compiler flags")
    else:
        print("- Running in development environment - can use aggressive optimizations")
    
    print("\nIf build still fails, try:")
    print("1. pip install --upgrade setuptools pybind11")
    print("2. pip install --no-cache-dir .")
    print("3. Check that external/rl-tools/include exists")

if __name__ == "__main__":
    main()
