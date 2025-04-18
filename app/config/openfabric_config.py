import os
from pathlib import Path

# Openfabric API Configuration
OPENFABRIC_API_KEY = os.getenv('OPENFABRIC_API_KEY')
OPENFABRIC_API_URL = os.getenv('OPENFABRIC_API_URL', 'https://api.openfabric.ai')

# App IDs for specific services
TEXT_TO_IMAGE_APP_ID = os.getenv('OPENFABRIC_TEXT_TO_IMAGE_APP_ID', 'f0997a01-d6d3-a5fe-53d8-561300318557')
IMAGE_TO_3D_APP_ID = os.getenv('OPENFABRIC_IMAGE_TO_3D_APP_ID', '69543f29-4d41-4afc-7f29-3d51591f11eb')

# Ensure required environment variables are set
def validate_config():
    if not OPENFABRIC_API_KEY:
        raise ValueError("OPENFABRIC_API_KEY environment variable is not set")
    
    return True 