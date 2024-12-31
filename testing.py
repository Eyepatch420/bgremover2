from flask import Flask, request, jsonify, send_file
from rembg import remove
from io import BytesIO
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    
    try:
        # Load the image with Pillow
        input_image = Image.open(image_file)

        # Convert to a standard mode (e.g., RGBA) if needed
        if input_image.mode not in ("RGB", "RGBA"):
            input_image = input_image.convert("RGBA")

        # Convert image to bytes and remove the background
        input_image_bytes = BytesIO()
        input_image.save(input_image_bytes, format="PNG")  # Save as PNG for processing
        input_image_bytes.seek(0)
        output_image_bytes = remove(input_image_bytes.read())

        # Convert output bytes back to an image
        output_image = Image.open(BytesIO(output_image_bytes))

        # Save the processed image in memory
        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")  # Output as PNG to support transparency
        output_buffer.seek(0)

        # Return the image as a response
        return send_file(output_buffer, mimetype='image/png', as_attachment=True, download_name='output.png')

    except UnidentifiedImageError:
        return jsonify({'error': 'Unsupported image format or corrupted file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
