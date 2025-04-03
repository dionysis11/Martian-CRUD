# Martian CRUD

A fully automated CI/CD pipeline for the Mission Control CRUD System that manages space station resource stock.

## 🚀 Mission Overview

This project implements a RESTful API for managing resources on a Martian space station. The application allows for:

- Creating new resources
- Reading information about existing resources
- Updating resource details
- Deleting resources

The system is built with a Flask backend API and MongoDB database, with a simple modern UI for user interaction.

## 🛠️ Technology Stack

- Backend: Flask (Python)
- Database: MongoDB
- Frontend: HTML, CSS, JavaScript with Bootstrap 5
- CI/CD: GitHub Actions
- Containerization: Docker & Docker Compose

## 📋 Requirements

To run this project locally, you need:

- Python 3.9+
- MongoDB
- Docker and Docker Compose (optional, for containerized deployment)

## 🚦 Getting Started

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Martian-CRUD.git
   cd Martian-CRUD
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure MongoDB is running locally or update the `.env` file with your MongoDB connection string.

5. Run the application:
   ```bash
   python run.py
   ```

6. Open your browser and navigate to http://localhost:5000

### Docker Deployment

The easiest way to run the entire application stack is with Docker Compose:

1. Make sure Docker and Docker Compose are installed on your system.

2. Run the following command:
   ```bash
   docker-compose up
   ```

3. The application will be available at http://localhost:5000

## 📁 Project Structure

```
Martian-CRUD/
├── app/                      # Flask application package
│   ├── __init__.py           # Application factory
│   ├── resources/            # Resources API blueprint
│   │   ├── __init__.py
│   │   └── routes.py         # CRUD endpoints
│   ├── static/               # Static assets
│   │   └── js/
│   │       └── main.js       # Frontend JavaScript
│   └── templates/            # HTML templates
│       └── index.html        # Main UI page
├── tests/                    # Test directory
│   ├── __init__.py
│   ├── conftest.py           # Test fixtures
│   └── test_resources.py     # API tests
├── .env                      # Environment variables
├── .github/                  # GitHub configuration
│   └── workflows/            # GitHub Actions workflows
│       └── ci.yml            # CI/CD pipeline
├── .gitignore                # Git ignore rules
├── .pylintrc                 # Pylint configuration
├── config.py                 # Application configuration
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
└── run.py                    # Application entry point
```

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow that:

1. Runs on every push to main and develop branches, and on pull requests to these branches
2. Executes code quality checks with Pylint
3. Runs unit tests with pytest
4. Generates test coverage reports
5. Builds and pushes a Docker image to Docker Hub (when merged to main/develop)

## 📝 API Documentation

### Endpoints

- `GET /api/resources` - Get all resources
- `GET /api/resources/<id>` - Get a specific resource
- `POST /api/resources` - Create a new resource
- `PUT /api/resources/<id>` - Update a resource
- `DELETE /api/resources/<id>` - Delete a resource

### Sample Resource Object

```json
{
  "_id": "60f7e4d93c9447a9b89b1234",
  "name": "Oxygen",
  "quantity": 100,
  "description": "Breathing air supply"
}
```

## 🔒 Environment Variables

The application uses the following environment variables:

- `FLASK_ENV` - Flask environment (development, testing, production)
- `SECRET_KEY` - Secret key for the Flask application
- `MONGO_URI` - MongoDB connection string
- `DOCKER_HUB_USERNAME` - Docker Hub username (for CI/CD)
- `DOCKER_HUB_ACCESS_TOKEN` - Docker Hub access token (for CI/CD)

## 👩‍🚀 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request