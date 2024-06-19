from flask import Blueprint, jsonify, request
import docker

start_container_blueprint = Blueprint('start_container', __name__)
client = docker.from_env()

@start_container_blueprint.route('/start', methods=['POST'])
def start_container():
    try:
        container_name = request.json.get('container_name')
        container = client.containers.get(container_name)
        container.start()
        return jsonify({"message": f"Started container: {container_name}"})
    except docker.errors.NotFound:
        return jsonify({"error": f"Container '{container_name}' not found"}), 404
    except docker.errors.APIError as e:
        return jsonify({"error": f"Failed to start container '{container_name}': {str(e)}"}), 500