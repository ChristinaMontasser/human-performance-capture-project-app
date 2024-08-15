from flask import Blueprint, request, jsonify, current_app
from services.model_service import run_model
from werkzeug.utils import secure_filename
import os 
import logging
#from ..utils.helpers import map_model_name
#Define functionalities as blueprints using the Blueprint function
run_model_blueprint = Blueprint('run_model', __name__)
logging.basicConfig(level=logging.DEBUG)

#Define a route, url, for the 'upload' funcrionality so the server can determine which function should process the request.
#The only function that should be called by the frontend 
@run_model_blueprint.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files and 'model' not in request.form:
        logging.error("No image or model specified")
        return jsonify({"error": "No image or model specified"}), 400

    #Recieve the data from the user request
    image = request.files['image']
    filename = secure_filename(image.filename)
    file_extension = os.path.splitext(filename)[1]  #image_or_video
    output_types = request.form['output_types'] 
    model = request.form['model']
    model = model.lower()
    model = f'{model}:latest'
    save_to_folder = request.form['save_to_folder']
    if image.filename == '':
        logging.error("No image filename")
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(image.filename)
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    try:
        image.save(image_path)
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to save image"}), 500

    if not os.path.exists(image_path):
        return jsonify({"error": "Image not saved"}), 500

    try:
        result = run_model(model, save_to_folder, file_extension, output_types)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

