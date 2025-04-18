import requests
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api():
    """Test the API endpoint with a sample prompt"""
    url = "http://localhost:8888/execution"
    
    # Test prompt
    prompt = "Create a glowing dragon standing on a cliff at sunset"
    
    # Prepare request payload
    payload = {
        "request": {
            "prompt": prompt,
            "attachments": []
        }
    }
    
    try:
        # Send request
        logger.info(f"Sending request with prompt: {prompt}")
        response = requests.post(url, json=payload)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            logger.info("API Response:")
            logger.info(json.dumps(result, indent=2))
            
            # Verify memory storage
            memory_file = Path("app/datastore/memory.json")
            if memory_file.exists():
                logger.info("Memory file exists and contains:")
                with open(memory_file) as f:
                    memory_data = json.load(f)
                    logger.info(json.dumps(memory_data, indent=2))
            else:
                logger.error("Memory file not found")
                
            # Verify generated files
            storage_dir = Path("app/datastore")
            if storage_dir.exists():
                logger.info("Generated files:")
                for file in storage_dir.glob("*"):
                    logger.info(f"- {file.name}")
            else:
                logger.error("Storage directory not found")
                
        else:
            logger.error(f"API request failed with status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            
    except Exception as e:
        logger.error(f"Error during API test: {str(e)}")

if __name__ == "__main__":
    test_api() 