@echo off
REM Setup script for PyBar development environment on Windows

echo ========================================
echo PyBar Setup Script (Windows)
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% found
echo.

REM Create virtual environment (recommended)
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo WARNING: Failed to create virtual environment
        echo Continuing with global Python installation...
    ) else (
        echo Virtual environment created
        echo.
        echo To activate it, run:
        echo   venv\Scripts\activate
        echo.
    )
) else (
    echo Virtual environment already exists
    echo.
)

REM Install Python dependencies
echo Installing Python dependencies...
echo.
echo NOTE: For Android APK building, you will need WSL or Docker.
echo This setup only installs dependencies for desktop development.
echo.

REM Install dependencies - PyTorch installation is the same from requirements.txt
REM For CPU-only PyTorch on systems without CUDA, use a different index URL
where nvidia-smi >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo NVIDIA GPU detected, installing PyTorch with CUDA support
    pip install -r requirements.txt
) else (
    echo No NVIDIA GPU detected, installing CPU-only PyTorch
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    pip install -r requirements.txt
)

if %ERRORLEVEL% equ 0 (
    echo.
    echo Dependencies installed successfully!
) else (
    echo.
    echo WARNING: Some dependencies failed to install
    echo You may need to install them manually
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Test the detector:
echo    python demo.py
echo.
echo 2. Run the full test suite:
echo    python test_detector.py
echo.
echo 3. ^(Optional^) Train the model:
echo    python train_model.py
echo.
echo 4. To build Android APK:
echo    - Install WSL2: wsl --install
echo    - Then run: build_apk.bat
echo    - Or see README.md for Docker/VM alternatives
echo.
echo ========================================
