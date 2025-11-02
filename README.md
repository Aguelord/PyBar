# PyBar - Neural Network Barcode Scanner

PyBar is a web application optimized for Android devices that uses PyTorch neural networks to scan and recognize barcodes. The app consists of a responsive web interface that captures photos using the device camera and a Python server that processes images using deep learning.

> **🚀 Quick Start - Web Application (Recommended):**
> 1. `python setup_model.py` - Train the model (if not already trained)
> 2. `python server.py` - Start the server
> 3. Open browser to `http://localhost:5000`
>
> See [WEBAPP_README.md](WEBAPP_README.md) for complete web app documentation

> **📱 Legacy Android APK:** The original Kivy-based Android APK version is still available. See [SIMPLE_USAGE.md](SIMPLE_USAGE.md) for APK build instructions.

## Features

### Web Application (New!)
- 📱 **Optimized for Android** devices with responsive design
- 📷 **Camera access** with automatic back camera selection
- 🌐 **Client-server architecture** for better performance
- 🧠 **Pre-trained PyTorch model** on server
- ⚡ **Fast inference** on server with GPU support
- 🎨 **Modern UI** with real-time feedback

### Legacy Features (APK version)
- 📷 Real-time camera preview for barcode scanning
- 🧠 PyTorch-based neural network for barcode recognition
- 📱 Native Android APK support via Kivy/Buildozer
- 🔢 Supports multiple barcode formats (EAN-13, EAN-8, UPC, etc.)
- 🎯 Can read barcode numbers directly or interpret band widths

## Architecture

### Web Application Architecture (Recommended)

```
┌─────────────────┐         ┌─────────────────┐
│   Web Browser   │         │  Python Server  │
│   (Android)     │ HTTPS   │   Flask API     │
│                 │────────>│                 │
│  - Camera       │         │  - PyTorch      │
│  - Capture      │<────────│  - BarcodeNet   │
│  - Display      │  JSON   │  - Detection    │
└─────────────────┘         └─────────────────┘
```

The web application uses:
- **HTML5/CSS3/JavaScript**: Responsive web interface
- **MediaDevices API**: Camera access
- **Flask**: Python web framework for the server
- **PyTorch**: Neural network inference on the server
- **torchvision**: Image preprocessing and ResNet18 model

### Legacy APK Architecture

The original application uses:
- **Kivy**: For the Android UI and camera interface
- **PyTorch**: For the neural network inference
- **torchvision**: For image preprocessing and model architecture
- **ResNet18**: As the backbone for feature extraction

## Project Structure

```
PyBar/
├── server.py                # Flask server application (NEW)
├── static/                  # Web application files (NEW)
│   ├── index.html          # Main HTML page
│   ├── style.css           # Responsive styles
│   └── app.js              # JavaScript application logic
├── barcode_detector.py     # PyTorch neural network detector
├── train_model.py          # Model training script
├── setup_model.py          # Model setup helper (NEW)
├── test_server.py          # Server API tests (NEW)
├── requirements-server.txt # Server dependencies (NEW)
├── WEBAPP_README.md        # Web app documentation (NEW)
├── main.py                 # Legacy Kivy application
├── requirements.txt        # Legacy Kivy dependencies
├── buildozer.spec          # Legacy Android build configuration
└── README.md              # This file
```

## Installation & Setup

### Web Application (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Aguelord/PyBar.git
cd PyBar
```

2. Install dependencies:
```bash
pip install -r requirements-server.txt
```

3. Setup the pre-trained model:
```bash
python setup_model.py
```

4. Start the server:
```bash
python server.py
```

5. Access the application:
   - **Local**: Open browser to `http://localhost:5000`
   - **Android (same network)**: `http://YOUR_IP:5000`
   
For detailed instructions, see [WEBAPP_README.md](WEBAPP_README.md)

### Legacy APK Build (For Development)

