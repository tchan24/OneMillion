from pymongo import MongoClient

def get_users_collection(client):
    return client.haas_db.users

def addUser(client, username, userId, password):
    users_collection = get_users_collection(client)
    user = {
        "username": username,
        "userId": userId,
        "password": password,
        "projects": []
    }
    users_collection.insert_one(user)

def __queryUser(client, username, userId):
    users_collection = get_users_collection(client)
    return users_collection.find_one({"username": username, "userId": userId})

def login(client, username, userId, password):
    user = __queryUser(client, username, userId)
    if user and user["password"] == password:
        return True
    return False

def joinProject(client, userId, projectId):
    users_collection = get_users_collection(client)
    users_collection.update_one(
        {"userId": userId},
        {"$addToSet": {"projects": projectId}}
    )

def getUserProjectsList(client, userId):
    user = __queryUser(client, None, userId)
    return user.get("projects", []) if user else []
