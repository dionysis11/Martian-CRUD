import pytest
from app import create_app, mongo

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app({
        'TESTING': True,
        'MONGO_URI': 'mongodb://localhost:27017/test_martian_resources'
    })
    
    # Create a test client using the Flask application
    with app.app_context():
        # Clear the database before each test
        mongo.db.resources.delete_many({})
        
        # Insert test data
        mongo.db.resources.insert_many([
            {'name': 'Oxygen', 'quantity': 100, 'description': 'Breathing air supply'},
            {'name': 'Water', 'quantity': 500, 'description': 'Drinking water'},
            {'name': 'Food', 'quantity': 300, 'description': 'Meal rations'}
        ])
    
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client() 