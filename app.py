from flask import Flask, request, redirect, session, render_template, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

mongo_uri = ""
client = MongoClient(mongo_uri)

# database name
db = client[""]

# users collection
users_collection = db.users



# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    confirmation = data.get("confirmation")

    if not email or not password or not confirmation:
        return jsonify({"error": "Please fill out all fields"}), 400

    if password != confirmation:
        return jsonify({"error": "Password confirmation doesn't match password"}), 400

    exist = users_collection.find_one({"email": email})

    if exist:
        return jsonify({"error": "User already registered"}), 400

    # use PBKDF2 with the SHA-256 hash function to securely hash passwords.
    pwhash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

    users_collection.insert_one({"email": email, "password": pwhash})

    return jsonify({"message": "Registered successfully!"}), 201


#Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Please fill out all required fields"}), 400

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "You didn't register"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Wrong password"}), 401

    session["user_id"] = str(user["_id"])

    return jsonify({"message": "Logged in successfully!"}), 200



# Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200

if __name__ == "__main__":
    app.run()