from flask import Flask, request, jsonify
import logging
from main import execute, AppModel, InputClass, OutputClass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/execution', methods=['POST'])
def handle_execution():
    try:
        # Get request data
        data = request.json
        logger.info(f"Received request: {data}")
        
        # Create input class
        input_data = InputClass()
        input_data.prompt = data['request']['prompt']
        input_data.attachments = data['request'].get('attachments', [])
        
        # Create output class
        output_data = OutputClass()
        
        # Create app model
        model = AppModel(request=input_data, response=output_data)
        
        # Execute
        execute(model)
        
        # Return response
        return jsonify({
            "status": "success",
            "response": model.response.message
        })
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True) 