1. Clone the repository:
```bash
git clone https://github.com/Aguelord/PyBar.git
cd PyBar
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Train the model:
```bash
python train_model.py
```

4. Run the application:
```bash
python main.py
```

### For Android APK Build

#### Quick Method (Recommended)

Use the Python build script which handles everything automatically:

```bash
python build_apk.py
```

This script will:
- Check and install buildozer if needed
- Verify system dependencies
- Build the Android APK
- On Windows, automatically use WSL if available

The APK will be created in the `bin/` directory.

#### Manual Method - On Linux

1. Install Buildozer:
```bash
pip install buildozer
```

2. Install Android SDK and NDK dependencies:
```bash
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
```

3. Build the APK:
```bash
./build_apk.sh
# or manually: buildozer android debug
```

4. The APK will be in `bin/` directory

#### On Windows

**Recommended Method: Use the Python build script**

Simply run:
```bash
python build_apk.py
```

The script will automatically detect WSL and use it to build the APK.

**Requirements:** WSL2 must be installed. If not installed:

1. Install WSL2 (if not already installed):
```powershell
# Run in PowerShell as Administrator
wsl --install
# Restart your computer after installation
```

2. Run the build script:
```bash
python build_apk.py
```

**📖 For detailed Windows instructions, see [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)**

**Alternative Methods:**

```cmd
# Pull Ubuntu image and run container
docker run -v %CD%:/app -w /app -it ubuntu:22.04 bash

