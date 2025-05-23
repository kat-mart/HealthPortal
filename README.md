- Carolina Martinez, Heather Bisset, Katherine Martinez, Kelly Ung
- Student ID: 2427693, 2456534, 2431480, 2428408
- CPSC408-01
- Final Project


# Final Project - Healthcare Portal
Health Portal is a website that allows patients and doctors to create appointments and communicate with each other through messages. Patients can export their health records and view their lab results.


# Source Files:
   - backend - Python Flask application
       - app.py
           - contains endpoints to run database queries
       - db_operations.py
           - functions were added to create the tables
       - helper.py
   - frontend - React
       - all pages and styling for the website can be found in src > components
       - LandingPage.js
           - user selects whether they are a patient or doctor and redirects them to the correct page
       - PatientLogin.js
           - patient can choose to log in or sign up
       - Patient.js
           - homepage for the patient
       - DoctorLogin.js
           - doctor can choose to log in or sign up
       - Doctor.js
           - homepage for the doctor
       - Navbar.js
           - the navbar is only accessible once a patient/doctor successfully logs in or signs up
           - the Health Records is only available to the patient
       - Appointments.js
           - patients and doctors can view, create, and delete appointments
       - Messages.js
           - patient to doctor messaging system
           - for simplicaiton, communication is limited to one-on-one
           - the first message sent will automatically assign an available patient/doctor to message,
               if none are available then the user will be notified
       - HealthRecord.js
           - allows the patient to export their health records and view their lab results


# Description of any known compile or runtime errors, code limitations, or deviations:
   - in the event of a request error the backend may quit and you need to restart the application


# References:
   - Styling for frontend was referenced from our past React projects
   - Appointments calendar structure referenced from a past React project as well
  
# Special Instructions
   - There are some blocks of commented code labeled TODOs that you will need uncomment in the backend app.py
   - keep inputs for names, emails, etc. short due to character limits
   - email inputs are case sensitive
   - refrain from using back and forward arrows or refreshing the page to prevent unexpected behavior

# Known Errors
- For patient-side email is case sensitive it will still let you login but you won't be able to view anything 
- The views and index creation should only be run once

# Installs:
   - pip install Flask
   - pip install flask-cors
   - pip install django djangorestframework
   - npm install
   - npm install @fullcalendar/react @fullcalendar/list @fullcalendar/interaction


# To run:
   - cd into backend --> run app.py
   - open in separate terminal: cd into frontend --> npm start
