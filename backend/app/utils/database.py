import docker, json, os

def set_up_docker_json_file():    
    # Connect to the Docker daemon
    client = docker.from_env()
    # Get all images
    images = client.images.list()
    # Prepare the dictionary to store image:container mapping
    image_container_mapping = {}
    # Initialize dictionary with all images
    for image in images:
        image_tags = image.tags if image.tags else [image.id]
        for tag in image_tags:
            image_container_mapping[tag] = [] 
    # Get all containers
    containers = client.containers.list(all=True)
    # Map images to their containers
    for container in containers:
        image = container.attrs['Config']['Image']
        container_name = container.name
        if ':' not in image:
            image += ':latest'
        if image in image_container_mapping:
            image_container_mapping[image].append(container_name)
    # Save the dictionary to a JSON file
    with open('image_container_mapping.json', 'w') as json_file:
        json.dump(image_container_mapping, json_file, indent=4)

    print("Image-container mapping saved to image_container_mapping.json")


def is_file_empty(file_path):
    return os.path.exists(file_path) and os.path.getsize(file_path) == 0
