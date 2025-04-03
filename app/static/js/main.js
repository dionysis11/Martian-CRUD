// API URL - adjust for local or production
const API_BASE_URL = '/api/resources';

// DOM elements
const resourceList = document.getElementById('resource-list');
const resourceForm = document.getElementById('resource-form');
const nameInput = document.getElementById('name');
const quantityInput = document.getElementById('quantity');
const descriptionInput = document.getElementById('description');
const submitBtn = document.getElementById('submit-btn');
const formTitle = document.getElementById('form-title');

let isEditing = false;
let editingId = null;

// Fetch and display all resources
async function fetchResources() {
    try {
        const response = await fetch(API_BASE_URL);
        const resources = await response.json();
        
        displayResources(resources);
    } catch (error) {
        console.error('Error fetching resources:', error);
        showMessage('Failed to load resources', 'error');
    }
}

// Display resources in the table
function displayResources(resources) {
    resourceList.innerHTML = '';
    
    if (resources.length === 0) {
        resourceList.innerHTML = '<tr><td colspan="5" class="text-center">No resources found</td></tr>';
        return;
    }
    
    resources.forEach(resource => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${resource.name}</td>
            <td>${resource.quantity}</td>
            <td>${resource.description || '-'}</td>
            <td>
                <button class="btn btn-sm btn-primary edit-btn" data-id="${resource._id}">Edit</button>
                <button class="btn btn-sm btn-danger delete-btn" data-id="${resource._id}">Delete</button>
            </td>
        `;
        
        resourceList.appendChild(row);
    });
    
    // Add event listeners to buttons
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', handleEdit);
    });
    
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', handleDelete);
    });
}

// Handle form submission (create or update)
async function handleSubmit(event) {
    event.preventDefault();
    
    // Validate form
    if (!nameInput.value || !quantityInput.value) {
        showMessage('Name and quantity are required', 'error');
        return;
    }
    
    const resourceData = {
        name: nameInput.value,
        quantity: parseInt(quantityInput.value),
        description: descriptionInput.value
    };
    
    try {
        let response;
        
        if (isEditing) {
            // Update existing resource
            response = await fetch(`${API_BASE_URL}/${editingId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(resourceData)
            });
            
            if (response.ok) {
                showMessage('Resource updated successfully!', 'success');
            }
        } else {
            // Create new resource
            response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(resourceData)
            });
            
            if (response.ok) {
                showMessage('Resource created successfully!', 'success');
            }
        }
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to save resource');
        }
        
        // Reset form and refresh resources
        resetForm();
        fetchResources();
    } catch (error) {
        console.error('Error saving resource:', error);
        showMessage(error.message, 'error');
    }
}

// Handle edit button click
async function handleEdit(event) {
    const resourceId = event.target.dataset.id;
    
    try {
        const response = await fetch(`${API_BASE_URL}/${resourceId}`);
        const resource = await response.json();
        
        // Populate form with resource data
        nameInput.value = resource.name;
        quantityInput.value = resource.quantity;
        descriptionInput.value = resource.description || '';
        
        // Set form to edit mode
        isEditing = true;
        editingId = resourceId;
        formTitle.textContent = 'Edit Resource';
        submitBtn.textContent = 'Update Resource';
        
        // Scroll to form
        resourceForm.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error fetching resource details:', error);
        showMessage('Failed to load resource details', 'error');
    }
}

// Handle delete button click
async function handleDelete(event) {
    const resourceId = event.target.dataset.id;
    
    if (!confirm('Are you sure you want to delete this resource?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/${resourceId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Resource deleted successfully!', 'success');
            fetchResources();
        } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to delete resource');
        }
    } catch (error) {
        console.error('Error deleting resource:', error);
        showMessage(error.message, 'error');
    }
}

// Reset form to create mode
function resetForm() {
    resourceForm.reset();
    isEditing = false;
    editingId = null;
    formTitle.textContent = 'Add New Resource';
    submitBtn.textContent = 'Add Resource';
}

// Show message to user
function showMessage(message, type = 'info') {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show mt-3`;
    alertBox.role = 'alert';
    
    alertBox.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.querySelector('.container').insertBefore(alertBox, document.querySelector('.row'));
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertBox.remove();
    }, 5000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    fetchResources();
    resourceForm.addEventListener('submit', handleSubmit);
    document.getElementById('reset-btn').addEventListener('click', resetForm);
}); 