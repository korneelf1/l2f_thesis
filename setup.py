import sys
import os
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
        else:
            # Use more conservative optimization flags that work across environments
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
    return link_args

# Get platform-specific arguments
compile_args = get_compile_args()
link_args = get_link_args()

ext_modules = [
    Pybind11Extension(
        "l2f.interface",
        ["l2f/interface.cpp"],  # Adjust the source file paths as necessary
        include_dirs=["external/rl-tools/include"],
        extra_compile_args=compile_args,
        extra_link_args=link_args,
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
    cmdclass={"build_ext": build_ext},
    python_requires=">=3.8",
    zip_safe=False,  # Required for compiled extensions
)
