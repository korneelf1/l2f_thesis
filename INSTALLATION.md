# L2F Installation Guide

This guide provides installation instructions for the L2F (Learning to Fly) Python package across different environments.

## Quick Installation

### Local Development
```bash
pip install .
```

### Google Colab / Jupyter Notebooks
```bash
# Run this in a Colab cell
!python install_colab.py
```

## Environment-Specific Instructions

### 1. Google Colab

Google Colab has some restrictions that can cause build issues. Use the provided installation script:

```python
# In a Colab cell
!git clone <your-repo-url>
%cd <repo-directory>
!python install_colab.py
```

### 2. Local Development (macOS/Linux)

```bash
# Clone the repository
git clone <your-repo-url>
cd l2f_thesis

# Install dependencies
pip install --upgrade setuptools pybind11

# Install the package
pip install .
```

### 3. Windows

```bash
# Install Visual Studio Build Tools first
# Then install the package
pip install .
```

### 4. Docker

```dockerfile
FROM python:3.9-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade setuptools pybind11

# Copy and install the package
COPY . /app
WORKDIR /app
RUN pip install .
```

## Troubleshooting

### Common Issues

1. **Build fails with compiler errors**
   - Try: `pip install --no-cache-dir .`
   - Check that `external/rl-tools/include` exists
   - Ensure you have a C++ compiler installed

2. **Colab-specific issues**
   - Use the `install_colab.py` script
   - The script automatically detects Colab and uses conservative compiler flags

3. **Memory issues during build**
   - Try: `pip install --no-cache-dir .`
   - Close other applications to free up memory

4. **Permission errors**
   - Use: `pip install --user .` for user installation
   - Or use a virtual environment

### Debug Information

Run the debug script to get detailed environment information:

```bash
python build_debug.py
```

This will show:
- Python version and platform information
- Available compilers
- Environment variables
- Package versions

### Build Configuration

The package automatically detects the environment and uses appropriate compiler flags:

- **Development environments**: Uses aggressive optimizations (`-O3`, `-ffast-math`)
- **CI/Colab environments**: Uses conservative optimizations (`-O3` only)
- **Debug mode**: Adds debug symbols (`-g`, `-D_DEBUG`)

## Requirements

- Python >= 3.8
- C++ compiler (GCC, Clang, or MSVC)
- setuptools >= 45
- pybind11 >= 2.6

## Dependencies

The package depends on:
- `external/rl-tools` (included as submodule)
- pybind11 (for Python bindings)
- Standard C++17 library

## Support

If you encounter issues:

1. Run `python build_debug.py` and share the output
2. Check that all requirements are met
3. Try the environment-specific installation methods above
4. Open an issue with detailed error messages
