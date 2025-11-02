# PyBar Deployment Guide

This guide provides instructions for deploying the PyBar web application to various hosting platforms.

## Quick Local Deployment

For development and testing on your local network:

```bash
# 1. Install dependencies
pip install -r requirements-server.txt

# 2. Setup model
python setup_model.py

# 3. Start server
python server.py

# 4. Access from Android device
# Find your computer's IP: ifconfig (Linux/Mac) or ipconfig (Windows)
# On Android browser: http://YOUR_IP:5000
```

## Production Deployment Options

### 1. Heroku (Free Tier Available)

**Note**: Model file (45MB) needs to be generated during deployment.

1. Create a `Procfile`:
```
web: gunicorn server:app
```

2. Update `requirements-server.txt` to include:
```
gunicorn==21.2.0
```

3. Add `runtime.txt`:
```
python-3.11.5
```

4. Create a `.slugignore` to reduce slug size:
```
*.md
test_*.py
demo.py
main.py
buildozer.spec
build_apk.*
```

5. Deploy:
```bash
# Install Heroku CLI and login
heroku login
heroku create pybar-scanner

# Set buildpack for Python
heroku buildpacks:set heroku/python

# Add post-build hook to train model
# Create a script called `train_on_deploy.py`:
# This runs after deployment to generate the model

git push heroku main
heroku open
```

**Important**: The free tier may timeout during model training. Consider:
- Pre-uploading model to cloud storage (S3, Google Drive)
- Using a paid tier with more memory/time
- Using a smaller model architecture

### 2. Google Cloud Run (Serverless)

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

# Copy application files
COPY server.py barcode_detector.py train_model.py setup_model.py ./
COPY static ./static

# Generate model on build
RUN python setup_model.py

# Expose port
ENV PORT 8080
EXPOSE 8080

# Run server
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app
```

2. Deploy:
```bash
# Install Google Cloud SDK and authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/pybar
gcloud run deploy pybar \
  --image gcr.io/YOUR_PROJECT_ID/pybar \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

### 3. AWS (EC2 or Elastic Beanstalk)

#### EC2 Manual Setup

1. Launch an Ubuntu EC2 instance (t2.medium recommended)

2. SSH into instance and setup:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/Aguelord/PyBar.git
cd PyBar

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-server.txt
pip install gunicorn

# Setup model
python setup_model.py

# Install as systemd service
sudo nano /etc/systemd/system/pybar.service
```

3. Create systemd service file:
```ini
[Unit]
Description=PyBar Barcode Scanner
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/PyBar
Environment="PATH=/home/ubuntu/PyBar/venv/bin"
ExecStart=/home/ubuntu/PyBar/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 server:app

[Install]
WantedBy=multi-user.target
```

4. Configure Nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. Start service:
```bash
sudo systemctl enable pybar
sudo systemctl start pybar
sudo systemctl restart nginx
```

### 4. Docker Deployment

1. Create `Dockerfile` (see Google Cloud Run example above)

2. Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  pybar:
    build: .
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
    restart: unless-stopped
```

3. Deploy:
```bash
docker-compose up -d
```

### 5. DigitalOcean App Platform

1. Create `app.yaml`:
```yaml
name: pybar-scanner
services:
- name: web
  github:
    repo: Aguelord/PyBar
    branch: main
  run_command: gunicorn -w 4 -b 0.0.0.0:8080 server:app
  environment_slug: python
  instance_size_slug: basic-xs
  instance_count: 1
  routes:
  - path: /
```

2. Deploy via DigitalOcean dashboard or CLI

## HTTPS Configuration

**Important**: Camera access requires HTTPS (except on localhost).

### Let's Encrypt (Free SSL)

For nginx on Ubuntu:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo systemctl reload nginx
```

### Cloudflare (Free SSL + CDN)

1. Point your domain to Cloudflare nameservers
2. Enable "Flexible SSL" or "Full SSL"
3. Point A record to your server IP
4. SSL is automatically enabled

## Performance Optimization

### Model Optimization

```python
# In barcode_detector.py, add model optimization:
model = torch.jit.script(model)  # JIT compilation
model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)  # Quantization
```

### Caching

Add caching for static files in Flask:

```python
from flask import send_from_directory
from werkzeug.middleware.shared_data import SharedDataMiddleware

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/static': 'static'
})
```

### Load Balancing

Use Nginx for load balancing multiple Gunicorn workers:

```nginx
upstream pybar {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location / {
        proxy_pass http://pybar;
    }
}
```

## Monitoring

### Basic Health Check Monitoring

```bash
# Cron job to check health
*/5 * * * * curl -f http://localhost:5000/api/health || systemctl restart pybar
```

### Application Performance Monitoring (APM)

Consider using:
- Sentry for error tracking
- New Relic for performance monitoring
- Prometheus + Grafana for metrics

## Scaling Considerations

1. **GPU Support**: Use GPU-enabled instances for faster inference
2. **Horizontal Scaling**: Run multiple instances behind a load balancer
3. **Model Serving**: Consider TensorFlow Serving or TorchServe for production
4. **Caching**: Implement Redis for result caching
5. **CDN**: Use CloudFront or Cloudflare for static assets

## Security Best Practices

1. **Rate Limiting**: Implement rate limiting on API endpoints
2. **Input Validation**: Validate image size and format
3. **CORS**: Configure CORS properly for your domain
4. **HTTPS Only**: Force HTTPS redirects
5. **Environment Variables**: Store sensitive config in environment variables

```python
# In server.py, add rate limiting:
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/detect', methods=['POST'])
@limiter.limit("10 per minute")
def detect_barcode():
    # ... existing code
```

## Cost Estimation

### Free Tiers
- **Heroku**: 550-1000 dyno hours/month (with credit card)
- **Google Cloud Run**: 2M requests/month, 180K vCPU-seconds
- **AWS Free Tier**: 750 hours EC2 t2.micro/month (1 year)
- **DigitalOcean**: $200 credit for 60 days (new accounts)

### Estimated Monthly Costs (After Free Tier)
- **Heroku Hobby**: ~$7/month
- **Google Cloud Run**: ~$5-15/month (depending on usage)
- **AWS t2.small EC2**: ~$15-20/month
- **DigitalOcean Basic Droplet**: ~$6-12/month
- **DigitalOcean App Platform**: ~$5-12/month

## Troubleshooting Deployment

### Model file too large for Git
- Use Git LFS: `git lfs track "*.pth"`
- Generate model during deployment
- Store in cloud storage and download on startup

### Out of memory during training
- Use a larger instance type
- Pre-train locally and upload model
- Reduce batch size in training

### Slow inference
- Enable GPU support
- Use model quantization
- Implement result caching
- Use smaller image sizes

### SSL/HTTPS issues
- Verify DNS is pointed correctly
- Check certificate expiration
- Ensure port 443 is open
- Test with SSL checker tools

## Support

For deployment help:
- Open an issue on GitHub
- Check deployment logs
- Review service-specific documentation
