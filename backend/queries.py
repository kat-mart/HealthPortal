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

    # db_ops.populate_table('./diagnosis.csv', 'diagnosis')
    # db_ops.populate_table('./doctors.csv', 'doctor')
    # db_ops.populate_table('./patients.csv', 'patient')
    # db_ops.populate_table('./records.csv', 'record')
    # db_ops.populate_table('./doctorRecords.csv', 'doctor_record')
    # db_ops.populate_table('./appointments.csv', 'appointment')
    # db_ops.populate_table('./tests.csv', 'test')
    # db_ops.populate_table('./labs.csv', 'lab')
    # db_ops.populate_table('./messages.csv', 'message')

# this is a test function to display patients  
def display_patients():
    data = {"role": "patient"} # example data
    
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

# main method
def main():
    initialize_database()
    display_patients()

    db_ops.destructor()


if __name__ == "__main__":
    main()