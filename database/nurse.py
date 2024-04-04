from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import os
from database import patients

class Nurse:
    def __init__(self, did=-1):
       uri = os.getenv('MONGO_URI')
       client = MongoClient(uri, server_api=ServerApi('1'))

       if did==-1:
          did=f"NU{int(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) % (10**8)}"
       self.did= did
    
       self.client=client
       self.db=self.client["COMP413"]
       self.collection=self.db["NurseInfo"]
    
    def getInfo(self):
       NInfo=self.collection.find_one({"NurseID":self.did})
       print(NInfo)
       
       
       return NInfo
    
    def addPatient(self, patientID):
       nMongo=self.collection.find_one({"NurseID":self.did})
       currP=nMongo.get("Patients",{})
       patient=patients.Patient(patientID)
       currP[patientID]=patient.getMongoPatient()['Name']
       
       
       return self.collection.update_one(
        {"NurseID": self.did},
        {"$set": {"Patients": currP}}
    )
        
      
    def ifExist(self):
       return self.collection.find_one({"NurseID": self.did})
   
       