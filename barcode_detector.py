"""
BarcodeDetector - Neural network-based barcode detection and recognition
Uses PyTorch and torchvision for barcode number extraction
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet18
import numpy as np
from PIL import Image
import io

class BarcodeNet(nn.Module):
    """Neural network for barcode detection and digit recognition"""
    
    def __init__(self, num_digits=13):
        """
        Initialize the barcode recognition network
        
        Args:
            num_digits: Maximum number of digits in barcode (default: 13 for EAN-13)
        """
        super(BarcodeNet, self).__init__()
        
        # Use ResNet18 as backbone
        self.backbone = resnet18(pretrained=False)
        
        # Replace the final layer for digit classification
        # Output: num_digits positions x 11 classes (0-9 + no digit)
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, 512)
        
        # Digit prediction heads
        self.digit_heads = nn.ModuleList([
            nn.Linear(512, 11) for _ in range(num_digits)
        ])
        
        # Barcode presence detector
        self.presence_head = nn.Linear(512, 2)
    
    def forward(self, x):
        """
        Forward pass
        
        Args:
            x: Input image tensor
            
        Returns:
            Tuple of (presence_logits, digit_logits)
        """
        features = self.backbone(x)
        
        # Detect if barcode is present
        presence = self.presence_head(features)
        
        # Predict digits
        digits = [head(features) for head in self.digit_heads]
        
        return presence, torch.stack(digits, dim=1)

class BarcodeDetector:
    """Barcode detector using PyTorch neural network"""
    
    def __init__(self, model_path=None):
        """
        Initialize the barcode detector
        
        Args:
            model_path: Path to pre-trained model (optional)
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = BarcodeNet()
        
        if model_path:
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"Loaded model from {model_path}")
            except Exception as e:
                print(f"Could not load model from {model_path}: {e}")
                print("Using untrained model")
        
        self.model.to(self.device)
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    
    def detect_barcode(self, image_data, size):
        """
        Detect and decode barcode from image
        
        Args:
            image_data: Raw image pixel data
            size: Tuple of (width, height)
            
        Returns:
            Barcode number as string, or None if not detected
        """
        try:
            # Convert image data to PIL Image
            image = self._process_image_data(image_data, size)
            
            if image is None:
                return None
            
            # Transform image
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Run inference
            with torch.no_grad():
                presence_logits, digit_logits = self.model(image_tensor)
            
            # Check if barcode is present
            presence_probs = torch.softmax(presence_logits, dim=1)
            if presence_probs[0, 1] < 0.5:  # Not confident about barcode presence
                return None
            
            # Decode digits
            barcode_number = self._decode_digits(digit_logits)
            
            # Validate barcode
            if barcode_number and len(barcode_number) >= 8:
                return barcode_number
            
            return None
            
        except Exception as e:
            print(f"Error detecting barcode: {e}")
            return None
    
    def _process_image_data(self, image_data, size):
        """
        Process raw image data to PIL Image
        
        Args:
            image_data: Raw pixel data
            size: Tuple of (width, height)
            
        Returns:
            PIL Image or None
        """
        try:
            # Convert to numpy array
            if isinstance(image_data, bytes):
                arr = np.frombuffer(image_data, dtype=np.uint8)
            else:
                arr = np.array(image_data, dtype=np.uint8)
            
            width, height = size
            
            # Reshape based on expected format (RGBA)
            if len(arr) == width * height * 4:
                arr = arr.reshape((height, width, 4))
                # Convert RGBA to RGB
                arr = arr[:, :, :3]
            elif len(arr) == width * height * 3:
                arr = arr.reshape((height, width, 3))
            else:
                print(f"Unexpected image data size: {len(arr)} for {width}x{height}")
                return None
            
            # Create PIL Image
            image = Image.fromarray(arr, mode='RGB')
            return image
            
        except Exception as e:
            print(f"Error processing image data: {e}")
            return None
    
    def _decode_digits(self, digit_logits):
        """
        Decode digit predictions to barcode number
        
        Args:
            digit_logits: Tensor of digit predictions
            
        Returns:
            Barcode number as string
        """
        # Get predicted digits (0-9, or 10 for "no digit")
        predictions = torch.argmax(digit_logits, dim=2)[0]
        
        # Convert to string, stopping at first "no digit" (10)
        barcode = ""
        for digit in predictions:
            digit_val = digit.item()
            if digit_val == 10:  # No digit marker
                break
            barcode += str(digit_val)
        
        return barcode if barcode else None
    
    def detect_from_file(self, image_path):
        """
        Detect barcode from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Barcode number as string, or None if not detected
        """
        try:
            image = Image.open(image_path).convert('RGB')
            
            # Transform image
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Run inference
            with torch.no_grad():
                presence_logits, digit_logits = self.model(image_tensor)
            
            # Check if barcode is present
            presence_probs = torch.softmax(presence_logits, dim=1)
            if presence_probs[0, 1] < 0.5:
                return None
            
            # Decode digits
            barcode_number = self._decode_digits(digit_logits)
            
            return barcode_number
            
        except Exception as e:
            print(f"Error detecting barcode from file: {e}")
            return None
