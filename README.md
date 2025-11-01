# PyBar - Neural Network Barcode Scanner for Android

PyBar is an Android application built with Python that uses PyTorch neural networks to scan and recognize barcodes. The app captures barcode images using the device camera and extracts the barcode number using deep learning.

## Features

- 📷 Real-time camera preview for barcode scanning
- 🧠 PyTorch-based neural network for barcode recognition
- 📱 Native Android APK support via Kivy/Buildozer
- 🔢 Supports multiple barcode formats (EAN-13, EAN-8, UPC, etc.)
- 🎯 Can read barcode numbers directly or interpret band widths

## Architecture

The application uses:
- **Kivy**: For the Android UI and camera interface
- **PyTorch**: For the neural network inference
- **torchvision**: For image preprocessing and model architecture
- **ResNet18**: As the backbone for feature extraction

## Project Structure

```
PyBar/
├── main.py                 # Main Kivy application
├── barcode_detector.py     # PyTorch neural network detector
├── train_model.py         # Model training script
├── requirements.txt       # Python dependencies
├── buildozer.spec         # Android build configuration
└── README.md             # This file
```

## Installation & Setup

### For Development (Desktop)

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

1. Install Buildozer:
```bash
pip install buildozer
```

2. Install Android SDK and NDK dependencies (Linux):
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
buildozer android debug
```

4. The APK will be in `bin/` directory

## Usage

1. **Launch the app** on your Android device
2. **Point the camera** at a barcode
3. **Press "Scan Barcode"** button
4. The app will display the detected barcode number
5. Press **"Clear"** to reset and scan another barcode

## How It Works

### Barcode Detection Pipeline

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

The included `train_model.py` script generates synthetic barcode images for training:

```bash
python train_model.py
```

This will:
- Generate 5000 training samples with synthetic barcodes
- Train for 20 epochs
- Save the best model to `barcode_model.pth`

To use real barcode images, modify the `SyntheticBarcodeDataset` class to load your dataset.

## Model Performance

The synthetic training provides a baseline model. For production use:
- Train on real barcode images
- Use data augmentation (rotation, blur, noise)
- Fine-tune on specific barcode types
- Increase training dataset size

## Requirements

- Python 3.8+
- PyTorch 2.0+
- Kivy 2.2+
- Android device with camera (for APK)
- 2GB RAM minimum
- Android 5.0+ (API 21+)

## Permissions

The app requires the following Android permissions:
- `CAMERA`: To access device camera
- `WRITE_EXTERNAL_STORAGE`: To save images (optional)
- `READ_EXTERNAL_STORAGE`: To load images (optional)
- `INTERNET`: For potential future features

## Troubleshooting

### Camera not working
- Ensure camera permissions are granted
- Check if another app is using the camera
- Restart the app

### Model not detecting barcodes
- Ensure good lighting conditions
- Hold barcode steady and in focus
- Train model with more diverse data
- Check if barcode is supported format

### APK build fails
- Ensure all buildozer dependencies are installed
- Check Android SDK/NDK paths
- Review buildozer logs for specific errors

## Future Enhancements

- [ ] Support for QR codes
- [ ] Real-time continuous scanning
- [ ] Barcode history and database
- [ ] Export scanned barcodes
- [ ] Multi-language OCR for text under barcodes
- [ ] Better model with more training data

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