from pymongo import MongoClient

def get_hardware_collection(client):
    return client.haas_db.hardware

def createHardwareSet(client, hwSetName, totalQty):
    hardware_collection = get_hardware_collection(client)
    hardware_set = {
        "hwSetName": hwSetName,
        "totalQty": totalQty,
        "availableQty": totalQty
    }
    hardware_collection.insert_one(hardware_set)

def queryHardwareSet(client, hwSetName):
    hardware_collection = get_hardware_collection(client)
    return hardware_collection.find_one({"hwSetName": hwSetName})

def updateAvailability(client, hwSetName, qty):
    hardware_collection = get_hardware_collection(client)
    hardware_collection.update_one(
        {"hwSetName": hwSetName},
        {"$set": {"availableQty": qty}}
    )

def requestSpace(client, hwSetName, qty):
    hardware_set = queryHardwareSet(client, hwSetName)
    if hardware_set and hardware_set["availableQty"] >= qty:
        updateAvailability(client, hwSetName, hardware_set["availableQty"] - qty)
        return True
    return False

def getAllHwNames(client):
    hardware_collection = get_hardware_collection(client)
    return [hw["hwSetName"] for hw in hardware_collection.find()]
