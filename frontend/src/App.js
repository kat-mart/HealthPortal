/*
Main application component for the healthcare portal. 
It sets up the routing for all pages and saves the user's selected role (either patient or doctor).
*/

import './App.css';
import { Route, Routes } from 'react-router-dom';
import { useState } from 'react';

import LandingPage from './components/LandingPage';
import DoctorLogin from './components/DoctorLogin';
import PatientLogin from './components/PatientLogin';
import Doctor from './components/Doctor';
import Patient from './components/Patient';
import Appointments from './components/Appointments';
import Messages from './components/Messages';
import HealthRecords from './components/HealthRecords';

function App() {
  const [role, setRole] = useState("");

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<LandingPage setRole={setRole} />} /> 
        <Route path="/DoctorLogin" element={<DoctorLogin />} />
        <Route path="/PatientLogin" element={<PatientLogin />} />
        <Route path="/Doctor" element={<Doctor role={role} />} />
        <Route path="/Patient" element={<Patient role={role} />} />
        <Route path="/Appointments" element={<Appointments role={role} />} />
        <Route path="/Messages" element={<Messages role={role} />} />
        <Route path="/HealthRecords" element={<HealthRecords role={role} />} />
      </Routes>
    </div>
  );
}

export default App;
