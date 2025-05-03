/*
Page for doctors to either sign in or create an account.
*/

import './Login.css';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function DoctorLogin() {
    const navigate = useNavigate();
    const[signUp, setSignUp] = useState(false);
    const[signIn, setSignIn] = useState(false);
    const[id, setID] = useState("");
    const[name, setName] = useState("");

    // saves user's choice when they click sign up or sign in
    const handleChoice = (input) => {
        if (input === "sign up") {
            setSignUp(true);
        } else if (input === "sign in") {
            setSignIn(true);
        }
    }

    // handle sign in
    const handleSignIn = (e) => {
        // TODO: Add logic to verify doctor credentials

        e.preventDefault();  
        navigate('/Doctor'); // redirect to Doctor page after sign in
    }

    // handle sign up
    const handleSignUp = (e) => {
        // TODO: Add logic to create a new doctor account

        e.preventDefault();  
        navigate('/Doctor'); // redirect to Doctor page after sign up
    }

    return (
        <div>
            <h1>Doctor</h1>

            {/* display both sign in and sign up options */}
            {!signIn && !signUp ? (
                <div className="account-container">
                    <button className="account-button" onClick={() => handleChoice("sign in")}>Sign In</button>
                    <button className="account-button" onClick={() => handleChoice("sign up")}>Create An Account</button>
                </div>
            ): null}
        
            {/* display sign in form if user selects sign in */}
            {signIn ? (
                <div>
                    <form className="login-form">
                        <div className="login-form-item">
                            <label>Enter Doctor ID:</label>
                            <input type="number" value={id} onChange={(e) => setID(e.target.value)}/>
                        </div>
                        <button onClick={(e) => handleSignIn(e)} type="submit">Sign In</button>
                    </form>
                    <button onClick={() => setSignIn(false)}>Back</button>
                </div>
            ) : null}
            
            {/* display sign up form if user selects sign up */}
            {signUp ? (
                <div> 
                    <form className="login-form">
                        <div className="login-form-item">
                            <label>Name:</label>
                            <input type="number" value={name} onChange={(e) => setName(e.target.value)}/>
                        </div>
                        <button onClick={(e) => handleSignUp(e)} type="submit">Sign Up</button>
                    </form>
                    <button onClick={() => setSignUp(false)}>Back</button>
                </div>
            ) : null}
        </div>
    )
}