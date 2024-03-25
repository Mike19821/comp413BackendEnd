from flask import Flask, request, redirect, session, render_template, jsonify,send_file
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from Amazon_s3 import uploadImage
from database import patients, doctors, nurse
import jwt
import datetime


app = Flask(__name__)
client = MongoClient('mongodb+srv://jw142:<password>@cluster0.dew2egn.mongodb.net/')
db = client['COMP413']


@app.route("/uploadImage", methods=["POST"])
def uploadImageS3():
        
        
        img = request.files['file']
        side = request.form.get("side")
        pid = request.form.get("patientID")
        date = request.form.get("date")

        if img:
            
            
            succ,e=uploadImage.upload_to_s3(img)

            if succ:
                patient=patients.Patient(pid)
                if side=='front':
                    patient.updatePatientFront(date,e)
                elif side=="back":
                    patient.updatePatientBack(date,e)
                print(e)
                return jsonify({'success': 'Image uploaded successfully' }), 200
            else:
                return jsonify({'error': str(e)}), 500

@app.route("/getImage", methods=["GET"])
def getImageS3():
        side = request.form.get("side")
        pid = request.form.get("patientID")
        date = request.form.get("date")

        if side and pid and date:
             
             patient=patients.Patient(pid)
             photos=patient.viewPatientMainPicMongo(date)
             if side =="front":
                  toGet=photos["Front"]
                  resp=uploadImage.get_image_s3(toGet)
                  return send_file(resp["Body"], mimetype='image/jpeg'),200

                  

             elif side =="back":
                  toGet=photos["Back"]
                  resp=uploadImage.get_image_s3(toGet)
                  print(resp["Body"])
                  return send_file(resp["Body"], mimetype='image/jpeg'),200
        else:
             return jsonify({'error': str("error")}), 400
@app.route("/patientInfo", methods=["GET"])                
def getPatientInfo():
     pid = request.form.get("patientID") 
     if pid:
          patient=patients.Patient(pid)
          patientInfo=patient.viewPatientInfoMongo()
          if patientInfo!={}:
               return jsonify (patientInfo),200
          else:
               return jsonify ("Patient Not Found"),500
     else:
          return jsonify({'error': str("error")}), 500

@app.route("/viewmyPatients", methods=["GET"])
def getPatients():
     idn = request.form.get("ID") 
     if idn[0]=='D':
          doc=doctors.Doctor(idn)
          info=doc.getInfo()
          patients=info['Patients']
     elif idn[0]=='N':
          nu=nurse.Nurse(idn)
          info=nu.getInfo()
          if info['Registered']==False:
               return 'nurse not reg'
               
          patients=info['Patients']
     else:
          return 'id invalid'
     return patients

@app.route("/assignNurse", methods=["POST"])
def assignNurse():
     patientID=request.form.get("patientID")
     nurseID=request.form.get("nurseID")
     docID=request.form.get("docID")
     doc=doctors.Doctor(docID)
     nur=nurse.Nurse(nurseID)
     patient=patients.Patient(patientID)


     if nur.getInfo()["Hospital"]==patient.viewPatientInfoMongo()["Hospital"] and nur.getInfo()["Hospital"]==doc.getInfo()["Hospital"]:
          if doc.checkPatient(patientID):
               b=nur.addPatient(patientID)
               if b:
                    return jsonify ("Added Patient"),200
               else:
                    return jsonify ("Server Error"),500
                    
          else:
               return jsonify ("Doc doesnt have patient"),400
     else:
          return jsonify ("Different Hospitals"),401

               
               
               
               
          
          
          


     
@app.route("/outsourceDoc", methods=["GET"])
def sendConsent():
     currDoc=request.form.get("docID")
     newDoc=request.form.get("newDoc")
     patient=request.form.get("patientID")
    

@app.route('/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')
    user_collection = db['DoctorInfo']

    user = user_collection.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        token = jwt.encode({
            'public_id': str(user['_id']),
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        
        return jsonify({'token': token.decode('UTF-8')}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


if __name__ == "__main__":
    app.run()