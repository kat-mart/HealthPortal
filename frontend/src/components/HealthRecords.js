/*
Health records page for doctors to view and manage their patient's health records.
This is only available to doctors and is hidden from the patient's navigation bar.
*/

import './HealthRecords.css';
import Navbar from './Navbar';
import axios from 'axios';

export default function HealthRecords({ role, pID, dID }) {

  const exportRecord = () => {
    axios.post('http://127.0.0.1:5000/export-health-records', {
        patient_id: pID
      }, {
        responseType: 'blob' // to get binary data
      })
      .then(res => {
        console.log('Response from server:', res);
        const url = window.URL.createObjectURL(new Blob([res.data])); // creates temporary url
        const a = document.createElement('a'); // creates an <a> element to trigger download
        a.href = url;
        a.download = 'health_records.csv';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Error exporting record:', error);
      });
  };

    return (
        <div className="container">
            <Navbar role={role} />
            <h1>Health Records</h1>
            {role === "patient" && <button onClick={exportRecord}>Export Health Record</button>}
        </div>
    )
}