# Inside the container:
apt-get update && apt-get install -y python3-pip git build-essential
pip3 install buildozer
./build_apk.sh
```

**Alternative Method 2: Native Windows (Limited Support)**

Buildozer has limited support for native Windows builds. For best results, use WSL2 or Docker.

#### On macOS

Building Android APKs on macOS requires a Linux environment:
- Use Docker (see Windows Docker method above)
- Use a Linux VM (VirtualBox, Parallels, etc.)
- Use a cloud Linux instance

## Usage

### Web Application

1. **Open the web app** in your browser (mobile or desktop)
2. **Allow camera permissions** when prompted
3. **Point the camera** at a barcode
4. **Press "📸 Capturer"** to take a photo
5. **Press "🔍 Analyser"** to detect the barcode
6. The barcode number will be displayed
7. Press **"🔄 Réessayer"** to scan another barcode

For detailed usage, API documentation, and deployment instructions, see [WEBAPP_README.md](WEBAPP_README.md)

### Legacy APK Application

1. **Launch the app** on your Android device
2. **Point the camera** at a barcode
3. **Press "Scan Barcode"** button
4. The app will display the detected barcode number
5. Press **"Clear"** to reset and scan another barcode

## How It Works

### Web Application Architecture

1. **Camera Capture**: Browser accesses device camera via MediaDevices API
2. **Image Capture**: JavaScript captures photo from video stream as base64
3. **Upload to Server**: Image sent to Flask server via HTTP POST
4. **Preprocessing**: Server converts and resizes image using PIL
5. **Neural Network Inference**: 
   - PyTorch model detects if a barcode is present
   - Predicts each digit position (0-9)
6. **Decoding**: Server converts predictions to barcode number
7. **Response**: Result sent back to browser as JSON
8. **Display**: JavaScript shows the result to the user

### Legacy APK Pipeline

1. **Camera Capture**: Captures frame from device camera
2. **Preprocessing**: Resizes and normalizes the image
3. **Neural Network Inference**: 
   - Detects if a barcode is present
   - Predicts each digit position (0-9)
4. **Decoding**: Converts predictions to barcode number
5. **Display**: Shows the result to the user

### Neural Network Architecture

The `BarcodeNet` model consists of:
- **ResNet18 backbone**: For feature extraction from images
- **Presence head**: Binary classifier (barcode present/absent)
- **Digit heads**: 13 classifiers for each digit position (0-9 + "no digit")

## Training Your Own Model

### Using the Setup Script (Recommended)

```bash
python setup_model.py
```

This script will:
- Check if a model already exists
- Train a new model if needed
- Generate 5000 training samples with synthetic barcodes
- Train for 20 epochs
- Save the best model to `barcode_model.pth` (~45 MB)

### Manual Training

The included `train_model.py` script can also be used directly:

```bash
python train_model.py
```

To use real barcode images, modify the `SyntheticBarcodeDataset` class in `train_model.py` to load your dataset.

## Model Performance

The synthetic training provides a baseline model. For production use:
- Train on real barcode images
- Use data augmentation (rotation, blur, noise)
- Fine-tune on specific barcode types
- Increase training dataset size

## Requirements

### Web Application
- Python 3.8+
- PyTorch 2.0+
- Flask 2.3+
- Modern web browser with camera support
- HTTPS for remote access (camera API requirement)

### Legacy APK
- Python 3.8+
- PyTorch 2.0+
- Kivy 2.2+
- Android device with camera
- 2GB RAM minimum
- Android 5.0+ (API 21+)

## Permissions

### Web Application
The web app requires:
- **Camera access**: Browser permission for camera API
- **HTTPS**: Required for camera access on remote devices (not needed for localhost)

### Legacy APK
The app requires the following Android permissions:
- `CAMERA`: To access device camera
- `WRITE_EXTERNAL_STORAGE`: To save images (optional)
- `READ_EXTERNAL_STORAGE`: To load images (optional)
- `INTERNET`: For potential future features

## Troubleshooting

### Web Application

**Camera not accessible**
- Ensure browser has camera permissions
- For remote access, use HTTPS (not needed for localhost)
- Check if another app/tab is using the camera
- Try a different browser

**Server connection error**
- Verify the server is running: `python server.py`
- Check firewall settings allow port 5000
- Ensure correct IP address and port
- Check server logs for errors

**Model not detecting barcodes**
- Ensure good lighting conditions
- Hold barcode steady and in focus
- Try different angles
- Make sure barcode is supported (8-13 digits)
- Check if model is loaded: visit `/api/health`

**Model not found error**
- Run `python setup_model.py` to train/generate the model
- Ensure `barcode_model.pth` exists in project root

### Legacy APK

**Camera not working**
- Ensure camera permissions are granted
- Check if another app is using the camera
- Restart the app

**Model not detecting barcodes**
- Ensure good lighting conditions
- Hold barcode steady and in focus
- Train model with more diverse data
- Check if barcode is supported format

**APK build fails**
- Ensure all buildozer dependencies are installed
- Check Android SDK/NDK paths
- Review buildozer logs for specific errors
- **Windows users**: Ensure WSL2 is properly installed and configured
- **Windows users**: Verify Linux dependencies are installed inside WSL
- **Docker users**: Increase RAM allocation in Docker settings

**WSL issues on Windows**
- Verify WSL2 is installed: `wsl --version`
- Update WSL: `wsl --update`
- Reinstall distribution: `wsl --install -d Ubuntu-22.04`
- Enable virtualization in BIOS if WSL fails to start
- Check Docker-WSL integration if using Docker

**Build script not executing on Windows**
- Ensure you're using `build_apk.bat` not `build_apk.sh`
- Run from Command Prompt or PowerShell, not Git Bash
- If using WSL directly, ensure line endings are correct: `dos2unix build_apk.sh`

## Future Enhancements

### Web Application
- [ ] Progressive Web App (PWA) support for offline usage
- [ ] Image history and database
- [ ] Batch barcode scanning
- [ ] Export scanned barcodes (CSV, JSON)
- [ ] Production deployment guides (Heroku, AWS, Docker)
- [ ] GPU acceleration support documentation

### General
- [ ] Support for QR codes
- [ ] Real-time continuous scanning
- [ ] Multi-language OCR for text under barcodes
- [ ] Better model with more training data
- [ ] Support for more barcode formats (Code 128, Code 39, etc.)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyTorch team for the deep learning framework
- Kivy team for the Python mobile framework
- ResNet architecture from torchvision

## Contact

For questions or issues, please open an issue on GitHub.

---

**Note**: This is a demonstration project using neural networks for barcode recognition. For production use, consider training on larger, real-world datasets and optimizing the model for mobile deployment.