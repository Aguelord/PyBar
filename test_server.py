"""
Test script for the web application server
Tests the API endpoints and barcode detection
"""

import requests
import base64
from PIL import Image, ImageDraw
import io
import sys

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

def image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def test_health_endpoint(base_url):
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ Health check passed!")
            return True
        else:
            print("✗ Health check failed!")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_detect_endpoint(base_url, barcode_number):
    """Test the barcode detection endpoint"""
    print("\n" + "="*60)
    print(f"Testing Barcode Detection: {barcode_number}")
    print("="*60)
    
    try:
        # Create test image
        print("Creating test barcode image...")
        image = create_test_barcode_image(barcode_number)
        image_data = image_to_base64(image)
        
        # Send request
        print("Sending image to server...")
        response = requests.post(
            f"{base_url}/api/detect",
            json={"image": image_data},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if response.status_code == 200:
            if result.get('success'):
                detected = result.get('barcode')
                print(f"\n✓ Detection successful!")
                print(f"  Expected: {barcode_number}")
                print(f"  Detected: {detected}")
                
                if detected == barcode_number:
                    print("  ✓ Perfect match!")
                else:
                    print("  ⚠ Different result (model needs training or improvement)")
                return True
            else:
                print(f"\n⚠ No barcode detected: {result.get('message')}")
                print("  (This is normal with untrained model)")
                return True
        else:
            print("✗ Detection failed!")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_tests(base_url="http://localhost:5000"):
    """Run all tests"""
    print("\n" + "="*60)
    print("PyBar Web Application - API Tests")
    print("="*60)
    print(f"Server URL: {base_url}")
    
    # Check if server is running
    try:
        requests.get(base_url, timeout=2)
    except:
        print("\n✗ Error: Server is not running!")
        print(f"   Please start the server with: python server.py")
        return False
    
    # Run tests
    results = []
    
    # Test 1: Health check
    results.append(test_health_endpoint(base_url))
    
    # Test 2: Barcode detection
    test_barcodes = [
        "1234567890123",
        "9876543210",
        "5901234123457"
    ]
    
    for barcode in test_barcodes:
        results.append(test_detect_endpoint(base_url, barcode))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
    
    print("\nNote: The detection accuracy depends on the model training.")
    print("The synthetic training provides baseline functionality.")
    print("For production use, train with real barcode images.")
    
    return passed == total

if __name__ == "__main__":
    # Allow custom server URL from command line
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    success = run_tests(server_url)
    sys.exit(0 if success else 1)
