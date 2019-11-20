import models
from flask import Flask, request, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict
from resources.companions import companion
from resources.locations import location
from resources.profiles import profile
from resources.users import user

DEBUG=True
PORT=8000

app = Flask(__name__)


app.secret_key = 'abjkduehdnsiau'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'testing things'

CORS(companion, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(companion, url_prefix='/api/v1/companions')

CORS(location, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(location, url_prefix='/api/v1/locations')

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/users')

CORS(profile, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(profile, url_prefix='/api/v1/profiles')


if __name__ == "__main__": 
    models.initialize()
    app.run(debug=DEBUG, port=PORT)