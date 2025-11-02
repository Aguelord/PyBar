// PyBar Web Application
// Handles camera access, image capture, and server communication

// Configuration - Change this to your server URL
const API_BASE_URL = window.location.origin;

// DOM Elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const cameraContainer = document.getElementById('camera-container');
const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview-image');
const resultDiv = document.getElementById('result');
const resultText = document.getElementById('result-text');
const captureBtn = document.getElementById('capture-btn');
const scanBtn = document.getElementById('scan-btn');
const retryBtn = document.getElementById('retry-btn');
const loading = document.getElementById('loading');

let stream = null;
let capturedImageData = null;

// Initialize the application
async function init() {
    try {
        // Request camera access with back camera preference (for mobile)
        const constraints = {
            video: {
                facingMode: { ideal: 'environment' }, // Use back camera on mobile
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        };
        
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        
        console.log('Camera initialized successfully');
    } catch (error) {
        console.error('Error accessing camera:', error);
        showError('Impossible d\'accéder à la caméra. Veuillez vérifier les permissions.');
    }
}

// Capture image from video stream
function captureImage() {
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw current video frame to canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Get image data as base64
    capturedImageData = canvas.toDataURL('image/jpeg', 0.9);
    
    // Show preview
    previewImage.src = capturedImageData;
    cameraContainer.style.display = 'none';
    previewContainer.style.display = 'block';
    
    // Update buttons
    captureBtn.style.display = 'none';
    scanBtn.style.display = 'inline-block';
    retryBtn.style.display = 'inline-block';
    
    // Update result text
    showMessage('Image capturée ! Appuyez sur Analyser pour détecter le code-barres.');
}

// Send image to server for barcode detection
async function scanBarcode() {
    if (!capturedImageData) {
        showError('Aucune image capturée');
        return;
    }
    
    // Show loading indicator
    showLoading(true);
    scanBtn.disabled = true;
    retryBtn.disabled = true;
    
    try {
        // Send image to server
        const response = await fetch(`${API_BASE_URL}/api/detect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: capturedImageData
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showSuccess(`Code-barres détecté: ${data.barcode}`);
        } else if (response.ok && !data.success) {
            showWarning(data.message || 'Aucun code-barres détecté');
        } else {
            showError(data.error || 'Erreur lors de l\'analyse');
        }
    } catch (error) {
        console.error('Error scanning barcode:', error);
        showError('Erreur de connexion au serveur');
    } finally {
        showLoading(false);
        scanBtn.disabled = false;
        retryBtn.disabled = false;
    }
}

// Reset to camera view
function retry() {
    // Show camera again
    cameraContainer.style.display = 'block';
    previewContainer.style.display = 'none';
    
    // Update buttons
    captureBtn.style.display = 'inline-block';
    scanBtn.style.display = 'none';
    retryBtn.style.display = 'none';
    
    // Clear captured data
    capturedImageData = null;
    
    // Reset result
    showMessage('Pointez la caméra vers un code-barres');
}

// UI Helper Functions
function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
}

function showMessage(message) {
    resultDiv.className = 'result';
    resultText.textContent = message;
}

function showSuccess(message) {
    resultDiv.className = 'result success';
    resultText.textContent = message;
}

function showWarning(message) {
    resultDiv.className = 'result';
    resultText.textContent = message;
}

function showError(message) {
    resultDiv.className = 'result error';
    resultText.textContent = message;
}

// Event Listeners
captureBtn.addEventListener('click', captureImage);
scanBtn.addEventListener('click', scanBarcode);
retryBtn.addEventListener('click', retry);

// Check server health on load
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('Server health:', data);
        
        if (!data.model_loaded) {
            console.warn('Warning: Model not loaded on server');
        }
    } catch (error) {
        console.error('Server health check failed:', error);
    }
}

// Initialize app on page load
window.addEventListener('load', () => {
    init();
    checkServerHealth();
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
