/*
Home Page for Doctors.
*/

import './Login.css';
import { useState } from 'react';
import Navbar from './Navbar';
import axios from 'axios';

export default function Patient({ role }) {
    const[patients, setPatients] = useState("");

    // call display patients API 
    const handleDisplay = () => {
        axios.post('http://127.0.0.1:5000/api/display-patients', {
            role: "patient"
        })
        .then(res => {
            setPatients(res.data);
            console.log('Response from display patients server:', res.data);
        })
        .catch(error => {
            console.error('Error sending message to display patients:', error);
        });
    };


    return (
        <div className="container">
            <Navbar role={role} />
            <h1>Patient Dashboard</h1>
            <button onClick={handleDisplay}>Click to Display Patients</button>
            <div>{patients.patients}</div>
        </div>
    )
}

