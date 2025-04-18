import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from pathlib import Path
import base64
import numpy as np
from PIL import Image, ImageDraw

@dataclass
class State:
    """Mock State class"""
    pass

@dataclass
class AppModel:
    """Mock AppModel class"""
    request: Any
    response: Any

class Schema:
    """Mock Schema class"""
    def __init__(self, data: Dict[str, Any]):
        self.data = data

class Resource:
    """Mock Resource class"""
    def __init__(self, value: Any = None):
        self.value = value

    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value):
        self.value = value

class Stub:
    """Mock Stub class for Openfabric SDK"""
    def __init__(self, app_ids: list):
        self.app_ids = app_ids
        logging.info(f"Initialized mock Stub with app_ids: {app_ids}")

    def execute(self, app_id: str, schema: Schema) -> bytes:
        """Mock execution that returns dummy image/model data"""
        logging.info(f"Executing mock app {app_id} with schema: {schema.data}")
        
        if "prompt" in schema.data:  # Text to Image
            # Create a 256x256 image with a gradient pattern
            img = Image.new('RGB', (256, 256))
            draw = ImageDraw.Draw(img)
            
            # Create a gradient from top to bottom
            for y in range(256):
                # Calculate gradient color based on y position
                r = int(y * 255 / 256)
                g = int((255 - y) * 255 / 256)
                b = int((y + 128) % 256)
                
                # Draw a horizontal line with the current gradient color
                draw.line([(0, y), (255, y)], fill=(r, g, b))
            
            # Add some text to make it more interesting
            draw.text((10, 10), "Mock Image", fill=(255, 255, 255))
            
            # Convert to bytes
            import io
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        
        elif "image_path" in schema.data:  # Image to 3D
            # Return a dummy GLB file content
            return b"glTF mock 3D model content"
        
        return b"" 