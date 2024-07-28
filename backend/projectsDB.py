from pymongo import MongoClient

# Helper function to get the projects collection
def get_projects_collection(client):
    return client.haas_db.projects

# Function to query a project by its ID
def queryProject(client, projectId):
    try:
        projects_collection = get_projects_collection(client)
        project = projects_collection.find_one({"projectId": projectId})
        if not project:
            raise Exception("Project not found.")
        return project
    except Exception as e:
        print(f"Error querying project: {e}")
        return None

# Function to create a new project
def createProject(client, projectName, projectId, description):
    try:
        projects_collection = get_projects_collection(client)
        # Ensure the projectId is unique
        if projects_collection.find_one({"projectId": projectId}):
            raise Exception("Project with this ID already exists.")
        
        project = {
            "projectName": projectName,
            "projectId": projectId,
            "description": description,
            "users": [],
            "hardwareUsage": {}
        }
        projects_collection.insert_one(project)
        return True
    except Exception as e:
        print(f"Error creating project: {e}")
        return False

# Function to add a user to a project
def addUser(client, projectId, userId):
    try:
        projects_collection = get_projects_collection(client)
        result = projects_collection.update_one(
            {"projectId": projectId},
            {"$addToSet": {"users": userId}}
        )
        if result.modified_count == 0:
            raise Exception("Failed to add user to project.")
        return True
    except Exception as e:
        print(f"Error adding user to project: {e}")
        return False

# Function to update the usage of a hardware set in a project
def updateUsage(client, projectId, hwSetName, qty):
    try:
        projects_collection = get_projects_collection(client)
        result = projects_collection.update_one(
            {"projectId": projectId},
            {"$set": {f"hardwareUsage.{hwSetName}": qty}}
        )
        if result.modified_count == 0:
            raise Exception("Failed to update hardware usage.")
        return True
    except Exception as e:
        print(f"Error updating hardware usage: {e}")
        return False

# Function to handle hardware checkout for a project
def checkOutHW(client, projectId, hwSetName, qty, userId):
    try:
        # Perform hardware checkout
        result = updateUsage(client, projectId, hwSetName, qty)
        if not result:
            raise Exception("Failed to check out hardware.")
        return True
    except Exception as e:
        print(f"Error checking out hardware: {e}")
        return False

# Function to handle hardware check-in for a project
def checkInHW(client, projectId, hwSetName, qty, userId):
    try:
        # Perform hardware check-in
        result = updateUsage(client, projectId, hwSetName, qty)
        if not result:
            raise Exception("Failed to check in hardware.")
        return True
    except Exception as e:
        print(f"Error checking in hardware: {e}")
        return False
