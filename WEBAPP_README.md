# PyBar Web Application

## Overview

PyBar is now a web application optimized for Android devices that uses PyTorch neural networks to detect and recognize barcodes. The application consists of:

1. **Web Client**: A responsive web interface that captures photos using the device camera
2. **Python Server**: A Flask server that processes images using a pre-trained PyTorch model

## Architecture

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

## Features

- 📱 Optimized for Android devices
- 📷 Native camera access with back camera preference
- 🧠 Pre-trained PyTorch neural network for barcode detection
- 🚀 Fast server-side inference
- 🎨 Modern, responsive UI
- ⚡ Real-time image capture and analysis

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Aguelord/PyBar.git
cd PyBar
```

2. Install dependencies:
```bash
pip install -r requirements-server.txt
```

3. Ensure you have a trained model (should already be included):
```bash
# The repository includes a pre-trained model: barcode_model.pth
# If you need to retrain: python train_model.py
```

## Usage

### Starting the Server

```bash
python server.py
```

The server will start on `http://localhost:5000` by default.

### Accessing the Web Application

1. **On the same device**:
   - Open a browser and navigate to `http://localhost:5000`

2. **On Android device (local network)**:
   - Find your computer's IP address:
     - Linux/Mac: `ifconfig` or `ip addr`
     - Windows: `ipconfig`
   - On your Android device, open a browser and navigate to `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

3. **Production deployment**:
   - Deploy to a cloud server (Heroku, AWS, Google Cloud, etc.)
   - Use a production WSGI server like Gunicorn
   - Enable HTTPS for secure camera access

### Using the Application

1. Allow camera permissions when prompted
2. Point your camera at a barcode
3. Click "📸 Capturer" to take a photo
4. Click "🔍 Analyser" to detect the barcode
5. The barcode number will be displayed
6. Click "🔄 Réessayer" to scan another barcode

## API Documentation

### Endpoints

#### `GET /`
Serves the web application

#### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "barcode_model.pth"
}
```

#### `POST /api/detect`
Detect barcode from image

**Request:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

**Response (Success):**
```json
{
  "success": true,
  "barcode": "1234567890123"
}
```

**Response (No barcode):**
```json
{
  "success": false,
  "message": "No barcode detected in image"
}
```

**Response (Error):**
```json
{
  "error": "Error message"
}
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 server:app
```

### Environment Variables

- `PORT`: Server port (default: 5000)

### HTTPS Configuration

For camera access on mobile devices, HTTPS is required (except for localhost). Use:
- Reverse proxy (nginx) with SSL certificate
- Cloud platform's built-in HTTPS (Heroku, Google Cloud Run, etc.)
- Let's Encrypt for free SSL certificates

## Model Information

The pre-trained model (`barcode_model.pth`) is a ResNet18-based neural network trained on synthetic barcode images. It can detect:

- EAN-13 barcodes
- EAN-8 barcodes
- UPC barcodes
- 8-13 digit barcodes

### Model Performance

The model is trained on synthetic data. For better performance:
- Train on real barcode images
- Increase dataset size
- Apply data augmentation

### Retraining

To retrain the model:

```bash
python train_model.py
```

This will generate a new `barcode_model.pth` file.

## Browser Compatibility

- Chrome/Chromium (Android): ✅ Fully supported
- Firefox (Android): ✅ Supported
- Samsung Internet: ✅ Supported
- Safari (iOS): ✅ Supported with HTTPS

## Troubleshooting

### Camera not accessible
- Ensure the website has camera permissions
- For remote access, use HTTPS
- Check if another app is using the camera

### Server connection error
- Verify the server is running
- Check firewall settings
- Ensure correct IP address and port

### No barcode detected
- Ensure good lighting conditions
- Hold the barcode steady and in focus
- Try different angles
- Make sure the barcode is supported (8-13 digits)

### Model not found
- Ensure `barcode_model.pth` exists in the project root
- Run `python train_model.py` to generate a new model

## Development

### Project Structure

```
PyBar/
├── server.py                 # Flask server application
├── barcode_detector.py       # PyTorch neural network detector
├── train_model.py           # Model training script
├── barcode_model.pth        # Pre-trained model (45 MB)
├── requirements-server.txt  # Python dependencies
└── static/                  # Web application files
    ├── index.html           # Main HTML page
    ├── style.css            # Styles
    └── app.js               # JavaScript application logic
```

### Technologies Used

**Backend:**
- Flask: Web framework
- PyTorch: Neural network inference
- torchvision: Image preprocessing and ResNet18 model
- Pillow: Image processing

**Frontend:**
- HTML5: Structure
- CSS3: Responsive styling with mobile optimization
- JavaScript: Camera API and server communication
- MediaDevices API: Camera access

## License

MIT License - see LICENSE file

## Contributing

Contributions are welcome! Please submit pull requests or open issues.

## Contact

For questions or support, please open an issue on GitHub.
