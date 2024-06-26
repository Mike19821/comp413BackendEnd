from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from patients import Patient
import uuid
import os
import certifi

class Doctor:
    def __init__(self, did=-1):
       uri = os.getenv('MONGO_URI')
       client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))

       if did==-1:
          did=f"DR{int(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) % (10**8)}"
       self.did= did
    
       self.client=client
       self.db=self.client["COMP413"]
       self.collection=self.db["DoctorInfo"]
    
    def getInfo(self):
       doctorInfo=self.collection.find_one({"DoctorID":self.did})
       drReturn={} 
       if doctorInfo:
         drReturn["Pid"]=doctorInfo["DoctorID"]
         drReturn["Name"]=doctorInfo["Name"]
         drReturn["Sex"]=doctorInfo["Sex"]
         drReturn["Age"]=doctorInfo["Age"]
         drReturn["Patients"]=doctorInfo["Hospital"]
         drReturn["Hospital"]=doctorInfo["Hospital"]
            


       else:
            print("Patient not found.")
       return drReturn
       
       return doctorInfo
    
    def checkPatient(self,PatientID):
       doctorInfo=self.collection.find_one({"DoctorID":self.did})
       patients=doctorInfo["Patients"]
       if PatientID in patients.keys():
          return True
       else:
          return False
       
    def assignPatientNewDoc(self, PatientID, PatientName):
       patientMapping={PatientID:PatientName}
       doctorInfo=self.collection.find_one({"DoctorID":self.did})

    def ifExist(self):
       return self.collection.find_one({"DoctorID": self.did})
       
       
       
       
       
       
   
       
       
       
       
       
       


