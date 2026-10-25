import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    # Load environment variables from .env if present
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Register blueprints/routes (using package-relative import for clean IDE resolution)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
