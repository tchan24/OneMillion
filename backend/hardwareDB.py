from pymongo import MongoClient

# Function to create a new hardware set
def createHardwareSet(db, hwSetName, totalQty):
    try:
        # Ensure the hardware set name is unique
        if db.HardwareSets.find_one({"name": hwSetName}):
            raise Exception("Hardware set with this name already exists.")
        
        # Insert the new hardware set into the database
        hw_set = {
            "name": hwSetName,
            "totalQty": totalQty,
            "availableQty": totalQty
        }
        db.HardwareSets.insert_one(hw_set)
        return True
    except Exception as e:
        print(f"Error creating hardware set: {e}")
        return False

# Function to query a hardware set by its name
def queryHardwareSet(db, hwSetName):
    try:
        # Find the hardware set by name
        hw_set = db.HardwareSets.find_one({"name": hwSetName}, {"_id": 0})
        if not hw_set:
            raise Exception("Hardware set not found.")
        return hw_set
    except Exception as e:
        print(f"Error querying hardware set: {e}")
        return None

# Function to update the availability of a hardware set
def updateAvailability(db, hwSetName, qty):
    try:
        # Find the 