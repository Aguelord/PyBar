"""
Demo script to test barcode detection without running the full Kivy app
This script tests the barcode detector with a sample image
"""

from barcode_detector import BarcodeDetector
from PIL import Image, ImageDraw, ImageFont
import sys

def create_demo_barcode(barcode_number="1234567890128"):
    """Create a demo barcode image"""
    width, height = 400, 200
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw title
    draw.text((width // 2, 20), "Demo Barcode", fill='black', anchor='mm')
    
    # Draw simple barcode bars
    bar_width = width // (len(barcode_number) * 2 + 2)
    x_offset = bar_width
    
    for i, digit in enumerate(barcode_number):
        digit_val = int(digit)
        
        # Draw bars based on digit value (simple encoding)
        for j in range(4):
            if (digit_val >> j) & 1:
                x1 = x_offset + j * bar_width // 4
                draw.rectangle([x1, 60, x1 + bar_width // 4, 140], 
                             fill='black')
        
        x_offset += bar_width * 2
    
    # Draw number text below barcode
    draw.text((width // 2, 170), barcode_number, fill='black', anchor='mm')
    
    return image, barcode_number

def main():
    print("=" * 60)
    print("PyBar Barcode Scanner - Demo Script")
    print("=" * 60)
    print()
    
    # Create demo barcode
    print("Creating demo barcode image...")
    demo_image, actual_barcode = create_demo_barcode()
    demo_path = '/tmp/demo_barcode.png'
    demo_image.save(demo_path)
    print(f"✓ Demo barcode saved to: {demo_path}")
    print(f"  Actual barcode number: {actual_barcode}")
    print()
    
    # Initialize detector
    print("Initializing barcode detector...")
    try:
        detector = BarcodeDetector()
        print("✓ Detector initialized successfully")
        print(f"  Using device: {detector.device}")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize detector: {e}")
        return 1
    
    # Test detection
    print("Testing barcode detection...")
    try:
        detected_barcode = detector.detect_from_file(demo_path)
        print(f"✓ Detection completed")
        print()
        
        # Display results
        print("-" * 60)
        print("RESULTS:")
        print("-" * 60)
        print(f"Actual barcode:   {actual_barcode}")
        print(f"Detected barcode: {detected_barcode if detected_barcode else 'None (model needs training)'}")
        print()
        
        if detected_barcode:
            if detected_barcode == actual_barcode:
                print("✓ PERFECT MATCH!")
            else:
                print("⚠ Mismatch - model needs more training")
        else:
            print("ℹ No barcode detected")
            print("  This is expected with an untrained model.")
            print("  Run 'python train_model.py' to train the model.")
        
        print("-" * 60)
        print()
        
    except Exception as e:
        print(f"✗ Detection failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Usage instructions
    print("=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. Train the model:")
    print("   python train_model.py")
    print()
    print("2. Build Android APK:")
    print("   buildozer android debug")
    print()
    print("3. Install on Android device:")
    print("   adb install bin/pybar-1.0-arm64-v8a-debug.apk")
    print()
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
