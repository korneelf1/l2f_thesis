import sys
import os
import time
from setuptools import setup, find_packages, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

debug = False
optimization = True

def get_compile_args():
    """Get compile arguments with fallbacks for different environments."""
    compile_args = []
    
    if optimization:
        if sys.platform == "win32":
            compile_args = ['/O2', '/fp:fast']
        elif sys.platform == "linux":
            # Ubuntu/Linux specific optimizations
            compile_args = ['-O3', '-DNDEBUG']
            # Only add -ffast-math if not in a restricted environment
            if not os.environ.get('CI') and not os.environ.get('COLAB_GPU'):
                compile_args.append('-ffast-math')
            # Add Ubuntu-specific flags for better compatibility
            compile_args.extend(['-fPIC', '-std=c++17'])
        else:
            # macOS and other Unix-like systems
            compile_args = ['-O3']
            # Only add -ffast-math if not in a restricted environment
            if not os.environ.get('CI') and not os.environ.get('COLAB_GPU'):
                compile_args.append('-ffast-math')
            if sys.platform == "darwin":
                compile_args.append('-mmacosx-version-min=10.14')
    
    if debug:
        if sys.platform == "win32":
            compile_args.extend(['/Zi', '/Od', '/D_DEBUG'])
        else:
            compile_args.extend(['-g', '-D_DEBUG'])
    
    return compile_args

def get_link_args():
    """Get link arguments."""
    link_args = []
    if sys.platform == "darwin":
        link_args.append('-mmacosx-version-min=10.14')
    elif sys.platform == "linux":
        # Ubuntu/Linux specific link flags
        link_args.extend(['-fPIC', '-shared'])
    return link_args

class ProgressBuildExt(build_ext):
    """Custom build extension with progress indicators."""
    
    def run(self):
        print("🚀 Starting L2F package build...")
        print("📦 Installing build dependencies...")
        super().run()
        print("✅ Build completed successfully!")
    
    def build_extension(self, ext):
        print(f"🔨 Building extension: {ext.name}")
        print("   This may take a few minutes...")
        start_time = time.time()
        
        try:
            super().build_extension(ext)
            elapsed = time.time() - start_time
            print(f"✅ Extension {ext.name} built in {elapsed:.1f} seconds")
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Extension {ext.name} failed after {elapsed:.1f} seconds")
            print(f"   Error: {str(e)}")
            if sys.platform == "linux":
                print("   💡 Ubuntu troubleshooting tips:")
                print("      - Run: sudo apt-get install build-essential python3-dev")
                print("      - Check: gcc --version")
                print("      - Try: pip install --upgrade setuptools wheel pybind11")
            raise
    
    def build_extensions(self):
        print("🔧 Configuring build environment...")
        print(f"   Platform: {sys.platform}")
        print(f"   Python: {sys.version}")
        print(f"   Compiler flags: {compile_args}")
        
        # Ubuntu-specific build information
        if sys.platform == "linux":
            print("   🐧 Ubuntu/Linux detected - using optimized build settings")
            print("   📋 Make sure you have: build-essential, python3-dev, libc6-dev")
        
        super().build_extensions()

# Get platform-specific arguments
print("🔍 Detecting build environment...")
compile_args = get_compile_args()
link_args = get_link_args()
print(f"   Compiler flags: {compile_args}")
print(f"   Link flags: {link_args}")

# Add Ubuntu-specific include directories
include_dirs = ["external/rl-tools/include"]
if sys.platform == "linux":
    # Add common Ubuntu include paths
    include_dirs.extend([
        "/usr/include",
        "/usr/local/include",
    ])

ext_modules = [
    Pybind11Extension(
        "l2f.interface",
        ["l2f/interface.cpp"],  # Adjust the source file paths as necessary
        include_dirs=include_dirs,
        extra_compile_args=compile_args,
        extra_link_args=link_args,
        language='c++',
        cxx_std=17,  # Ensure C++17 standard
    ),
]

setup(
    name="l2f",
    version="0.0.2",
    description="Python bindings for the L2F (Learning to Fly) Simulator",
    author="Jonas Eschmann",
    author_email="jonas.eschmann@gmail.com",
    packages=find_packages(include=['l2f']),
    include_package_data=True,
    ext_modules=ext_modules,
    cmdclass={"build_ext": ProgressBuildExt},
    python_requires=">=3.8",
    zip_safe=False,  # Required for compiled extensions
)
