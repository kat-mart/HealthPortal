"""
Health Portal Backend API

This Python Flask application provides backend API endpoints for a Health Portal system. 
It interacts with the HealthPortal database to manage and retrieve information.
"""

# imports
from helper import helper
from db_operations import db_operations

# formating the date and time
from datetime import timedelta

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
    
# add a new patient to the database
@app.route('/patient-sign-up', methods=['POST'])
def add_patient():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    name = data["name"]
    dob = data["dob"]
    gender = data["gender"]
    phone = data["phone"]

    insert_patient = '''
    INSERT INTO patient(email,password,name,dob,gender,phone)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    db_ops.modify_query_params(insert_patient,(email,password,name,dob,gender,phone))

    select_max_id= '''
    SELECT MAX(patient_id)
    FROM patient;
    '''
    patient_id = db_ops.select_query(select_max_id)[0][0]

    return jsonify({"patient_id": patient_id})



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

# add a new doctor to the database
@app.route('/doctor-sign-up', methods=['POST'])
def add_doctor():
    data = request.get_json()
    name = data["name"]

    insert_doctor = '''
    INSERT INTO doctor(name)
    VALUES(%s)
    '''
    db_ops.modify_query_params(insert_doctor, (name,))

    # return the max id because autoincrement assigns the next largest id
    select_max_id = '''
    SELECT MAX(doctor_id)
    FROM doctor;
    '''
    doctor_id = db_ops.select_query(select_max_id)[0][0]

    return jsonify({"doctor_id": doctor_id})



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

@app.route('/add-appointment', methods=['POST'])
def add_appointment():
    data = request.get_json()
    find_doc = '''
    SELECT doctor_id 
    FROM doctor
    ORDER BY RAND() 
    LIMIT 1;
    '''
    result = db_ops.select_query(find_doc)  # This returns a list of tuples
    doctor_id = result[0][0]
    patient_id = data["patient_id"]
    date = data["newEventDate"]
    time = data["newEventTime"]
    status = data["eventStatus"]
    reason = data["newEventTitle"]

    insert_appointment = '''
    INSERT INTO appointment(date, time, status, reason, patient_id, doctor_id)
    VALUES(%s, %s, %s, %s, %s, %s)
    '''
    db_ops.modify_query_params(insert_appointment, (date, time, status, reason, patient_id, doctor_id))

    # Now fetch the newly created appointment_id
    get_appointment_id = "SELECT LAST_INSERT_ID();"
    appointment_id = db_ops.single_record(get_appointment_id)  # Fetch the last inserted id

    return jsonify({
        "result": "success",
        "appointment_id": appointment_id,  # Return the appointment_id
        "title": reason,
        "newEventDate": date,
        "newEventTime": time,
        "eventStatus": status
    })

# delete an appointment on click
@app.route('/delete-appointment', methods=['POST'])
def delete_appointment():
    data = request.get_json()
    appointment_id = data.get("appointment_id")

    if appointment_id:
        delete_query = '''
        DELETE FROM appointment WHERE appointment_id = %s
        '''
        db_ops.modify_query_params(delete_query, (appointment_id,))
        return jsonify({"result": "success", "message": f"Appointment {appointment_id} deleted."})
    else:
        return jsonify({"result": "failure", "message": "appointment_id is required."}), 400

@app.route('/get-appointments', methods=['GET'])
def get_appointments():
    ## TODO depending on the role either get patient ID or doctor ID
    patient_id = request.args.get("patient_id")
    patient_id = int(patient_id)

    query = '''
    SELECT appointment_id, date, time, status, reason
    FROM appointment
    WHERE patient_id = %s;
    '''
    appointments = db_ops.select_query_params(query, (patient_id,))
    appointments_list = [
        {
            "appointment_id": appointment[0],
            "date": str(appointment[1]),
            "time": str(appointment[2]),
            "status": appointment[3],
            "reason": appointment[4]
        }
        for appointment in appointments
    ]
    return jsonify({"appointments": appointments_list})

# main method
if __name__ == '__main__':
    initialize_database()
    
    # ensure db_ops.destructor() is called when the application exits
    atexit.register(db_ops.destructor)
    
    # start the Flask application
    app.run(debug=True)
