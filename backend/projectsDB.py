from pymongo import MongoClient

def get_projects_collection(client):
    return client.haas_db.projects

def queryProject(client, projectId):
    projects_collection = get_projects_collection(client)
    return projects_collection.find_one({"projectId": projectId})

def createProject(client, projectName, projectId, description):
    projects_collection = get_projects_collection(client)
    project = {
        "projectName": projectName,
        "projectId": projectId,
        "description": description,
        "users": [],
        "hardwareUsage": {}
    }
    projects_collection.insert_one(project)

def addUser(client, projectId, userId):
    projects_collection = get_projects_collection(client)
    projects_collection.update_one(
        {"projectId": projectId},
        {"$addToSet": {"users": userId}}
    )

def updateUsage(client, projectId, hwSetName, qty):
    projects_collection = get_projects_collection(client)
    projects_collection.update_one(
        {"projectId": projectId},
        {"$set": {f"hardwareUsage.{hwSetName}": qty}}
    )

def checkOutHW(client, projectId, hwSetName, qty, userId):
    updateUsage(client, projectId, hwSetName, qty)

def checkInHW(client, projectId, hwSetName, qty, userId):
    updateUsage(client, projectId, hwSetName, qty)
