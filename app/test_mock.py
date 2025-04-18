import logging
from pathlib import Path
from main import execute, AppModel, InputClass, OutputClass

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_pipeline():
    """Test the entire pipeline with mock implementation"""
    
    # Create test directories
    Path("app/datastore").mkdir(parents=True, exist_ok=True)
    
    # Create test input
    class TestInput:
        prompt = "A glowing dragon standing on a cliff at sunset"
    
    class TestOutput:
        message = None
    
    # Create test model
    model = AppModel(
        request=TestInput(),
        response=TestOutput()
    )
    
    # Execute pipeline
    execute(model)
    
    # Print results
    print("\nTest Results:")
    print("-" * 80)
    print(f"Response: {model.response.message}")
    
    # Verify files were created
    datastore = Path("app/datastore")
    print("\nGenerated Files:")
    print("-" * 80)
    for file in datastore.glob("*"):
        print(f"- {file.name}")

if __name__ == "__main__":
    test_pipeline() 