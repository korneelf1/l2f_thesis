#!/usr/bin/env python3
"""
Installation script specifically for Google Colab and similar environments.
This script handles common issues in restricted environments.
"""

import os
import sys
import subprocess
import shutil

def install_in_colab():
    """Install l2f package in Colab environment."""
    print("Installing l2f in Colab environment...")
    
    # Set environment variables for conservative compilation
    os.environ['COLAB_GPU'] = '1'  # This will trigger conservative compiler flags
    
    # Ensure we have the required packages
    print("Installing build dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'setuptools', 'pybind11'], 
                  check=True)
    
    # Try to install with conservative settings
    print("Installing l2f package...")
    try:
        # First try with no cache to avoid any cached issues
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', '--verbose', '.'], 
                      check=True)
        print("✓ Installation successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Installation failed: {e}")
        
        # Try with even more conservative settings
        print("Trying with minimal optimization...")
        try:
            # Temporarily modify optimization settings
            original_setup = None
            if os.path.exists('setup.py'):
                with open('setup.py', 'r') as f:
                    original_setup = f.read()
                
                # Create a minimal setup
                minimal_setup = original_setup.replace('optimization = True', 'optimization = False')
                with open('setup.py', 'w') as f:
                    f.write(minimal_setup)
                
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', '--verbose', '.'], 
                              check=True)
                print("✓ Installation successful with minimal optimization!")
                return True
        except subprocess.CalledProcessError as e2:
            print(f"✗ Installation still failed: {e2}")
            return False
        finally:
            # Restore original setup
            if original_setup:
                with open('setup.py', 'w') as f:
                    f.write(original_setup)

def main():
    """Main installation function."""
    if install_in_colab():
        print("\n✓ l2f package installed successfully!")
        print("You can now import it with: import l2f")
    else:
        print("\n✗ Installation failed. Please check the error messages above.")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're in the correct directory")
        print("2. Check that external/rl-tools/include exists")
        print("3. Try running: pip install --upgrade setuptools pybind11")
        print("4. Check available disk space")

if __name__ == "__main__":
    main()
