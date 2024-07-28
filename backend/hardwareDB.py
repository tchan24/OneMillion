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
        # Find the hardware set by name
        hw_set = db.HardwareSets.find_one({"name": hwSetName})
        if not hw_set:
            raise Exception("Hardware set not found.")

        # Update the available quantity
        new_qty = hw_set["availableQty"] + qty
        if new_qty < 0 or new_qty > hw_set["totalQty"]:
            raise Exception("Invalid quantity update.")

        db.HardwareSets.update_one({"name": hwSetName}, {"$set": {"availableQty": new_qty}})
        return True
    except Exception as e:
        print(f"Error updating hardware availability: {e}")
        return False

# Function to request a certain amount of hardware from a set
def requestSpace(db, hwSetName, qty):
    try:
        # Find the hardware set by name
        hw_set = db.HardwareSets.find_one({"name": hwSetName})
        if not hw_set:
            raise Exception("Hardware set not found.")
        
        # Check if enough hardware is available
        if hw_set["availableQty"] < qty:
            raise Exception("Not enough hardware available.")
        
        # Update the available quantity
        db.HardwareSets.update_one({"name": hwSetName}, {"$inc": {"availableQty": -qty}})
        return True
    except Exception as e:
        print(f"Error requesting hardware: {e}")
        return False

# Function to retrieve a list of all hardware set names
def getAllHwNames(db):
    try:
        # Retrieve all hardware set names
        hw_names = db.HardwareSets.distinct("name")
        return hw_names
    except Exception as e:
        print(f"Error retrieving hardware names: {e}")
        return []
