from flask import Flask, request, redirect, session, render_template, jsonify,send_file
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from Amazon_s3 import uploadImage
from database import patients, doctors, nurse
import os


app = Flask(__name__)


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

    

          
          
     

if __name__ == "__main__":
    app.run()