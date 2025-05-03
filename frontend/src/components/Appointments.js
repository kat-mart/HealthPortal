/*
Apointments page for users to view and manage their appointments.
*/

import './Appointments.css';
import React, { useState } from 'react'; 
import Navbar from './Navbar';

import FullCalendar from '@fullcalendar/react';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction'; 

export default function Appointments({ role }) {
    const [events, setEvents] = useState([]);
    const [newEventTitle, setNewEventTitle] = useState('');
    const [newEventDate, setNewEventDate] = useState('');
    const [newEventTime, setNewEventTime] = useState('');

    const handleDateClick = (arg) => {
        alert('Date clicked: ' + arg.dateStr);
    };

    // adding a new event to the calendar
    const handleAddEvent = () => {
        if (newEventTitle && newEventDate && newEventTime) {
            const dateTime = `${newEventDate} ${newEventTime}`; // Combine date and time 

            const newEvent = {
                id: events.length + 1,  // generate a simple id based on current event length
                title: newEventTitle,
                date: dateTime,
            };

            setEvents([...events, newEvent]);  // add new event to the state
            setNewEventTitle('');
            setNewEventDate('');
            setNewEventTime('');
        } else {
            alert('Please fill in all fields (title, date, and time).');
        }
    };

    // deleting an event from the calendar
    const handleEventClick = (clickInfo) => {
        if (window.confirm('Are you sure you want to delete this event?')) {
            // remove the event from FullCalendar
            clickInfo.event.remove();
            setEvents(events.filter(event => event.id !== clickInfo.event.id));
        }
    };

    return (
        <div className='container'>
            <Navbar role={role} />
            <h1>Appointments</h1>
            
            <div className='appointment-header'>Upcoming events</div>
                <p>Add a new event:</p>
            <div className='add-event-form'>
                <input
                    type="text"
                    placeholder="Event Title"
                    value={newEventTitle}
                    onChange={(e) => setNewEventTitle(e.target.value)}/>
                <input
                    type="date"
                    value={newEventDate}
                    onChange={(e) => setNewEventDate(e.target.value)}/>
                <input
                    type="time"
                    value={newEventTime}
                    onChange={(e) => setNewEventTime(e.target.value)}/>
                <button onClick={handleAddEvent}>Add Event</button>
            </div>
            <div className='calender-container'>
                <FullCalendar
                    plugins={[listPlugin, interactionPlugin]} 
                    initialView="listMonth" 
                    events={events} 
                    dateClick={handleDateClick}
                    eventClick={handleEventClick}/>
            </div>
        </div>
    );
}