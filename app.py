from flask import Flask, request, redirect, session, render_template, jsonify,send_file
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from Amazon_s3 import uploadImage
from database import patients, doctors, nurse
import jwt
import datetime


app = Flask(__name__)
# client = MongoClient('mongodb+srv://jw142:<password>@cluster0.dew2egn.mongodb.net/')
# db = client['COMP413']

@app.route('/login', methods=['POST'])
def login_user():
    
    username = request.json.get('username')
    password = request.json.get('password')
    print("users" + username)
    print("passss" + password)
    
    if username[0]=='P':
         curr=patients.Patient(username)
         typeL='patient'
    elif username[0]=='D':
         typeL='doctor'
         curr=doctors.Doctor(username)
    elif username[0]=='N':
         typeL='nurse'
         curr=nurse.Nurse(username) 
    user=curr.ifExist()
    if user:
         print("safasdfas"+ user['Password'])
         if password==user['Password']:
              token = jwt.encode({
            'public_id': str(user['_id']),
            'exp' : datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
        },"secret",algorithm="HS256")
              return jsonify({'token': jwt.decode(token,"secret",algorithms=["HS256"]),'type':typeL}), 200
         else:
              return jsonify({'message': 'Invalid  password'}), 401
    return jsonify({'message': 'Invalid username'}), 402



@app.route("/uploadImage", methods=["POST"])
def uploadImageS3():
        
        img = request.files['file']
        side = request.form.get("side")
        pid = request.form.get("patientID")
        date = request.form.get("date")
        print(img)
        print(side)
        print(pid)
        print(date)
        if img:
            
            succ,e=uploadImage.upload_to_s3(img)

            if succ:
                patient=patients.Patient(pid)
                if side=='front':
                    print(e+"front e")
                    patient.updatePatientFront(date,e)
                elif side=="back":
                    print(e+"back e")
                    patient.updatePatientBack(date,e)
                print(e)
                return jsonify({'success': 'Image uploaded successfully' }), 200
            else:
                return jsonify({'error': str(e)}), 500

@app.route("/getImage", methods=["POST"])
def getImageS3():
        side = request.json.get("side")
        pid = request.json.get("patientID")
        date = request.json.get("date")
        print(side)
        print(pid)
        print(date)

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
@app.route("/patientInfo", methods=["POST"])                
def getPatientInfo():
     pid = request.json.get("patientID")
     print(pid)
     if pid:
          patient=patients.Patient(pid)
          patientInfo=patient.viewPatientInfoMongo()
          if patientInfo!={}:
               return jsonify (patientInfo),200
          else:
               return jsonify ("Patient Not Found"),500
     else:
          return jsonify({'error': str("error")}), 500
     
@app.route("/doctorInfo", methods=["POST"])                
def getDoctorInfo():
     pid = request.json.get("docID")
     print(pid)
     if pid:
          doc=doctors.Doctor(pid)
          drInfo=doc.getInfo()
          
          if drInfo!={}:
               return jsonify (drInfo),200
          else:
               return jsonify ("Dcotor Not Found"),500
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
     
@app.route("/askConsent", methods=["POST"])
def askConsent():
     currDoc=request.form.get("docID")
     newDoc=request.form.get("newDoc")
     patient=request.form.get("patientID")
     Cdoc=doctors.Doctor(str(currDoc))
     nDoc=doctors.Doctor(str(newDoc))
     patient=patients.Patient(str(patient))
     CdocName=Cdoc.getInfo()["Name"]
     NdocName=nDoc.getInfo()["Name"]
     NdocHospital=nDoc.getInfo()["Hospital"]
     patientName=patient.viewPatientInfoMongo()["Name"]
     message=f"Hey {patientName}! Dr.{CdocName} wants to consult your images with Dr.{NdocName} from Hospital {NdocHospital}, Click 'Yes' to agree and consent or click 'No' otherwise "
     try:
          patient.addMsg(message)
          
     except Exception as e:
          return jsonify(str(e)),500
     return jsonify ("Consent Request Sent"),200

@app.route("/sendConsent", methods=["POST"])
def sendConsent():
     newDoc=request.form.get("newDoc")
     patientID=request.form.get("patientID")
     consent=request.form.get("Consent")
     nDoc=doctors.Doctor(str(newDoc))
     patient=patients.Patient(str(patientID))
     patientName=patient.viewPatientInfoMongo()["Name"]

     if consent=='True':
          nDoc.assignPatientNewDoc(patientID,patientName)
          return jsonify ("User Consented to Doctor"),200
     else:
          return jsonify ("User Did not consented to Doctor"),200



@app.route("/test", methods=["GET"])
def test():
     patient=request.form.get("patientID")
     patient=patients.Patient(str(patient))
     return jsonify(patient.viewPatientInfoMongo())

if __name__ == "__main__":
    app.run()