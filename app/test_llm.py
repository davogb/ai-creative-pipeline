import logging
from pathlib import Path
from main import CreativeEngine

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_creative_engine():
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