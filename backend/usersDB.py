from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Helper function to get the users collection
def get_users_collection(client):
    return client.haas_db.users

# Function to add a new user to the database
def addUser(db, username, userId, password):
    try:
        users_collection = get_users_collection(db)
        # Ensure the userId is unique
        if users_collection.find_one({"userId": userId}):
            raise Exception("User with this ID already exists.")
        
        # Hash the password before storing
        hashed_password = generate_password_hash(password)
        
        user = {
            "username": username,
            "userId": userId,
            "password": hashed_password,
            "projects": []
        }
        users_collection.insert_one(user)
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

# Helper function to query a user by username and userId
def queryUser(db, userId):
    try:
        users_co