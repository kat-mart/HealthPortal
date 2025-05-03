/*
Home Page for Doctors.
*/

import './Doctor.css';
import { useState } from 'react';
import Navbar from './Navbar';

export default function Doctor({ role }) {
    return (
        <div className='container'>
            <Navbar role={role} />
            <h1>Doctor Dashboard</h1>
        </div>
    )
}

