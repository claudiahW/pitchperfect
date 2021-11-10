from flask_simplemde import SimpleMDE 
from . import Flask 
simple = SimpleMDE()
def create_app(config_name):
    app = Flask(__name__)
    
    simple.init_app(app)