"""API routes for resource management."""
from flask import jsonify, request
from bson.objectid import ObjectId

# Import from the parent package
from app.resources import bp
from app import mongo

# GET all resources
@bp.route('', methods=['GET'])
def get_resources():
    resources = list(mongo.db.resources.find())
    
    # Convert ObjectId to string for JSON serialization
    for resource in resources:
        resource['_id'] = str(resource['_id'])
    
    return jsonify(resources)

# GET single resource
@bp.route('/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = mongo.db.resources.find_one({'_id': ObjectId(resource_id)})
    
    if not resource:
        return jsonify({'error': 'Resource not found'}), 404
    
    # Convert ObjectId to string for JSON serialization
    resource['_id'] = str(resource['_id'])
    
    return jsonify(resource)

# CREATE new resource
@bp.route('', methods=['POST'])
def create_resource():
    data = request.json
    
    # Basic validation
    if not data or not data.get('name') or not data.get('quantity'):
        return jsonify({'error': 'Name and quantity are required'}), 400
    
    new_resource = {
        'name': data.get('name'),
        'quantity': data.get('quantity'),
        'description': data.get('description', '')
    }
    
    result = mongo.db.resources.insert_one(new_resource)
    
    # Return the created resource with the generated ID
    new_resource['_id'] = str(result.inserted_id)
    
    return jsonify(new_resource), 201

# UPDATE existing resource
@bp.route('/<resource_id>', methods=['PUT'])
def update_resource(resource_id):
    data = request.json
    
    # Basic validation
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check if resource exists
    if not mongo.db.resources.find_one({'_id': ObjectId(resource_id)}):
        return jsonify({'error': 'Resource not found'}), 404
    
    # Update only provided fields
    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'quantity' in data:
        update_data['quantity'] = data['quantity']
    if 'description' in data:
        update_data['description'] = data['description']
    
    mongo.db.resources.update_one(
        {'_id': ObjectId(resource_id)},
        {'$set': update_data}
    )
    
    # Get and return the updated resource
    updated_resource = mongo.db.resources.find_one({'_id': ObjectId(resource_id)})
    updated_resource['_id'] = str(updated_resource['_id'])
    
    return jsonify(updated_resource)

# DELETE resource
@bp.route('/<resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    # Check if resource exists
    if not mongo.db.resources.find_one({'_id': ObjectId(resource_id)}):
        return jsonify({'error': 'Resource not found'}), 404
    
    mongo.db.resources.delete_one({'_id': ObjectId(resource_id)})
    
    return jsonify({'message': 'Resource deleted successfully'}), 200 
