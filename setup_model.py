#!/usr/bin/env python3
"""
Script to train and generate the pre-trained barcode detection model
This should be run before starting the server if barcode_model.pth doesn't exist
"""

import os
import sys
from train_model import train_model

MODEL_PATH = 'barcode_model.pth'

def main():
    """Main function to setup the model"""
    if os.path.exists(MODEL_PATH):
        print(f"✓ Pre-trained model already exists: {MODEL_PATH}")
        size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
        print(f"  Size: {size_mb:.1f} MB")
        
        response = input("\nDo you want to retrain the model? (y/N): ")
        if response.lower() != 'y':
            print("Using existing model.")
            return 0
    
    print("\n" + "="*60)
    print("Training Barcode Detection Model")
    print("="*60)
    print("\nThis will train a PyTorch neural network on synthetic barcode data.")
    print("Training may take several minutes depending on your hardware.")
    print("\nNote: For production use, train on real barcode images for better accuracy.\n")
    
    try:
        # Train the model with appropriate settings
        print("Starting training...")
        train_model(
            num_epochs=20,
            batch_size=32,
            learning_rate=0.001,
            save_path=MODEL_PATH
        )
        
        print("\n" + "="*60)
        print("✓ Model training completed successfully!")
        print("="*60)
        print(f"\nModel saved to: {MODEL_PATH}")
        
        if os.path.exists(MODEL_PATH):
            size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
            print(f"Model size: {size_mb:.1f} MB")
        
        print("\nYou can now start the server with: python server.py")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
