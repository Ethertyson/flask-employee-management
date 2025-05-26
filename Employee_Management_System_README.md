
# Employee Management System - Flask REST API

## Overview
A modular Flask-based REST API for managing employees, featuring JWT authentication, Redis token revocation, and CRUD operations using both SQLAlchemy ORM and raw SQL. The app is containerized with Docker and deployed on Render.

## Features
- Modular Flask app with Blueprints and factory pattern
- CRUD operations with SQLAlchemy ORM & raw SQL
- JWT-based authentication and secure logout using Redis
- Input validation & serialization with Marshmallow
- Role-Based Access Control (RBAC)
- Dockerized app for consistent development & deployment
- Deployment ready for cloud platforms like Render, AWS, Azure

## Setup & Run Locally
1. Clone the repo:  
   ```bash
   git clone https://github.com/Ethertyson/flask-employee-management.git
   cd flask-employee-management
   ```

2. Create and activate a virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/macOS
   venv\Scripts\activate          # Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Setup environment variables (.env file):  
   Create a `.env` file in the root directory with the following variables:
   - FLASK_ENV=development
   - SECRET_KEY=your_secret_key
   - DATABASE_URL=your_database_url
   - REDIS_HOST=localhost
   - REDIS_PORT=6379
   - REDIS_DB=0
   - JWT_SECRET_KEY=your_jwt_secret_key

5. Run the app locally:  
   ```bash
   flask run	# OR python run.py
   ```

## Docker
Build and run the Docker image:  
```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app
```

## Deployment
Deployed on Render: https://flask-employee-management.onrender.com/

## Deploy at your end
- Push your code to GitHub
- Connect your repo to Render (or any other cloud platform)
- Add required environment variables in Render settings
- Deploy and access your live URL

## API Documentation
- **Auth:** `/registerUser`, `/loginUser`, `/loginUserV2`, `/logoutUser`, `/logoutUserV2`  
- **Employees:** `/fetchEmployeewithFlask`, `/insertEmployeewithFlask`, `/updateEmployeewithFlask`, `/deleteEmployeewithFlask`, `fetchEmployeewithFlaskUsingPagination`, `fetchEmpthroughPagValidFilter`, `/fetchEmpSerialized` (CRUD operations)
- Protected routes require JWT token in `Authorization` header as:  
  `Authorization: Bearer <your-token>`

## Technologies Used
- Python, Flask, Flask-JWT-Extended, Flask-Bcrypt,JWTManager, wraps, get_jwt_identity, create_access_token, Blueprint 
- SQLAlchemy ORM, Marshmallow  
- Docker, Render cloud platform  
- Redis for token revocation  

## Project Structure
- app -- models
      -- routes
      -- schemas
      -- utils
      -- __init__.py
      -- extensions.py
- venv
- .env
- config.py
- Dockerfile
- requirements.txt
- run.py

## Usage
- Access root: / → returns hello message
- Use Postman or curl to test JWT-protected endpoints with Authorization header

## Author
Pritanshu Srivastava 
[linkedin](https://www.linkedin.com/in/pritanshu-srivastava-59aaa7226/)
[GitHub](https://github.com/Ethertyson)
