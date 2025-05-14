from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True  # ejemplo

    # Acá deberías registrar blueprints, DB, etc.
    return app
