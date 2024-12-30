from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """
    Check if the uploaded file has a valid extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    """
    API endpoint to remove the background from an image.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']

    # Validate file
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Use JPG, JPEG, or PNG."}), 400

    try:
        # Process the image
        input_image = file.read()
        output_image = remove(input_image)

        # Convert output bytes to a PIL Image
        output_image = Image.open(io.BytesIO(output_image))

        # Save to a BytesIO stream
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        # Return the processed image
        return send_file(output_buffer, mimetype='image/png', as_attachment=True, download_name='output.png')
    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500


@app.route('/')
def home():
    """
    Home endpoint for testing.
    """
    return "Background Remover API is running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the dynamic Render port or default to 5000
    app.run(host="0.0.0.0", port=port)  # Bind to all interfaces (0.0.0.0)