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
