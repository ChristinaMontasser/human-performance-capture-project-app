from flask import Blueprint, request, jsonify, current_app
from services.model_service import run_model
from werkzeug.utils import secure_filename
import os 

#Define functionalities as blueprints using the Blueprint function
run_model_blueprint = Blueprint('run_model', __name__)

#curl -X POST http://127.0.0.1:5000/upload \
#     -F "image=@ path/image.jpg" \
#     -F "model=model1"
#Define a route, url, for the 'upload' funcrionality so the server can determine which function should process the request.
@run_model_blueprint.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'model' not in request.form:
        return jsonify({"error": "No image or model specified"}), 400

    image = request.files['image']
    model = request.form['model']
    
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    result = run_model(model, image_path)
    return jsonify(result)


#jsonify converts a Python dictionary into a json response