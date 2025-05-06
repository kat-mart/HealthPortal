#imports
from helper import helper
from db_operations import db_operations

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

    db_ops.populate_table('./csv_files/diagnosis.csv', 'diagnosis')
    db_ops.populate_table('./csv_files/doctors.csv', 'doctor')
    db_ops.populate_table('./csv_files/patients.csv', 'patient')
    db_ops.populate_table('./csv_files/records.csv', 'record')
    db_ops.populate_table('./csv_files/doctorRecords.csv', 'doctor_record')
    db_ops.populate_table('./csv_files/appointments.csv', 'appointment')
    db_ops.populate_table('./csv_files/tests.csv', 'test')
    db_ops.populate_table('./csv_files/labs.csv', 'lab')
    db_ops.populate_table('./csv_files/messages.csv', 'message')

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
    

# main method
def main():
    initialize_database()
    # display_patients()
    # verify_patient_account()
    # get_patient_profile()
    # verify_doctor_account()
    # get_doctor_profile()

    db_ops.destructor()


if __name__ == "__main__":
    main()