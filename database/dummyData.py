import pymongo
import random
from faker import Faker
from datetime import datetime, time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import secrets
uri = "mongodb+srv://jw142:gp1huwFEuma8pIlS@cluster0.dew2egn.mongodb.net"

client = MongoClient(uri, server_api=ServerApi('1'))
fake = Faker()



client = pymongo.MongoClient(uri)


db = client['COMP413']


patient_collection = db['PatientInfo']
dr_collection=db["DoctorInfo"]
nurse_collection=db["NurseInfo"]


def generate_dummy_patient_data():
    unique_id = int(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) % (10**8)
    password_length = 13
    password=secrets.token_urlsafe(password_length)
    visited_dates=sorted([fake.date_between('-1y', 'today') for _ in range(fake.random_int(min=1, max=10))])
    return {
        "PatientID": f"PA{unique_id:08d}",
        "Password":password,
        "Name": fake.name(),
        "Sex": fake.random_element(elements=("Male", "Female")),
        "Age": fake.random_int(min=18, max=70),
        "Visited": [datetime.combine(fake.date_between('-1y', 'today'), time.min) for _ in range(fake.random_int(min=1, max=10))],
        "Photos": {str(date): {"Front": f"url_to_front_image_{date}", "Back": f"url_to_back_image_{date}"} for date in visited_dates},
        "Hospital": random.choice(["Hospital1","Hospital2"])
    }

def generate_dummy_doctor_data():
    unique_id = int(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) % (10**8) 
    
    password_length = 13
    password=secrets.token_urlsafe(password_length)
 

    return {
        "DoctorID": f"DR{unique_id:08d}",
        "Password": password,
        "Name": fake.name(),
        "Patients": generate_random_patient_mapping(),
        "Hospital": random.choice(["Hospital1","Hospital2"])
    }

def generate_dummy_nurse_data():
    unique_id = int(uuid.uuid4().int & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) % (10**8) 
    
    password_length = 13
    password=secrets.token_urlsafe(password_length)


    return {
        "NurseID": f"NU{unique_id:08d}",
        "Password": password,
        "Name": fake.name(),
        "Patients": generate_random_patient_mapping(),
        "Registered": random.choice([True, False]),
        "Hospital": random.choice(["Hospital1","Hospital2"])
    }



def generate_random_patient_mapping():
    patient_mapping = {}
    
    random_patients = random.sample(list(patient_collection.find()), k=random.randint(1, 10))
    for patient in random_patients:
        patient_mapping[patient["Name"]] = patient["_id"]
    return patient_mapping
num_doctor_records = 10
num_nurse_records=30
num_patient_records = 100
num_phys_records=20


# for _ in range(num_patient_records):
#     patient_data = generate_dummy_patient_data()
#     patient_collection.insert_one(patient_data)

print("added patient data")
for _ in range(num_doctor_records):
    doctor_data = generate_dummy_doctor_data()
    dr_collection.insert_one(doctor_data)
print("added dr data")

for _ in range(num_nurse_records):
    nurse_data = generate_dummy_nurse_data()
    nurse_collection.insert_one(nurse_data)
print("added nurse data")
