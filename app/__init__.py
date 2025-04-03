"""Main application package."""
import os
from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from config import config

# Initialize extensions that will be bound to the app later
mongo = PyMongo()

def create_app(test_config=None, environ=None):
    """Factory function for creating the Flask application."""
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load environment variables from a .env file if present
    load_dotenv()
    
    # Load configuration
    if test_config is None:
        # Load the config based on environment
        env = environ or os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config[env])
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Setup CORS
    CORS(app)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Create index route to serve the frontend
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # API root info route
    @app.route('/api')
    def api_info():
        return {"message": "Welcome to Martian Resources API!"}
    
    # Register blueprints - this import must be inside the function to avoid circular imports
    # but pylint will complain about import-outside-toplevel, so disabling that check locally
    # pylint: disable=import-outside-toplevel
    from app.resources import bp as resources_bp
    app.register_blueprint(resources_bp)
    # pylint: enable=import-outside-toplevel
    
    return app


# Create a global Flask application object
app = create_app()
