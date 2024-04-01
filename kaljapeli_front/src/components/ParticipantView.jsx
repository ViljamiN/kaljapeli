import React, { useState } from "react";
import axios from "axios";

const ParticipantView = () => {
    const [started, setStarted] = useState(false);

    const handleLeaveSession = () => {
        axios
            .post("http://localhost:5000/leave_session")
            .then((response) => {
                console.log(response.data.message);
            })
            .catch((error) => {
                console.error("Error leaving session:", error);
            });
    };

    return (
        <div>
            <h1>You have joined the Minute Beer Session number %sessionNumber%</h1>
            <p>Waiting for the host to start the session...</p>
            {started ? (
                <div>The game has started! Redirecting to the game view...</div>
            ) : (
                <div>
                    <button onClick={handleLeaveSession}>Leave Session</button>
                </div>
            )}
        </div>
    );
};

export default ParticipantView;
