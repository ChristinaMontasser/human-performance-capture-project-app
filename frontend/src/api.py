import requests

def upload_image_to_server(image_path, model):
    url = "http://127.0.0.1:5000/upload"
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        data = {'model': model}
        response = requests.post(url, files=files, data=data)
    return response

if __name__ == "__main__":
    response = upload_image_to_server("path/to/your/image.jpg", "model1")
    print(response.json())
