#imports
from helper import helper
from db_operations import db_operations
import csv

#global variables
db_ops = db_operations("localhost")

#functions

# populate the database with initial data
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

    # db_ops.populate_table('./csv_files/diagnosis.csv', 'diagnosis')
    # db_ops.populate_table('./csv_files/doctors.csv', 'doctor')
    # db_ops.populate_table('./csv_files/patients.csv', 'patient')
    # db_ops.populate_table('./csv_files/records.csv', 'record')
    # db_ops.populate_table('./csv_files/doctorRecords.csv', 'doctor_record')
    # db_ops.populate_table('./csv_files/appointments.csv', 'appointment')
    # db_ops.populate_table('./csv_files/tests.csv', 'test')
    # db_ops.populate_table('./csv_files/labs.csv', 'lab')
    # db_ops.populate_table('./csv_files/messages.csv', 'message')

# this is a test function to display patients  
def display_patients():
    data = {"role": "patient"} # example data
    
    if data["role"] == "patient":
        query = '''
        SELECT patient_id, name, email, dob, gender, phone
        FROM patient;
        '''
        patients = db_ops.select_query(query)
        allPatients = ""
        for patient in patients:
            allPatients += str(patient) + "\n"
        print(allPatients)

# check if patient's email and password are in the database and return patient_id
def verify_patient_account():
    data = {"email": "brian@email.com", "password": "b456word"} # example data
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
        result = "success"
    else:
        result = "error"

# get patient personal details based on patient_id
def get_patient_profile():
    data = {"patient_id": 2} # example data
    patient_id = data["patient_id"]

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

# check if doctor's id is in the database and return doctor_id
def verify_doctor_account():
    data = {"doctor_id": 301} # example data
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
    else:
        result = "error"

# get doctor personal details based on doctor_id
def get_doctor_profile():
    data = {"doctor_id": 301} # example data
    doctor_id = data["doctor_id"]

    query = '''
    SELECT name
    FROM doctor
    WHERE doctor_id = %s;
    '''
    name = db_ops.select_query(query % doctor_id)[0][0]

# add a new doctor to the database
def add_doctor():
    data = {"name": "Dr. Wendy Lopez"}
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
    print(doctor_id)


# add new patient info
def add_patient():
    data = {"name" : "Lisa", "email" : "lisa@gmail.com", "password" : "1234", "dob" : "2000-01-01", "gender" : "F", "phone" : "7147471740"} # example data
    name = data["name"]
    email = data["email"]
    password = data["password"]
    dob = data["dob"]
    gender = data["gender"]
    phone = data["phone"]

    insert_patient = '''
    INSERT INTO patient(name, email, password, dob, gender, phone)
    VALUES(%s, %s, %s, %s, %s, %s)
    '''
    db_ops.modify_query_params(insert_patient, (name, email, password, dob, gender, phone))
    
    select_max_id = '''
    SELECT MAX(patient_id)
    FROM patient;
    '''
    patient_id = db_ops.select_query(select_max_id)[0][0]
    print(patient_id)

# select all messages between patient and doctor assuming 1-to-1 relationship
def select_messages():
    # could be patient or doctor
    data = {"role": "patient", "id": 1}
    # data = {"role": "doctor", "id": 301}
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
            "message_id": message[0],
            "message_body": message[1],
            "receiver_id": message[2],
            "sender_id" : message[3],
            "receiver_name": message[4],
            "sender_name": message[5]
        }

        all_messages.append(message_dict)


# add patient's message to database
def send_patient_message():
    data = {"id": 3, "message_body": "Yes that works"}
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
            "message_id": message_id,
            "message_body": message_body,
            "receiver_id": doctor_id,
            "sender_id" : patient_id,
            "receiver_name": receiver_name,
            "sender_name": sender_name
        }
        print(message)
    # if no doctors are available
    else:
        print("no doctors found")


# add doctor's message to database
def send_doctor_message():
    data = {"id": 305, "message_body": "Reminder for appointment tomorrow"}
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
            "message_id": message_id,
            "message_body": message_body,
            "receiver_id": patient_id,
            "sender_id" : doctor_id,
            "receiver_name": receiver_name,
            "sender_name": sender_name
        }
        print(message)
    # if no patients are available
    else:
        print("no patients found")
        

# query to update patiet's phone number
def update_patient_phone():
    data = {"patient_id" : 2, "new_phone" : "9491234567"}
    patient_id = data["patient_id"]
    new_phone = data["new_phone"]

    update_query = '''
    UPDATE patinet
    SET phone = %s
    WHERE patient_id = %s;
    '''

    db_ops.modify_query_params(update_query, (new_phone, patient_id))
    print(f"Updated phone number for patient_id {patient_id} to {new_phone}")
    
