"""
Health Portal Backend API

This Python Flask application provides backend API endpoints for a Health Portal system. 
It interacts with the HealthPortal database to manage and retrieve information.
"""

# imports
from helper import helper
from db_operations import db_operations

# flask imports
from flask import Flask, jsonify, request
from flask_cors import CORS # allow API calls from localhost
import atexit # used to close database connection when the application exits

# initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# global variables
db_ops = db_operations("localhost")

# functions
def initialize_database():
    print("Welcome to Health Portal!")

    # db_ops.create_diagnosis_table()
    # db_ops.create_doctor_table()
    # db_ops.create_patient_table()
    # db_ops.create_record_table()
    # db_ops.create_doctor_record_table()
    # db_ops.create_appointment_table()
    # db_ops.create_test_table()
    # db_ops.create_lab_table()
    # db_ops.create_message_table()

    # db_ops.populate_table('./diagnosis.csv', 'diagnosis')
    # db_ops.populate_table('./doctors.csv', 'doctor')
    # db_ops.populate_table('./patients.csv', 'patient')
    # db_ops.populate_table('./records.csv', 'record')
    # db_ops.populate_table('./doctorRecords.csv', 'doctor_record')
    # db_ops.populate_table('./appointments.csv', 'appointment')
    # db_ops.populate_table('./tests.csv', 'test')
    # db_ops.populate_table('./labs.csv', 'lab')
    # db_ops.populate_table('./messages.csv', 'message')


@app.route('/messages', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    # if not user_message:
    #     return jsonify({'response': 'Error: No message provided.'}), 400

    # try:
    #     ## TODO: get the senders message and pass it through
    #     user_text = response.text
        
    #     return jsonify({'response': user_text})
    # except Exception as e:
    #     print(f"Error: {str(e)}")


# check if patient's email and password are in the database and return patient_id
@app.route('/patient-sign-in', methods=['POST'])
def verify_patient_account():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    
    query = '''
    SELECT patient_id
    FROM patient
    WHERE email = %s AND password =  %s;
    '''
    account = db_ops.select_query_params(query, (email, password))

    result = ""
    if account:
        patient_id = account[0][0]
        print(patient_id)
        result = "success"
        return jsonify({"result": result, "patient_id": patient_id})
    else:
        result = "error"
        return jsonify({"result": result})


# get patient personal details based on patient_id
@app.route('/patient-profile', methods=['POST'])
def get_patient_profile():
    data = request.get_json()
    patient_id = data["patient_id"]
    print(patient_id)

    query = '''
    SELECT name, email, dob, gender, phone
    FROM patient
    WHERE patient_id = %s;
    '''
    info = db_ops.select_query(query % patient_id)[0]
    name = info[0]
    email = info[1]
    dob = info[2]
    gender = info[3]
    phone = info[4]

    return jsonify({"name": name, "email": email, "dob": dob, "gender": gender, "phone": phone})

# check if doctor's id is in the database and return doctor_id
@app.route('/doctor-sign-in', methods=['POST'])
def verify_doctor_account():
    data = request.get_json()
    doctor_id = data["doctor_id"]

    query = '''
    SELECT doctor_id
    FROM doctor
    WHERE doctor_id = %s;
    '''
    account = db_ops.select_query(query % doctor_id)
    
    result = ""
    if account:
        doctor_id = account[0][0]
        result = "success"
        return jsonify({"result": result, "doctor_id": doctor_id})
    else:
        result = "error"
        return jsonify({"result": result})


# get doctor personal details based on doctor_id
@app.route('/doctor-profile', methods=['POST'])
def get_doctor_profile():
    data = request.get_json() 
    doctor_id = data["doctor_id"]

    query = '''
    SELECT name
    FROM doctor
    WHERE doctor_id = %s;
    '''
    name = db_ops.select_query(query % doctor_id)[0][0]

    return jsonify({"name": name})


# main method
if __name__ == '__main__':
    initialize_database()
    
    # ensure db_ops.destructor() is called when the application exits
    atexit.register(db_ops.destructor)
    
    # start the Flask application
    app.run(debug=True)
