#!/bin/bash
# Setup script for Render deployment

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

echo "Setup completed successfully!"