# query for patients to be able to export their health records as a csv
def export_health_records(patient_id, file_path = 'exported_health_records.csv'):
    export_query = '''
    SELECT r.record_id, r.date AS record_date, r.notes, d.diagnosis, d.treatment, doc.name AS doctor_name
    FROM record r
    INNER JOIN diagnosis d 
        ON r.diagnosis_id = d.diagnosis_id
    INNER JOIN doctor_record dr 
        ON r.record_id = dr.record_id
    INNER JOIN doctor doc
        ON dr.doctor_id = doc.doctor_id
    WHERE r.patient_id = %s
    ORDER BY r.date DESC;
    '''

    records = db_ops.select_query_params(export_query, (patient_id,))

    with open(file_path, mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        # csv header
        writer.writerow(['Record ID', 'Date', 'Notes', 'Diagnosis', 'Treatment', 'Doctor Name'])
        for row in records:
            writer.writerow(row)
   
    print(f"Health records for patient_id {patient_id} exported to {file_path}")

# query to count appointments per doctor
def count_appointments_per_doctor():
    query = '''
    SELECT d.name AS doctor_name, COUNT(*) AS appointment_count
    FROM appointment a
    JOIN doctor d 
        ON a.doctor_id = d.doctor_id
    GROUP BY d.name
    ORDERY BY appointment_count DESC;
    '''

    results = db_ops.select_query(query)
    for row in results:
        print(f"{row[0]} has {row[1]} appointments.")

# transaction query! when patients book appts, it randomly assigns a doctor, and sends that doctor and automatic message
def book_appt_message_doctor(patient_id, date, time, status = None, reason = None):
    try:
        db_ops.connection.start_transaction()

        # randomly assign a doctor
        select_random_doctor = '''
        SELECT doctor_id 
        FROM doctor
        ORDER BY RAND()
        LIMIT 1;
        '''

        doctor_id = db_ops.select_query(select_random_doctor)[0][0]

        # insert appointment
        insert_appointment = '''
        INSERT INTO appointment(date, time, status, reason, patient_id, doctor_id)
        VALUES(%s, %s, %s, %s, %s, %s)
        '''

        db_ops.modify_query_params(insert_appointment, (date, time, status, reason, patient_id, doctor_id))

        # create a message
        message_body = f"A new appointment has been booked with patient ID {patient_id} on {date} at {time}."
        insert_message = '''
        INSERT INTO message(patient_id, doctor_id, message_body, timestamp)
        VALUES(%s, %s, %s, NOW())
        '''

        db_ops.modify_query_params(insert_message, (patient_id, doctor_id, message_body))
        
        # commit transaction
        db_ops.connection.commit()
        print(f"Appointment booked and doctor (ID {doctor_id}) notified.")
    
    except Exception as e:
        db_ops.connection.rollback()
        print("Transaction failed:", e)

# database view query - patient appointment summary
def create_patient_appt_summary_view():
    query = '''
    CREATE VIEW patient_appt_summary AS
    SELECT a.appointment_id, a.patient_id, p.name AS patient_name, d.name AS doctor_name, a.date, a.time, a.status, a.reason
    FROM appointment a
    JOIN patient p 
        ON a.patient_id = p.patient_id
    JOIN doctor d
        ON a.doctor_id = d.doctor_id
    '''

    db_ops.modify_query(query)
    print("View patient_appointment_summary created.")

# database index query - search patients by their ids
def create_index():
    query = '''
    CREATE INDEX index_patient_id ON appointment(patinet_id)
    '''
    db_ops.modify_query(query)
    print("Index idx_patient_id created on appointment(patient_id).")

def get_appointments():
    patient_id = 2

    query = '''
    SELECT appointment_id, date, time, status, reason, patient_id
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
    helper.pretty_print(appointments_list)
    

# main method
def main():
    initialize_database()
    # add_patient()
    # display_patients()
    # verify_patient_account()
    # get_patient_profile()
    # verify_doctor_account()
    # get_doctor_profile()
    # add_doctor()
    # select_messages()
    # send_patient_message()
    # send_doctor_message()


    create_patient_appt_summary_view()
    create_index()

    book_appt_message_doctor(
        patient_id = 1,  
        date = "2025-05-15",
        time = "14:30:00"
    )

    db_ops.destructor()


if __name__ == "__main__":
    main()
