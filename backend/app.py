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


# add patient's message to database
@app.route('/send-patient-message', methods=['POST'])
def send_patient_message():
    data = request.get_json()
    patient_id = data["id"]
    message_body = data["message_body"]

    # check if patient has messaged a doctor already
    select_doctor = '''
    SELECT doctor_id
    FROM message
    WHERE patient_id = %s;
    '''
    doctor_id = db_ops.select_query_params(select_doctor, (patient_id,))
    doctor_assigned = False
    
    # if message exists with a doctor then continue to send to that doctor
    if doctor_id:
        doctor_id = doctor_id[0][0] 
        doctor_assigned = True
    # if not then try to assign an available doctor
    else: 
        query = '''
        SELECT doctor_id
        FROM doctor
        WHERE doctor_id NOT IN (SELECT doctor_id FROM message);
        '''
        available_doctors = db_ops.select_query(query)
        available_doctors = [x[0] for x in available_doctors]

        if available_doctors:
            doctor_id = available_doctors[0]
            doctor_assigned = True
    
    # if doctor is available then assign to the patient
    if doctor_assigned == True:
        # add the patient's message to the message table
        insert_message = '''
        INSERT INTO message(message_body, timestamp, patient_id, doctor_id, sender_id)
        VALUES(%s, NOW(), %s, %s, %s);
        '''
        db_ops.modify_query_params(insert_message, (message_body, patient_id, doctor_id, patient_id))

        # return the max message id
        select_max_id = '''
        SELECT MAX(message_id)
        FROM message;
        '''
        message_id = db_ops.select_query(select_max_id)[0][0]

        # return patient name
        select_patient_name = '''
        SELECT name
        FROM patient
        WHERE patient_id = %s;
        '''
        sender_name = db_ops.select_query_params(select_patient_name, (patient_id,))[0][0]

        # return doctor name
        select_doctor_name = '''
        SELECT name
        FROM doctor
        WHERE doctor_id = %s;
        '''
        receiver_name = db_ops.select_query_params(select_doctor_name, (doctor_id,))[0][0]

        message = {
            "result": True,
            "message_id": message_id,
            "message_body": message_body,
            "receiver_id": doctor_id,
            "sender_id" : patient_id,
            "receiver_name": receiver_name,
            "sender_name": sender_name
        }
        return jsonify(message)
    # if no doctors are available
    else:
        return jsonify({"result": False})


# add doctor's message to database
@app.route('/send-doctor-message', methods=['POST'])
def send_doctor_message():
    data = request.get_json()
    doctor_id = data["id"]
    message_body = data["message_body"]

    # check if doctor has messaged a patient already
    select_patient = '''
    SELECT patient_id
    FROM message
    WHERE doctor_id = %s;
    '''
    patient_id = db_ops.select_query_params(select_patient, (doctor_id,))
    patient_assigned = False
    
    # if message exists with a patient then continue to send to that patient
    if patient_id:
        patient_id = patient_id[0][0] 
        patient_assigned = True
    # if not then try to assign an available patient
    else: 
        query = '''
        SELECT patient_id
        FROM patient
        WHERE patient_id NOT IN (SELECT patient_id FROM message);
        '''
        available_patients = db_ops.select_query(query)
        available_patients = [x[0] for x in available_patients]

        if available_patients:
            patient_id = available_patients[0]
            patient_assigned = True
    
    # if patient is available then assign to the doctor
    if patient_assigned == True:
        # add the doctor's message to the message table
        insert_message = '''
        INSERT INTO message(message_body, timestamp, patient_id, doctor_id, sender_id)
        VALUES(%s, NOW(), %s, %s, %s);
        '''
        db_ops.modify_query_params(insert_message, (message_body, patient_id, doctor_id, doctor_id))

        # return the max message id
        select_max_id = '''
        SELECT MAX(message_id)
        FROM message;
        '''
        message_id = db_ops.select_query(select_max_id)[0][0]

        # return patient name
        select_patient_name = '''
        SELECT name
        FROM patient
        WHERE patient_id = %s;
        '''
        receiver_name = db_ops.select_query_params(select_patient_name, (patient_id,))[0][0]

        # return doctor name
        select_doctor_name = '''
        SELECT name
        FROM doctor
        WHERE doctor_id = %s;
        '''
        sender_name = db_ops.select_query_params(select_doctor_name, (doctor_id,))[0][0]

        message = {
            "result": True,
            "message_id": message_id,
            "message_body": message_body,
            "receiver_id": patient_id,
            "sender_id" : doctor_id,
            "receiver_name": receiver_name,
            "sender_name": sender_name
        }
        return jsonify(message)
    # if no patients are available
    else:
        return jsonify({"result": False})


# select all messages between patient and doctor assuming 1-to-1 relationship
@app.route('/get-messages', methods=['POST'])
def select_messages():
    # could be patient or doctor
    data = request.get_json()
    role = data["role"]
    id = data["id"]

    messages = ""
    if role == "patient":
        select_messages = '''
        SELECT message.message_id, message.message_body, message.doctor_id, message.sender_id, doctor.name, patient.name
        FROM message
        INNER JOIN doctor
            ON message.doctor_id = doctor.doctor_id
        INNER JOIN patient
            ON message.patient_id = patient.patient_id
        WHERE message.patient_id = %s;
        '''
        messages = db_ops.select_query_params(select_messages, (id,))
    elif role == "doctor":
        select_messages = '''
        SELECT message.message_id, message.message_body, message.patient_id, message.sender_id, patient.name, doctor.name
        FROM message
        INNER JOIN patient
            ON message.patient_id = patient.patient_id
        INNER JOIN doctor
            ON message.doctor_id = doctor.doctor_id
        WHERE message.doctor_id = %s;
        '''
        messages = db_ops.select_query_params(select_messages, (id,))
    
    all_messages = []

    for message in messages:
        message_dict = {
            "result": True,
            "message_id": message[0],
            "message_body": message[1],
            "receiver_id": message[2],
            "sender_id" : message[3],
            "receiver_name": message[4],
            "sender_name": message[5]
        }
        
        all_messages.append(message_dict)
    
    return jsonify(all_messages)


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
