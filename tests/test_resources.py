import json

def test_get_resources(client):
    """Test getting all resources."""
    response = client.get('/api/resources')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert any(resource['name'] == 'Oxygen' for resource in data)
    assert any(resource['name'] == 'Water' for resource in data)
    assert any(resource['name'] == 'Food' for resource in data)

def test_create_resource(client):
    """Test creating a new resource."""
    response = client.post(
        '/api/resources',
        data=json.dumps({
            'name': 'Fuel',
            'quantity': 1000,
            'description': 'Rocket fuel'
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Fuel'
    assert data['quantity'] == 1000
    assert data['description'] == 'Rocket fuel'
    
    # Verify the resource was added
    response = client.get('/api/resources')
    data = json.loads(response.data)
    assert len(data) == 4
    assert any(resource['name'] == 'Fuel' for resource in data)

def test_get_resource(client):
    """Test getting a single resource."""
    # First get all resources to get an ID
    response = client.get('/api/resources')
    resources = json.loads(response.data)
    resource_id = resources[0]['_id']
    
    # Now get the specific resource
    response = client.get(f'/api/resources/{resource_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['_id'] == resource_id

def test_update_resource(client):
    """Test updating a resource."""
    # First get all resources to get an ID
    response = client.get('/api/resources')
    resources = json.loads(response.data)
    resource_id = resources[0]['_id']
    
    # Update the resource
    response = client.put(
        f'/api/resources/{resource_id}',
        data=json.dumps({
            'quantity': 200,
            'description': 'Updated description'
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['quantity'] == 200
    assert data['description'] == 'Updated description'
    
    # Verify the update persisted
    response = client.get(f'/api/resources/{resource_id}')
    data = json.loads(response.data)
    assert data['quantity'] == 200
    assert data['description'] == 'Updated description'

def test_delete_resource(client):
    """Test deleting a resource."""
    # First get all resources to get an ID
    response = client.get('/api/resources')
    resources = json.loads(response.data)
    resource_id = resources[0]['_id']
    initial_count = len(resources)
    
    # Delete the resource
    response = client.delete(f'/api/resources/{resource_id}')
    assert response.status_code == 200
    
    # Verify the resource was deleted
    response = client.get('/api/resources')
    resources = json.loads(response.data)
    assert len(resources) == initial_count - 1
    assert not any(resource['_id'] == resource_id for resource in resources) 