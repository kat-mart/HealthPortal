/*
Health records page for doctors to view and manage their patient's health records.
This is only available to doctors and is hidden from the patient's navigation bar.
*/

import './HealthRecords.css';
import Navbar from './Navbar';

export default function HealthRecords({ role }) {

    //add function for button
    return (
        <div className="container">
            <Navbar role={role} />
            <h1>Health Records</h1>
            <p>Here you can view and manage your health records.</p>
        </div>
    )
}


