/*
Messages page for doctors and patients to send and receive messages.
*/

import './Messages.css';
import React, { useState } from 'react'; 
import Navbar from './Navbar';

export default function Messages({ role }) {
    return (
        <div className='container'>
            <Navbar role={role} />
            <h1>Messages</h1>
            <form>
                <div>
                    <input type="text"/>
                    <button type="submit">Send</button>
                </div>
            </form>
        </div>
    );
}