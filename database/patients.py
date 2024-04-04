import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import os
import certifi

#TODO add check for same Patient ID


class Patient:
    def __init__(self, pid=-1):
       uri = os.getenv('MONGO_URI')
       client = MongoClient(uri, tlsCAFile=certifi.where())

       if pid==-1:
          pid=f"PA{int(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) % (10**8)}"
       self.pid= pid
    
       self.client=client
       self.db=self.client["COMP413"]
       self.collection=self.db["PatientInfo"]


    def addNewPatientMongo(self, name, sex, age, hospital,visited=[]):
      
      
      photos={}
      for date in visited:
        photos[date]=[[],[]]
      curr_Patient={
        "PatientID": self.pid,
        "Name": name,
        "Sex": sex,
        "Age": age,
        "Visited":visited,
        "Photos":photos,
        "Hospital":hospital
        
    }
      try:
        print(curr_Patient)
        self.collection.insert_one(curr_Patient)
        print("inserted patient")
      except Exception as e:
        print(e)
    
    

    def updatePatientFront(self, new_visited_date, front_image_link):
        self.collection.update_one(
            {"PatientID": self.pid},
            {
                "$addToSet": {"Visited": new_visited_date},
                "$set": {
                    f"Photos.{str(new_visited_date)}": {
                        "Front": front_image_link,
                      
                    }
                }
            }
   )
    def updatePatientBack(self, new_visited_date, back_image_link):
        self.collection.update_one(
            {"PatientID": self.pid},
            {
                "$addToSet": {"Visited": new_visited_date},
                "$set": {
                    f"Photos.{str(new_visited_date)}": {
                        "Back": back_image_link,
                      
                    }
                }
            }
   )

    def viewPatientInfoMongo(self):
        patientData = self.collection.find_one({"PatientID": self.pid})

        patientReturn={} 
        if patientData:
            patientReturn["Pid"]=patientData["PatientID"]
            patientReturn["Name"]=patientData["Name"]
            patientReturn["Sex"]=patientData["Sex"]
            patientReturn["Age"]=patientData["Age"]
            patientReturn["Visited"]=patientData["Visited"]
            patientReturn["Hospital"]=patientData["Hospital"]
            


        else:
            print("Patient not found.")
        return patientReturn


    def viewPatientMainPicMongo(self,date):
    

      patientData = self.collection.find_one({"PatientID":self.pid})
      if len(patientData["PatientID"])==0:
          print("Patient not found")
      patientReturn=patientData["Photos"][date]

      
      return (patientReturn)
    
    def getObjID(self):
       patientData = self.collection.find_one({"PatientID":self.pid})
       return patientData['_id']
    def getMongoPatient(self):
       return self.collection.find_one({"PatientID":self.pid})
       
 
    def addMsg(self,message):
       try:
          self.collection.update_one({"PatientID": self.pid},
                                  {'$push':{'Messages':message}}
                                  
                                  )
          return ("Success")
       except Exception as e:
          return (e)
    
    def ifExist(self):
       return self.collection.find_one({"PatientID": self.pid})
       
       
       

# newPatient=Patient("PA012345678")
# # newPatient.addNewPatientMongo("Ali Khokhar","Male",20,"Hospital1")


# newPatient.updatePatientMongo("2024-02-22","linktofront","linktoback")


# print(newPatient.viewPatientInfoMongo())
# print(newPatient.viewPatientMainPicMongo("2024-02-22"))





    


    
      
    




      
      
      
      
      
      