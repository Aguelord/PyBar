@echo off
REM Build script for PyBar Android APK on Windows
REM Note: This script requires WSL (Windows Subsystem for Linux) to be installed
REM For native Windows builds, see the documentation for Docker alternatives

echo ========================================
echo PyBar Android APK Build Script (Windows)
echo ========================================
echo.

REM Note: If this script is run directly inside WSL, it will be detected by the shell
REM and the bash script should be used instead. This script is for Windows CMD/PowerShell.

REM Check if WSL is available
wsl --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: WSL is not installed or not available
    echo.
    echo Buildozer requires a Linux environment to build Android APKs.
    echo Please use one of the following methods:
    echo.
    echo 1. Install WSL2 ^(Recommended^):
    echo    - Open PowerShell as Administrator
    echo    - Run: wsl --install
    echo    - Restart your computer
    echo    - Then run this script again
    echo.
    echo 2. Use Docker:
    echo    docker run -v %CD%:/app -w /app -it ubuntu:22.04 bash
    echo    # Inside the container, run:
    echo    apt-get update ^&^& apt-get install -y python3-pip git
    echo    pip3 install buildozer
    echo    ./build_apk.sh
    echo.
    echo 3. Use a Linux VM ^(VirtualBox, VMware, etc.^)
    echo.
    exit /b 1
)

echo WSL is available!
echo.

REM Check if buildozer is installed in WSL
echo Checking WSL environment...
wsl bash -c "command -v buildozer" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Buildozer not found in WSL. Installing...
    wsl bash -c "pip3 install buildozer"
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to install buildozer in WSL
        exit /b 1
    )
)

echo.
echo ========================================
echo Starting APK build in WSL...
echo ========================================
echo.
echo This may take 30-60 minutes on first build
echo ^(downloads Android SDK, NDK, and dependencies^)
echo.

REM Get the WSL path for the current directory
for /f "delims=" %%i in ('wsl wslpath -u "%CD%"') do set WSLPATH=%%i

REM Change to the script directory and run build_apk.sh in WSL
wsl bash -c "cd '%WSLPATH%' && ./build_apk.sh"

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo APK location: bin\pybar-1.0-arm64-v8a-debug.apk
    echo.
    echo To install on device:
    echo   adb install bin\pybar-1.0-arm64-v8a-debug.apk
    echo.
) else (
    echo.
    echo ========================================
    echo BUILD FAILED
    echo ========================================
    echo.
    echo Check the logs above for errors.
    echo Common issues:
    echo   - Missing system dependencies in WSL
    echo   - SDK/NDK download failures
    echo   - Insufficient disk space
    echo.
    echo To troubleshoot in WSL:
    echo   wsl bash
    echo   cd ^<your project path^>
    echo   ./build_apk.sh
    echo.
    exit /b 1
)
