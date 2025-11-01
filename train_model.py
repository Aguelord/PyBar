"""
Training script for barcode recognition neural network
This script trains the BarcodeNet model on synthetic or real barcode images
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import os
from barcode_detector import BarcodeNet

class SyntheticBarcodeDataset(Dataset):
    """Generate synthetic barcode images for training"""
    
    def __init__(self, num_samples=1000, image_size=(224, 224)):
        """
        Initialize synthetic barcode dataset
        
        Args:
            num_samples: Number of synthetic samples to generate
            image_size: Size of generated images
        """
        self.num_samples = num_samples
        self.image_size = image_size
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        """
        Generate a synthetic barcode image
        
        Returns:
            Tuple of (image_tensor, presence_label, digit_labels)
        """
        # Generate random barcode number (8-13 digits)
        num_digits = random.randint(8, 13)
        barcode_number = ''.join([str(random.randint(0, 9)) for _ in range(num_digits)])
        
        # Create image with barcode
        image = self._create_barcode_image(barcode_number)
        image_tensor = self.transform(image)
        
        # Create labels
        presence_label = 1  # Barcode is present
        
        # Digit labels (pad with 10 for "no digit")
        digit_labels = [int(d) for d in barcode_number]
        digit_labels += [10] * (13 - len(digit_labels))  # Pad to 13 digits
        
        return image_tensor, presence_label, torch.tensor(digit_labels, dtype=torch.long)
    
    def _create_barcode_image(self, barcode_number):
        """
        Create a simple barcode image
        
        Args:
            barcode_number: Barcode digits as string
            
        Returns:
            PIL Image with barcode
        """
        width, height = self.image_size
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw vertical bars representing the barcode
        bar_width = width // (len(barcode_number) * 2 + 2)
        x_offset = bar_width
        
        for i, digit in enumerate(barcode_number):
            # Simple encoding: digit value determines bar pattern
            digit_val = int(digit)
            
            # Draw bars based on digit value
            for j in range(4):
                if (digit_val >> j) & 1:
                    x1 = x_offset + j * bar_width // 4
                    draw.rectangle([x1, height // 4, x1 + bar_width // 4, 3 * height // 4], 
                                 fill='black')
            
            x_offset += bar_width * 2
        
        # Add number text below barcode
        try:
            # Try to use a font, fallback to default if not available
            font_size = height // 10
            draw.text((width // 2, 7 * height // 8), barcode_number, 
                     fill='black', anchor='mm')
        except Exception:
            pass
        
        # Add some noise and variations
        if random.random() > 0.5:
            # Add random rotation
            angle = random.uniform(-10, 10)
            image = image.rotate(angle, fillcolor='white')
        
        return image

def train_model(num_epochs=10, batch_size=32, learning_rate=0.001, save_path='barcode_model.pth'):
    """
    Train the barcode recognition model
    
    Args:
        num_epochs: Number of training epochs
        batch_size: Training batch size
        learning_rate: Learning rate for optimizer
        save_path: Path to save trained model
    """
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Training on device: {device}")
    
    # Create dataset and dataloader
    train_dataset = SyntheticBarcodeDataset(num_samples=5000)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    val_dataset = SyntheticBarcodeDataset(num_samples=1000)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Initialize model
    model = BarcodeNet()
    model.to(device)
    
    # Loss functions
    presence_criterion = nn.CrossEntropyLoss()
    digit_criterion = nn.CrossEntropyLoss()
    
    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    best_val_loss = float('inf')
    
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        
        for batch_idx, (images, presence_labels, digit_labels) in enumerate(train_loader):
            images = images.to(device)
            presence_labels = presence_labels.to(device)
            digit_labels = digit_labels.to(device)
            
            # Forward pass
            optimizer.zero_grad()
            presence_logits, digit_logits = model(images)
            
            # Calculate losses
            presence_loss = presence_criterion(presence_logits, presence_labels)
            
            # Digit loss (sum over all positions)
            digit_loss = 0
            for i in range(13):
                digit_loss += digit_criterion(digit_logits[:, i, :], digit_labels[:, i])
            digit_loss /= 13
            
            # Total loss
            loss = presence_loss + digit_loss
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
            if batch_idx % 20 == 0:
                print(f"Epoch [{epoch+1}/{num_epochs}], Batch [{batch_idx}/{len(train_loader)}], "
                      f"Loss: {loss.item():.4f}")
        
        # Validation
        model.eval()
        val_loss = 0.0
        correct_presence = 0
        total_presence = 0
        
        with torch.no_grad():
            for images, presence_labels, digit_labels in val_loader:
                images = images.to(device)
                presence_labels = presence_labels.to(device)
                digit_labels = digit_labels.to(device)
                
                presence_logits, digit_logits = model(images)
                
                # Presence accuracy
                presence_pred = torch.argmax(presence_logits, dim=1)
                correct_presence += (presence_pred == presence_labels).sum().item()
                total_presence += presence_labels.size(0)
                
                # Loss
                presence_loss = presence_criterion(presence_logits, presence_labels)
                digit_loss = 0
                for i in range(13):
                    digit_loss += digit_criterion(digit_logits[:, i, :], digit_labels[:, i])
                digit_loss /= 13
                
                val_loss += (presence_loss + digit_loss).item()
        
        val_loss /= len(val_loader)
        presence_acc = 100.0 * correct_presence / total_presence
        
        print(f"Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss/len(train_loader):.4f}, "
              f"Val Loss: {val_loss:.4f}, Presence Acc: {presence_acc:.2f}%")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Model saved to {save_path}")
    
    print("Training completed!")

if __name__ == '__main__':
    # Train the model
    train_model(num_epochs=20, batch_size=32, learning_rate=0.001)
