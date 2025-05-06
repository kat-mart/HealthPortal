/*
Home Page for Patients.
*/

import './Login.css';
import { useState, useEffect } from 'react';
import Navbar from './Navbar';
import axios from 'axios';

export default function Patient({ role, id }) {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [dob, setDob] = useState("");
    const [gender, setGender] = useState("");
    const [phone, setPhone] = useState("");

    // display patient profile
    useEffect(() => {
        if (id !== "") {
          // delay the call by 1 ms
          const timer = setTimeout(() => {
            const fetchData = () => {
              axios.post('http://127.0.0.1:5000/patient-profile', {
                patient_id: id
              })
              .then(res => {
                console.log('Response from patient profile server:', res.data);
                setName(res.data.name);
                setEmail(res.data.email);
                setDob(res.data.dob);
                setGender(res.data.gender);
                setPhone(res.data.phone);
              })
              .catch(error => {
                console.error('Error sending message to patient profile:', error);
              });
            };
    
            fetchData(); 
          }, 1);  // 1ms delay
    
          // cleanup timeout if the component is unmounted or if id changes
          return () => clearTimeout(timer);
        }
    }, [id]); // run when id changes

    return (
        <div className="container">
            <Navbar role={role} />
            <h1>Patient Dashboard</h1>
            <h2>Hi, {name}</h2>
            <p>Patient ID: {id}</p>
            <p>Email: {email}</p>
            <p>Date of Birth: {dob}</p>
            <p>Gender: {gender}</p>
            <p>Phone: {phone}</p>
        </div>
    )
}

