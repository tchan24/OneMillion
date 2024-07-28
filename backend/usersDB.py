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
        users_collection = get_users_collection(db)
        user = users_collection.find_one({"userId": userId})
        if not user:
            raise Exception("User not found.")
        return user
    except Exception as e:
        print(f"Error querying user: {e}")
        return None

# Function to authenticate a user and handle login
def login(db, username, password):
    try:
        users_collection = get_users_collection(db)
        user = users_collection.find_one({"username": username})
        if not user or not check_password_hash(user['password'], password):
            return False
        return True
    except Exception as e:
        print(f"Error logging in: {e}")
        return False

# Function to add a user to a project
def joinProject(db, userId, projectId):
    try:
        users_collection = get_users_collection(db)
        result = users_collection.update_one(
            {"userId": userId},
            {"$addToSet": {"projects": projectId}}
        )
        if result.modified_count == 0:
            raise Exception("Failed to join project.")
        return True
    except Exception as e:
        print(f"Error joining project: {e}")
        return False

# Function to retrieve the list of projects a user is part of
def getUserProjectsList(db, userId):
    try:
        user = queryUser(db, userId)
        if not user:
            raise Exception("User not found.")
        return user.get("projects", [])
    except Exception as e:
        print(f"Error retrieving user projects list: {e}")
        return []