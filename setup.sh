#!/bin/bash
# Setup script for PyBar development environment

echo "========================================"
echo "PyBar Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION"
echo ""

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
    echo "To activate it, run:"
    echo "  source venv/bin/activate"
    echo ""
else
    echo "✓ Virtual environment already exists"
    echo ""
fi

# Install Python dependencies
echo "Installing Python dependencies..."
echo ""

# Check if CUDA is available for GPU support
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU detected, installing PyTorch with CUDA support"
    pip install -r requirements.txt
else
    echo "ℹ No NVIDIA GPU detected, installing CPU-only PyTorch"
    pip install -r requirements.txt --index-url https://download.pytorch.org/whl/cpu
fi

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "⚠ Some dependencies failed to install"
    echo "You may need to install them manually"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Test the detector:"
echo "   python demo.py"
echo ""
echo "2. Run the full test suite:"
echo "   python test_detector.py"
echo ""
echo "3. (Optional) Train the model:"
echo "   python train_model.py"
echo ""
echo "4. To build Android APK:"
echo "   ./build_apk.sh"
echo ""
echo "========================================"
