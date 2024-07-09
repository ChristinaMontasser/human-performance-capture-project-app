from flask import Blueprint, request, jsonify, current_app
from services.model_service import run_model
from werkzeug.utils import secure_filename
import os 
import logging
#Define functionalities as blueprints using the Blueprint function
run_model_blueprint = Blueprint('run_model', __name__)
logging.basicConfig(level=logging.DEBUG)
#curl -X POST http://127.0.0.1:5000/upload \
#     -F "image=@ path/image.jpg" \
#     -F "model=model1"

#Define a route, url, for the 'upload' funcrionality so the server can determine which function should process the request.
#!! the only function that should be called by the frontend 
@run_model_blueprint.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files and 'model' not in request.form:
        logging.error("No image or model specified")
        return jsonify({"error": "No image or model specified"}), 400

    #Recieve the data from the user request
    image = request.files['image']
    model = request.form['model']
    save_to_folder = request.form['save_to_folder']
   # print(save_to_folder)
    if image.filename == '':
        logging.error("No image filename")
        return jsonify({"error": "No selected file"}), 400
    #Save the imgae 
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
        print(f'imm {model}')
        print(save_to_folder)
        result = run_model(model, save_to_folder)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    #Run the model (there, it should check thecontainer existancy) 
   # result = run_model(model)
    #return jsonify(result)

#jsonify converts a Python dictionary into a json response

'''@run_model_blueprint.route('/containers', methods=['GET'])
def list_docker_containers():
    result = list_containers()
    return jsonify(result)'''

# ##!! Only upload route is called by the frontend and the backend is responsible of all logics from whether a container exist or not
# #!! Also the front end start, upload functionalities will be merged to one function. 
# @run_model_blueprint.route('/start', methods=['POST'])
# def start_docker_container():
#     container_name = request.json.get('container_name')
#     result = start_container(container_name)
#     return jsonify(result)
