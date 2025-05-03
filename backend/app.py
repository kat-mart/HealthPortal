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
CORS(app)

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


# display patients in the database
@app.route('/api/display-patients', methods=['POST'])
def display_patients():
    data = request.get_json()
    
    if data["role"] == "patient":
        query = '''
        SELECT patient_id, name, email, dob, gender, phone
        FROM Patient
        '''
        patients = db_ops.select_query(query)
        allPatients = ""
        for patient in patients:
            allPatients += str(patient) + "\n"
        print(allPatients)

    return jsonify({"patients": allPatients})

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

# main method
if __name__ == '__main__':
    initialize_database()
    
    # ensure db_ops.destructor() is called when the application exits
    atexit.register(db_ops.destructor)
    
    # start the Flask application
    app.run(debug=True)
