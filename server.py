"""
Flask server for barcode detection
Receives images from web app and returns detected barcode numbers
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
from barcode_detector import BarcodeDetector
from PIL import Image
import io
import os
import base64
import tempfile

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Enable CORS for cross-origin requests

# Initialize the barcode detector with pre-trained model
MODEL_PATH = 'barcode_model.pth'
detector = None

def init_detector():
    """Initialize the barcode detector"""
    global detector
    if os.path.exists(MODEL_PATH):
        detector = BarcodeDetector(model_path=MODEL_PATH)
        print(f"Loaded pre-trained model from {MODEL_PATH}")
    else:
        detector = BarcodeDetector()
        print("Warning: No pre-trained model found, using untrained model")

@app.route('/')
def index():
    """Serve the main web application"""
    return send_from_directory('static', 'index.html')

@app.route('/api/detect', methods=['POST'])
def detect_barcode():
    """
    API endpoint to detect barcode from uploaded image
    Expects: JSON with base64 encoded image data
    Returns: JSON with detected barcode number or error
    """
    try:
        # Get image data from request
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = data['image']
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        
        # Open image with PIL
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Save temporarily for processing
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.jpg', delete=False)
        temp_path = temp_file.name
        temp_file.close()
        image.save(temp_path)
        
        # Detect barcode
        if detector is None:
            return jsonify({'error': 'Detector not initialized'}), 500
        
        barcode_number = detector.detect_from_file(temp_path)
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except OSError:
            pass
        
        if barcode_number:
            return jsonify({
                'success': True,
                'barcode': barcode_number
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No barcode detected in image'
            })
    
    except Exception as e:
        print(f"Error processing image: {e}")
        import traceback
        traceback.print_exc()
        # Don't expose internal error details to client in production
        return jsonify({'error': 'Internal server error processing image'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector is not None,
        'model_path': MODEL_PATH if os.path.exists(MODEL_PATH) else 'No model'
    })

if __name__ == '__main__':
    # Initialize detector on startup
    init_detector()
    
    # Run server
    port = int(os.environ.get('PORT', 5000))
    # Debug mode should only be enabled in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
