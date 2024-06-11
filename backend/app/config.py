import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data', 'uploads')
    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'data', 'outputs')

config = Config()
