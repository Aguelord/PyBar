"""
Test script for barcode detection functionality
Tests the BarcodeDetector class with synthetic images
"""

import torch
from barcode_detector import BarcodeDetector, BarcodeNet
from PIL import Image, ImageDraw
import numpy as np
import tempfile
import os

def create_test_barcode_image(barcode_number, size=(224, 224)):
    """Create a simple test barcode image"""
    width, height = size
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw vertical bars
    bar_width = width // (len(barcode_number) * 2 + 2)
    x_offset = bar_width
    
    for i, digit in enumerate(barcode_number):
        digit_val = int(digit)
        
        # Draw bars based on digit value
        for j in range(4):
            if (digit_val >> j) & 1:
                x1 = x_offset + j * bar_width // 4
                draw.rectangle([x1, height // 4, x1 + bar_width // 4, 3 * height // 4], 
                             fill='black')
        
        x_offset += bar_width * 2
    
    # Add number text
    draw.text((width // 2, 7 * height // 8), barcode_number, 
             fill='black', anchor='mm')
    
    return image

def test_barcode_net():
    """Test BarcodeNet model architecture"""
    print("Testing BarcodeNet architecture...")
    
    model = BarcodeNet()
    
    # Test forward pass
    batch_size = 2
    test_input = torch.randn(batch_size, 3, 224, 224)
    
    presence_logits, digit_logits = model(test_input)
    
    print(f"Input shape: {test_input.shape}")
    print(f"Presence logits shape: {presence_logits.shape}")
    print(f"Digit logits shape: {digit_logits.shape}")
    
    assert presence_logits.shape == (batch_size, 2), "Presence output shape mismatch"
    assert digit_logits.shape == (batch_size, 13, 11), "Digit output shape mismatch"
    
    print("✓ BarcodeNet architecture test passed!\n")

def test_detector_initialization():
    """Test BarcodeDetector initialization"""
    print("Testing BarcodeDetector initialization...")
    
    detector = BarcodeDetector()
    
    assert detector.model is not None, "Model not initialized"
    assert detector.device is not None, "Device not set"
    
    print(f"Device: {detector.device}")
    print("✓ BarcodeDetector initialization test passed!\n")

def test_image_processing():
    """Test image processing functionality"""
    print("Testing image processing...")
    
    detector = BarcodeDetector()
    
    # Create test image
    test_image = create_test_barcode_image("1234567890123")
    
    # Convert to numpy array (simulate camera data)
    image_array = np.array(test_image)
    width, height = test_image.size
    
    # Flatten to bytes
    image_bytes = image_array.tobytes()
    
    # Test processing
    processed_image = detector._process_image_data(image_bytes, (width, height))
    
    assert processed_image is not None, "Image processing failed"
    assert processed_image.size == test_image.size, "Image size mismatch"
    
    print(f"Processed image size: {processed_image.size}")
    print("✓ Image processing test passed!\n")

def test_barcode_detection():
    """Test barcode detection with synthetic image"""
    print("Testing barcode detection...")
    
    detector = BarcodeDetector()
    
    # Test with a synthetic barcode
    test_barcode = "9876543210123"
    test_image = create_test_barcode_image(test_barcode)
    
    # Save test image to temporary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.png', delete=False) as tmp_file:
        test_image.save(tmp_file.name)
        tmp_path = tmp_file.name
    
    print(f"Test barcode image saved to {tmp_path}")
    
    # Test detection from file
    result = detector.detect_from_file(tmp_path)
    
    # Clean up
    try:
        os.unlink(tmp_path)
    except:
        pass
    
    print(f"Test barcode: {test_barcode}")
    print(f"Detected: {result}")
    
    # Note: Without training, the model will likely not detect correctly
    # This test validates the pipeline works, not accuracy
    if result:
        print(f"✓ Detection pipeline successful (returned: {result})")
    else:
        print("✓ Detection pipeline successful (no detection - model needs training)")
    
    print()

def test_digit_decoding():
    """Test digit decoding logic"""
    print("Testing digit decoding...")
    
    detector = BarcodeDetector()
    
    # Create mock digit logits
    batch_size = 1
    num_positions = 13
    num_classes = 11
    
    # Create logits that predict specific digits
    digit_logits = torch.zeros(batch_size, num_positions, num_classes)
    
    # Set first 10 positions to predict 0-9, rest to "no digit" (10)
    for i in range(10):
        digit_logits[0, i, i] = 10.0  # High logit for digit i
    digit_logits[0, 10:, 10] = 10.0  # High logit for "no digit"
    
    result = detector._decode_digits(digit_logits)
    
    expected = "0123456789"
    print(f"Expected: {expected}")
    print(f"Decoded: {result}")
    
    assert result == expected, f"Decoding mismatch: expected {expected}, got {result}"
    
    print("✓ Digit decoding test passed!\n")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("PyBar Barcode Detector Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_barcode_net()
        test_detector_initialization()
        test_image_processing()
        test_digit_decoding()
        test_barcode_detection()
        
        print("=" * 60)
        print("All tests completed successfully! ✓")
        print("=" * 60)
        print()
        print("Note: The model needs training to accurately detect barcodes.")
        print("Run 'python train_model.py' to train the model.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
