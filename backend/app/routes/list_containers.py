from flask import Blueprint, jsonify
import docker

list_containers_blueprint = Blueprint('list_containers', __name__)
client = docker.from_env()

@list_containers_blueprint.route('/containers', methods=['GET'])
def list_containers():
    try:
        containers = client.containers.list(all=True)
        container_names = [container.name for container in containers]
        return jsonify(container_names)
    except docker.errors.DockerException as e:
        return jsonify({"error": str(e)}), 500
