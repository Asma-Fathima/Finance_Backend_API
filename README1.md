Finance Data Processing Backend

Tech Stack:
Python
Flask
SQLite

Features:
User management
Role based access
Finance record CRUD
Summary analytics API
Input validation
Database persistence

Run project:

pip install flask flask_sqlalchemy

python app.py

APIs:

POST /users
GET /users

POST /records
GET /records
PUT /records/<id>
DELETE /records/<id>

GET /summary
