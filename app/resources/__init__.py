"""Resources module for the Martian Resources API."""
from flask import Blueprint

# Create the Blueprint
bp = Blueprint('resources', __name__, url_prefix='/api/resources')

def init_bp():
    """Initialize the blueprint with routes."""
    # Import routes here to avoid circular imports while still registering them with bp
    # pylint: disable=import-outside-toplevel,cyclic-import
    from . import routes  # noqa
    # pylint: enable=import-outside-toplevel,cyclic-import
    return bp

# Initialize routes
init_bp()
