from flask import Flask
from routes.run_model import run_model_blueprint
from config import Config
from utils.database import set_up_docker_json_file, is_file_empty
#Creat flask appliction
app = Flask(__name__)
#Configure the app using the configurations that are defined in Config Class, specifically for data 
app.config.from_object(Config)
#We usually divide the flask application into modules, each modules is a defined as a blueprint 
#Then we register blueprints that are related to the flask app 

app.register_blueprint(run_model_blueprint)

if __name__ == '__main__':
    #Setting up the database of image and containers 
    #if(is_file_empty('database/image_container_mapping.json')):
    set_up_docker_json_file()
    app.run(debug=True)
