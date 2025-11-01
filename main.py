"""
PyBar - Android Barcode Scanner Application
Main application entry point using Kivy framework
"""

import os
# Set Kivy GL backend before importing Kivy modules
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.camera import Camera as CoreCamera
from kivy.logger import Logger
import torch
from barcode_detector import BarcodeDetector

class BarcodeScanner(BoxLayout):
    """Main widget for barcode scanning interface"""
    
    def __init__(self, **kwargs):
        super(BarcodeScanner, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Initialize barcode detector
        try:
            self.detector = BarcodeDetector()
            Logger.info("PyBar: BarcodeDetector initialized successfully")
        except Exception as e:
            Logger.error(f"PyBar: Failed to initialize BarcodeDetector: {e}")
            self.detector = None
        
        # Camera preview
        self.camera_image = Image()
        self.add_widget(self.camera_image)
        
        # Result label
        self.result_label = Label(
            text='Point camera at barcode and press Scan',
            size_hint=(1, 0.2),
            font_size='20sp'
        )
        self.add_widget(self.result_label)
        
        # Control buttons
        button_layout = BoxLayout(size_hint=(1, 0.2))
        
        self.scan_button = Button(text='Scan Barcode')
        self.scan_button.bind(on_press=self.scan_barcode)
        button_layout.add_widget(self.scan_button)
        
        self.clear_button = Button(text='Clear')
        self.clear_button.bind(on_press=self.clear_result)
        button_layout.add_widget(self.clear_button)
        
        self.add_widget(button_layout)
        
        # Initialize camera
        try:
            self.camera = CoreCamera(index=0, resolution=(640, 480))
            self.camera.play = True
            Clock.schedule_interval(self.update_camera, 1.0 / 30.0)
            Logger.info("PyBar: Camera initialized successfully")
        except Exception as e:
            Logger.error(f"PyBar: Failed to initialize camera: {e}")
            self.camera = None
            self.result_label.text = 'Camera initialization failed'
    
    def update_camera(self, dt):
        """Update camera preview"""
        if self.camera and self.camera.texture:
            self.camera_image.texture = self.camera.texture
    
    def scan_barcode(self, instance):
        """Scan barcode from current camera frame"""
        if not self.camera or not self.camera.texture:
            self.result_label.text = 'Camera not available'
            return
        
        if not self.detector:
            self.result_label.text = 'Detector not available'
            return
        
        try:
            # Get image from camera
            texture = self.camera.texture
            pixels = texture.pixels
            size = texture.size
            
            # Process with detector
            self.result_label.text = 'Processing...'
            barcode_number = self.detector.detect_barcode(pixels, size)
            
            if barcode_number:
                self.result_label.text = f'Barcode: {barcode_number}'
                Logger.info(f"PyBar: Detected barcode: {barcode_number}")
            else:
                self.result_label.text = 'No barcode detected'
                Logger.info("PyBar: No barcode detected")
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'
            Logger.error(f"PyBar: Scan error: {e}")
    
    def clear_result(self, instance):
        """Clear the result label"""
        self.result_label.text = 'Point camera at barcode and press Scan'
    
    def on_stop(self):
        """Cleanup when app stops"""
        if self.camera:
            self.camera.play = False

class PyBarApp(App):
    """Main application class"""
    
    def build(self):
        self.title = 'PyBar - Barcode Scanner'
        return BarcodeScanner()
    
    def on_stop(self):
        """Cleanup on app stop"""
        if hasattr(self.root, 'on_stop'):
            self.root.on_stop()

if __name__ == '__main__':
    PyBarApp().run()
