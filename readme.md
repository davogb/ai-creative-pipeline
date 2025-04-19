# AI Creative Pipeline

An intelligent end-to-end pipeline that transforms text descriptions into 3D models using local LLM and Openfabric.

## 📋 Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🔧 Requirements

- Python 3.9 or higher
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space
- Windows 10/11, Linux, or macOS

### Required Software
- Git
- Python 3.9+
- pip (Python package manager)

## 📥 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/davogb/ai-creative-pipeline.git
   cd ai-creative-pipeline
   ```

2. **Set Up Python Environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Required Model**
   - Download the LLaMA model from [HuggingFace](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
   - Place the downloaded file in the `models/` directory
   - Rename it to `llama-2-7b-chat.gguf`

## ⚙️ Configuration

1. **Create Environment File**
   Create a `.env` file in the root directory:
   ```env
   MAX_STORAGE_DAYS=30
   MAX_STORAGE_SIZE_MB=1000
   MAX_REQUESTS_PER_MINUTE=10
   ```

2. **Configure App IDs**
   The application uses two Openfabric apps:
   - Text to Image App ID: `f0997a01-d6d3-a5fe-53d8-561300318557`
   - Image to 3D App ID: `69543f29-4d41-4afc-7f29-3d51591f11eb`

## 🚀 Running the Application

1. **Start the Server**
   ```bash
   # Make sure you're in the project root directory
   python -m app.main
   ```

2. **Verify the Server is Running**
   - Open your browser and navigate to: `http://localhost:8888/swagger-ui/`
   - You should see the Swagger UI interface

3. **Make a Test Request**
   Using curl:
   ```bash
   curl -X POST "http://localhost:8888/execution" \
        -H "Content-Type: application/json" \
        -d '{"prompt": "dragon on mountain"}'
   ```

   Or using the Swagger UI:
   1. Navigate to `http://localhost:8888/swagger-ui/`
   2. Click on POST /execution
   3. Click "Try it out"
   4. Enter your prompt
   5. Click "Execute"

## 🧪 Testing

1. **Run All Tests**
   ```bash
   pytest tests/
   ```

2. **Run Specific Test Categories**
   ```bash
   # Run LLM tests only
   pytest tests/test_llm.py

   # Run API tests only
   pytest tests/test_api.py

   # Run mock tests only
   pytest tests/test_mock.py
   ```

## 📚 API Documentation

### Main Endpoint: POST /execution

**Request Format:**
```json
{
    "prompt": "string"
}
```

**Success Response:**
```json
{
    "status": "success",
    "original_prompt": "dragon on mountain",
    "expanded_prompt": "A majestic dragon perched...",
    "image_path": "/path/to/image.png",
    "model_path": "/path/to/model.glb"
}
```

**Error Response:**
```json
{
    "status": "error",
    "error": "Error message"
}
```

## ❗ Troubleshooting

### Common Issues

1. **LLM Not Loading**
   ```
   Error: Failed to initialize LLM
   ```
   Solution:
   - Verify model file exists in models/ directory
   - Check model filename matches configuration
   - Ensure sufficient RAM is available

2. **Storage Issues**
   ```
   Error: Failed to save generation
   ```
   Solution:
   - Check disk space
   - Verify write permissions in app/datastore
   - Run cleanup script: `python scripts/cleanup.py`

3. **Rate Limiting**
   ```
   Error: Rate limit exceeded
   ```
   Solution:
   - Wait for rate limit to reset (1 minute)
   - Adjust MAX_REQUESTS_PER_MINUTE in .env

### Getting Help

If you encounter issues:
1. Check the logs in `app/logs/`
2. Verify all requirements are met
3. Ensure configuration is correct
4. Check GitHub issues for similar problems

## 📊 System Requirements

### Minimum Requirements
- CPU: 4 cores
- RAM: 8GB
- Storage: 10GB free space
- Python: 3.9+

### Recommended Requirements
- CPU: 8 cores
- RAM: 16GB
- Storage: 20GB free space
- Python: 3.11+

## 🔒 Security Notes

1. Never share your .env file
2. Keep model files secure
3. Monitor rate limits
4. Regular security updates

## 📝 License

MIT License - See LICENSE file for details
