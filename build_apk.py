#!/usr/bin/env python3
"""
PyBar APK Builder
Simple Python script to build Android APK using Buildozer

Usage:
    python build_apk.py

This script will:
1. Check if buildozer is installed
2. Install buildozer if needed
3. Check for required dependencies
4. Build the Android APK
5. Show the location of the generated APK

The APK will be created in the 'bin/' directory.
"""

import os
import sys
import subprocess
import platform
import shutil


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50 + "\n")


def print_success(text):
    """Print success message"""
    print(f"✓ {text}")


def print_error(text):
    """Print error message"""
    print(f"✗ {text}")


def print_warning(text):
    """Print warning message"""
    print(f"⚠ {text}")


def run_command(cmd, shell=False, check=True, cwd=None):
    """Run a command and return the result"""
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        
        result = subprocess.run(
            cmd, 
            shell=shell, 
            check=check, 
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except Exception as e:
        return False, "", str(e)


def check_command_exists(cmd):
    """Check if a command exists in PATH"""
    return shutil.which(cmd) is not None


def check_buildozer():
    """Check if buildozer is installed"""
    print("Checking for buildozer...")
    
    if check_command_exists('buildozer'):
        print_success("Buildozer is installed")
        return True
    
    print_warning("Buildozer not found")
    return False


def install_buildozer():
    """Install buildozer using pip"""
    print("Installing buildozer...")
    
    success, stdout, stderr = run_command([sys.executable, "-m", "pip", "install", "buildozer"])
    
    if success:
        print_success("Buildozer installed successfully")
        return True
    else:
        print_error("Failed to install buildozer")
        print(stderr)
        return False


def check_dependencies():
    """Check for required system dependencies"""
    print("Checking system dependencies...")
    
    required_commands = ['git', 'zip', 'unzip']
    missing = []
    
    for cmd in required_commands:
        if not check_command_exists(cmd):
            missing.append(cmd)
    
    if missing:
        print_warning(f"Missing dependencies: {', '.join(missing)}")
        print("\nPlease install missing dependencies:")
        
        system = platform.system()
        if system == "Linux":
            print("  sudo apt-get install -y " + " ".join(missing))
        elif system == "Darwin":
            print("  brew install " + " ".join(missing))
        else:
            print("  Please install manually: " + ", ".join(missing))
        
        return False
    
    print_success("All required dependencies found")
    return True


def check_wsl_on_windows():
    """Check if WSL is available on Windows"""
    if platform.system() != "Windows":
        return False
    
    success, stdout, stderr = run_command(["wsl", "--version"], check=False)
    return success


def build_apk_wsl():
    """Build APK using WSL on Windows"""
    print_header("Building APK using WSL")
    
    print("Converting Windows path to WSL path...")
    current_dir = os.getcwd()
    
    # Convert Windows path to WSL path using proper quoting
    success, wsl_path, stderr = run_command(['wsl', 'wslpath', '-u', current_dir], check=False)
    
    if not success:
        print_error("Failed to convert path to WSL format")
        return False
    
    wsl_path = wsl_path.strip()
    print(f"WSL path: {wsl_path}")
    
    # Check if buildozer is installed in WSL
    print("\nChecking buildozer in WSL...")
    success, stdout, stderr = run_command(['wsl', 'bash', '-c', 'command -v buildozer'], check=False)
    
    if not success:
        print_warning("Buildozer not found in WSL. Installing...")
        success, stdout, stderr = run_command(['wsl', 'bash', '-c', 'pip3 install buildozer'], check=False)
        if not success:
            print_error("Failed to install buildozer in WSL")
            return False
        print_success("Buildozer installed in WSL")
    
    # Build the APK using WSL
    print("\nStarting APK build in WSL...")
    print("This may take 30-60 minutes on first build")
    print("(downloads Android SDK, NDK, and dependencies)\n")
    
    # Use proper command list to avoid shell injection
    build_cmd = ['wsl', 'bash', '-c', f'cd "{wsl_path}" && buildozer android debug']
    
    # Run without capturing output so user can see progress
    result = subprocess.run(build_cmd)
    
    return result.returncode == 0


def clean_build_artifacts():
    """Clean previous build artifacts"""
    print("Cleaning previous build artifacts...")
    
    buildozer_dir = os.path.join(os.getcwd(), ".buildozer")
    if os.path.exists(buildozer_dir):
        build_dir = os.path.join(buildozer_dir, "android", "platform")
        if os.path.exists(build_dir):
            # Remove build-* directories
            for item in os.listdir(build_dir):
                if item.startswith("build-"):
                    item_path = os.path.join(build_dir, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
            print_success("Cleaned build artifacts")
    else:
        print("No previous build artifacts found")


def build_apk_direct():
    """Build APK directly using buildozer"""
    print_header("Building APK")
    
    print("Starting APK build...")
    print("This may take 30-60 minutes on first build")
    print("(downloads Android SDK, NDK, and dependencies)\n")
    
    # Run buildozer directly
    result = subprocess.run(["buildozer", "android", "debug"])
    
    return result.returncode == 0


def main():
    """Main function"""
    print_header("PyBar Android APK Builder")
    
    # Detect platform
    system = platform.system()
    print(f"Detected platform: {system}\n")
    
    # Windows-specific handling
    if system == "Windows":
        print("Windows detected. Checking for WSL...")
        if check_wsl_on_windows():
            print_success("WSL is available")
            print("\nNote: Buildozer requires a Linux environment.")
            print("Building APK using WSL...\n")
            
            success = build_apk_wsl()
        else:
            print_error("WSL is not installed or not available")
            print("\nBuildozer requires a Linux environment to build Android APKs.")
            print("Please use one of the following methods:\n")
            print("1. Install WSL2 (Recommended):")
            print("   - Open PowerShell as Administrator")
            print("   - Run: wsl --install")
            print("   - Restart your computer")
            print("   - Then run this script again\n")
            print("2. Use Docker:")
            print("   docker run -v %CD%:/app -w /app -it ubuntu:22.04 bash")
            print("   # Inside the container, run:")
            print("   pip3 install buildozer")
            print("   python3 build_apk.py\n")
            print("3. Use a Linux VM (VirtualBox, VMware, etc.)\n")
            return 1
    else:
        # Linux or macOS
        # Check for buildozer
        if not check_buildozer():
            print("\nAttempting to install buildozer...")
            if not install_buildozer():
                print_error("Failed to install buildozer")
                return 1
        
        # Check dependencies
        if not check_dependencies():
            print_error("Missing required dependencies")
            print("\nPlease install the missing dependencies and try again.")
            return 1
        
        # Clean previous builds (optional)
        # clean_build_artifacts()
        
        # Build APK
        success = build_apk_direct()
    
    # Check result
    if success:
        print_header("BUILD SUCCESSFUL!")
        
        # Find the APK file
        bin_dir = os.path.join(os.getcwd(), "bin")
        if os.path.exists(bin_dir):
            apk_files = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
            if apk_files:
                # Sort by modification time to get the most recent
                apk_files.sort(key=lambda f: os.path.getmtime(os.path.join(bin_dir, f)), reverse=True)
                apk_path = os.path.join(bin_dir, apk_files[0])
                print(f"APK location: {apk_path}\n")
                
                print("To install on your Android device:\n")
                print("Option 1 - Using ADB (USB debugging):")
                print(f"  adb install {apk_path}\n")
                print("Option 2 - Manual transfer:")
                print(f"  1. Copy the APK file to your device")
                print(f"  2. Open the APK file on your device")
                print(f"  3. Follow the installation prompts\n")
                print("Option 3 - Using a file server:")
                print(f"  python3 -m http.server 8000")
                print(f"  Then access http://<your-ip>:8000/bin/ from your Android browser\n")
        
        return 0
    else:
        print_header("BUILD FAILED")
        print("\nCheck the logs above for errors.")
        print("Common issues:")
        print("  - Missing system dependencies")
        print("  - SDK/NDK download failures")
        print("  - Insufficient disk space")
        print("  - Network connectivity issues\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
