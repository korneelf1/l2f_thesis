import sys
import os
import time
import subprocess
import shutil
from setuptools import setup, find_packages, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

debug = False
optimization = True

def get_compile_args():
    """Get compile arguments with fallbacks for different environments."""
    # Define platform-specific compile and link arguments
    if optimization:
        compile_args = {
            'msvc': ['/O2', '/fp:fast'],
            'unix': ['-Ofast', '-march=native'],
            'macos': ['-Ofast', '-march=native', '-mmacosx-version-min=10.14'],
        }
    else:
        compile_args = {
            'msvc': [],
            'unix': [],
            'macos': [],
        }
    
    if debug:
        compile_args['msvc'] += ['/Zi', '/Od', '/D_DEBUG']
        compile_args['unix'] += ['-g', '-D_DEBUG']
        compile_args['macos'] += ['-g', '-D_DEBUG']
    
    # Determine the platform and select the appropriate arguments
    if sys.platform == "win32":
        return compile_args['msvc']
    elif sys.platform == "darwin":
        return compile_args['macos']
    else:
        return compile_args['unix']

def get_link_args():
    """Get link arguments."""
    link_args = {
        'msvc': [],
        'unix': [],
        'macos': [],
    }
    
    # Determine the platform and select the appropriate arguments
    if sys.platform == "win32":
        return link_args['msvc']
    elif sys.platform == "darwin":
        return link_args['macos']
    else:
        return link_args['unix']

class ProgressBuildExt(build_ext):
    """Custom build extension with progress indicators."""
    
    def run(self):
        print("🚀 Starting L2F package build...")
        print("📦 Installing build dependencies...")
        
        # Ensure external dependencies are available
        self.ensure_external_dependencies()
        
        # Build external dependencies with CMake
        self.build_external_dependencies()
        
        super().run()
        print("✅ Build completed successfully!")
    
    def ensure_external_dependencies(self):
        """Ensure external C++ dependencies are properly set up."""
        print("🔍 Checking external dependencies...")
        
        # Check if external/rl-tools exists and has the required files
        external_path = "external/rl-tools"
        if not os.path.exists(external_path):
            print("❌ External rl-tools directory not found!")
            print("   Make sure you have cloned the repository with external dependencies")
            raise FileNotFoundError("external/rl-tools directory not found")
        
        # Check for key header files
        key_headers = [
            "external/rl-tools/include/rl_tools/rl/environments/l2f/parameters/default.h",
            "external/rl-tools/include/rl_tools/rl/environments/l2f/operations_cpu.h"
        ]
        
        for header in key_headers:
            if not os.path.exists(header):
                print(f"❌ Required header not found: {header}")
                raise FileNotFoundError(f"Required header not found: {header}")
        
        print("✅ External dependencies verified")
    
    def build_external_dependencies(self):
        """Build external rl-tools dependencies using CMake."""
        print("🔨 Building external rl-tools dependencies with CMake...")
        
        # Check if CMake is available
        try:
            subprocess.run(["cmake", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ CMake not found. Skipping external dependency build.")
            print("   This may cause segmentation faults during runtime.")
            print("   To fix: install CMake and rebuild the package.")
            return
        
        external_path = "external/rl-tools"
        build_path = os.path.join(external_path, "build")
        
        # Create build directory
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        os.makedirs(build_path, exist_ok=True)
        
        try:
            # Configure CMake
            print("   Configuring CMake...")
            cmake_args = [
                "cmake", "..",
                "-DCMAKE_BUILD_TYPE=Release",
                "-DRL_TOOLS_ENABLE_TARGETS=OFF",
                "-DRL_TOOLS_ENABLE_TESTS=OFF",
                "-DRL_TOOLS_BACKEND_ENABLE_MKL=OFF",
                "-DRL_TOOLS_BACKEND_ENABLE_ACCELERATE=OFF",
                "-DRL_TOOLS_BACKEND_ENABLE_CUDA=OFF",
                "-DRL_TOOLS_RL_ENVIRONMENTS_ENABLE_MUJOCO=OFF",
                "-DRL_TOOLS_ENABLE_JSON=OFF",
                "-DRL_TOOLS_ENABLE_CJSON=OFF",
                "-DRL_TOOLS_ENABLE_BOOST_BEAST=OFF",
                "-DRL_TOOLS_ENABLE_LIBWEBSOCKETS=OFF",
                "-DRL_TOOLS_ENABLE_TRACY=OFF",
                "-DRL_TOOLS_ENABLE_LTO=OFF",
                "-DRL_TOOLS_DISABLE_FAST_MATH=OFF",
                "-DRL_TOOLS_WARNINGS_AS_ERRORS=OFF",
                "-DRL_TOOLS_DISABLE_CPU_SPECIFIC_OPTIMIZATIONS=ON"
            ]
            
            result = subprocess.run(
                cmake_args,
                cwd=build_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ CMake configuration failed:")
                print(f"   stdout: {result.stdout}")
                print(f"   stderr: {result.stderr}")
                raise RuntimeError("CMake configuration failed")
            
            print("✅ CMake configuration successful")
            
            # Build with CMake
            print("   Building with CMake...")
            build_args = ["cmake", "--build", ".", "--config", "Release"]
            
            result = subprocess.run(
                build_args,
                cwd=build_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ CMake build failed:")
                print(f"   stdout: {result.stdout}")
                print(f"   stderr: {result.stderr}")
                raise RuntimeError("CMake build failed")
            
            print("✅ External dependencies built successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ CMake build failed: {e}")
            raise
        except FileNotFoundError:
            print("❌ CMake not found. Please install CMake:")
            if sys.platform == "darwin":
                print("   brew install cmake")
            elif sys.platform == "linux":
                print("   sudo apt-get install cmake")
            else:
                print("   Install CMake from https://cmake.org/download/")
            raise
    
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
