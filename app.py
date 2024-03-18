from flask import Flask, request, redirect, session, render_template, jsonify,send_file
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from Amazon_s3 import uploadImage
from database import patients
import os


app = Flask(__name__)



# Register
# @app.route("/register", methods=["POST"])
# def register():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
#     confirmation = data.get("confirmation")

#     if not email or not password or not confirmation:
#         return jsonify({"error": "Please fill out all fields"}), 400

#     if password != confirmation:
#         return jsonify({"error": "Password confirmation doesn't match password"}), 400

#     exist = users_collection.find_one({"email": email})

#     if exist:
#         return jsonify({"error": "User already registered"}), 400

#     # use PBKDF2 with the SHA-256 hash function to securely hash passwords.
#     pwhash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

#     users_collection.insert_one({"email": email, "password": pwhash})

#     return jsonify({"message": "Registered successfully!"}), 201


# #Login
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     if not email or not password:
#         return jsonify({"error": "Please fill out all required fields"}), 400

#     user = users_collection.find_one({"email": email})

#     if not user:
#         return jsonify({"error": "You didn't register"}), 404

#     if not check_password_hash(user["password"], password):
#         return jsonify({"error": "Wrong password"}), 401

#     session["user_id"] = str(user["_id"])

#     return jsonify({"message": "Logged in successfully!"}), 200



# # Logout
# @app.route("/logout", methods=["POST"])
# def logout():
#     session.clear()
#     return jsonify({"message": "Logged out successfully!"}), 200


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
                  return send_file(resp["Body"], mimetype='image/jpeg')

                  

             elif side =="back":
                  toGet=photos["Back"]
                  resp=uploadImage.get_image_s3(toGet)
                  print(resp["Body"])
                  return send_file(resp["Body"], mimetype='image/jpeg')
        else:
             return jsonify({'error': str("error")}), 500
                  
                  





if __name__ == "__main__":
    app.run()