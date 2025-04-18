import logging
from typing import Dict, Optional
import os 
from pathlib import Path
import json
from datetime import datetime
from llama_cpp import Llama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import mock components instead of SDK
from mock_openfabric import AppModel, State, Stub, Schema, Resource

from ontology_dc8f06af066e4a7880a5938933236037.config import ConfigClass
from ontology_dc8f06af066e4a7880a5938933236037.input import InputClass
from ontology_dc8f06af066e4a7880a5938933236037.output import OutputClass

# Import configuration
from config.openfabric_config import (
    TEXT_TO_IMAGE_APP_ID,
    IMAGE_TO_3D_APP_ID,
    validate_config
)

# Directory for storing generated content and memory
STORAGE_DIR = Path("app/datastore")
MEMORY_FILE = STORAGE_DIR / "memory.json"

# Ensure storage directory exists
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Validate Openfabric configuration
validate_config()

# Configurations for the app
configurations: Dict[str, ConfigClass] = dict()

class MemoryManager:
    def __init__(self, memory_file: Path):
        self.memory_file = memory_file
        self._ensure_memory_file()
    
    def _ensure_memory_file(self):
        if not self.memory_file.exists():
            self.memory_file.write_text('{"generations": []}')
    
    def save_generation(self, prompt: str, image_path: str, model_path: str) -> None:
        """Save a generation to memory"""
        data = self._read_memory()
        data["generations"].append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "image_path": str(image_path),
            "model_path": str(model_path)
        })
        self._write_memory(data)
    
    def _read_memory(self) -> dict:
        return json.loads(self.memory_file.read_text())
    
    def _write_memory(self, data: dict) -> None:
        self.memory_file.write_text(json.dumps(data, indent=2))
    
    def find_similar_generations(self, prompt: str) -> list:
        """Find similar previous generations"""
        data = self._read_memory()
        similar_generations = []
        for generation in data["generations"]:
            if prompt in generation["prompt"]:
                similar_generations.append(generation)
        return similar_generations

class CreativeEngine:
    def __init__(self):
        """Initialize the local LLM for creative prompt expansion"""
        try:
            # Initialize Llama model
            model_path = "models/llama-2-7b-chat.gguf"
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=4
            )
            logging.info("LLM initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize LLM: {str(e)}")
            self.llm = None

    def expand_prompt(self, prompt: str) -> str:
        """Expand user prompt using local LLM with creative enhancement"""
        if not self.llm:
            logging.warning("LLM not initialized, returning original prompt")
            return prompt

        try:
            system_prompt = """You are a creative assistant that enhances image generation prompts. 
            Your task is to expand the given prompt with rich, detailed descriptions while maintaining 
            the original intent. Focus on visual elements, atmosphere, and artistic style."""

            formatted_prompt = f"{system_prompt}\n\nOriginal prompt: {prompt}\n\nEnhanced prompt:"
            response = self.llm(
                formatted_prompt,
                max_tokens=200,
                temperature=0.7,
                top_p=0.9,
                stop=["Original prompt:"]
            )
            enhanced_prompt = response['choices'][0]['text'].strip()
            enhanced_prompt = enhanced_prompt.replace("Enhanced prompt:", "").strip()
            logging.info(f"Prompt expanded from '{prompt}' to '{enhanced_prompt}'")
            return enhanced_prompt

        except Exception as e:
            logging.error(f"Error in prompt expansion: {str(e)}")
            return prompt

def execute(model: AppModel) -> None:
    """
    Main execution entry point for handling a model pass.
    """
    try:
        # Initialize components
        memory_manager = MemoryManager(MEMORY_FILE)
        creative_engine = CreativeEngine()

        # Get input prompt
        request: InputClass = model.request
        prompt = request.prompt

        # Get user config and initialize stub
        user_config: ConfigClass = configurations.get('super-user', None)
        app_ids = [TEXT_TO_IMAGE_APP_ID, IMAGE_TO_3D_APP_ID]
        stub = Stub(app_ids)

        # 1. Expand prompt using local LLM
        expanded_prompt = creative_engine.expand_prompt(prompt)
        logging.info(f"Expanded prompt: {expanded_prompt}")

        # 2. Generate image from text using Openfabric
        image_schema = Schema({
            "prompt": expanded_prompt,
            "num_inference_steps": 50,
            "guidance_scale": 7.5
        })
        
        image_result = stub.execute(
            app_id=TEXT_TO_IMAGE_APP_ID,
            schema=image_schema
        )

        if not image_result:
            raise Exception("Failed to generate image")
        
        # Save generated image
        image_path = STORAGE_DIR / f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        with open(image_path, 'wb') as f:
            f.write(image_result)

        # 3. Convert image to 3D model using Openfabric
        model_schema = Schema({
            "image_path": str(image_path),
            "num_steps": 1000,
            "resolution": 512
        })
        
        model_result = stub.execute(
            app_id=IMAGE_TO_3D_APP_ID,
            schema=model_schema
        )

        if not model_result:
            raise Exception("Failed to generate 3D model")
        
        # Save 3D model
        model_path = STORAGE_DIR / f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.glb"
        with open(model_path, 'wb') as f:
            f.write(model_result)

        # 4. Store in memory
        memory_manager.save_generation(prompt, image_path, model_path)

        # 5. Prepare response
        response: OutputClass = model.response
        response.message = {
            "status": "success",
            "original_prompt": prompt,
            "expanded_prompt": expanded_prompt,
            "image_path": str(image_path),
            "model_path": str(model_path)
        }

    except Exception as e:
        logging.error(f"Error in execution: {str(e)}")
        response: OutputClass = model.response
        response.message = {
            "status": "error",
            "error": str(e)
        }

def config(configuration: Dict[str, ConfigClass], state: State) -> None:
    """
    Stores user-specific configuration data.
    """
    for uid, conf in configuration.items():
        logging.info(f"Saving new config for user with id:'{uid}'")
        configurations[uid] = conf