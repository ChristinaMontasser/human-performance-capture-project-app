from flask import Flask
from routes.run_model import run_model_blueprint
from config import Config

#Creat flask appliction
app = Flask(__name__)
#Configure the app using the configurations that are defined in Config Class, specifically for data 
app.config.from_object(Config)
#We usually divide the flask application into modules, each modules is a defined as a blueprint 
#Then we register blueprints that are related to the flask app 

app.register_blueprint(run_model_blueprint)

if __name__ == '__main__':
    
    app.run(debug=True)
