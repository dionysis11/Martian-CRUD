from flask import Blueprint

bp = Blueprint('resources', __name__, url_prefix='/api/resources')

# Import routes at the end to avoid circular imports
from app.resources import routes 