import logging
from pathlib import Path
from llama_cpp import Llama

class CreativeEngine:
    def __init__(self):
        """Initialize the local LLM for creative prompt expansion"""
        try:
            # Initialize Llama model
            model_path = "models/llama-2-7b-chat.gguf"  # You'll need to download this
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
            # Create a system prompt for creative expansion
            system_prompt = """You are a creative assistant that enhances image generation prompts. 
            Your task is to expand the given prompt with rich, detailed descriptions while maintaining 
            the original intent. Focus on visual elements, atmosphere, and artistic style."""

            # Format the prompt for the LLM
            formatted_prompt = f"{system_prompt}\n\nOriginal prompt: {prompt}\n\nEnhanced prompt:"

            # Generate enhanced prompt
            response = self.llm(
                formatted_prompt,
                max_tokens=200,
                temperature=0.7,
                top_p=0.9,
                stop=["Original prompt:"]
            )

            # Extract the enhanced prompt from the response
            enhanced_prompt = response['choices'][0]['text'].strip()
            
            # Clean up the response
            enhanced_prompt = enhanced_prompt.replace("Enhanced prompt:", "").strip()
            
            logging.info(f"Prompt expanded from '{prompt}' to '{enhanced_prompt}'")
            return enhanced_prompt

        except Exception as e:
            logging.error(f"Error in prompt expansion: {str(e)}")
            return prompt

def test_creative_engine():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize the creative engine
    engine = CreativeEngine()
    
    # Test prompts
    test_prompts = [
        "A glowing dragon standing on a cliff at sunset",
        "A cyberpunk city skyline at night",
        "A futuristic robot with wings"
    ]
    
    # Test each prompt
    for prompt in test_prompts:
        print(f"\nOriginal prompt: {prompt}")
        enhanced_prompt = engine.expand_prompt(prompt)
        print(f"Enhanced prompt: {enhanced_prompt}")
        print("-" * 80)

if __name__ == "__main__":
    test_creative_engine() 