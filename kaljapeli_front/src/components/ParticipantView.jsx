import React, { useState } from "react";
import axios from "axios";

const ParticipantView = ({ sessionCode, playerId }) => {
    const [started, setStarted] = useState(false);

    const handleLeaveSession = () => {
        // Make a POST request to leave the session by using the remove_participant endpoint
        axios
            .post("http://localhost:5000/remove_participant", { code: sessionCode, playerId })
            .then((response) => {
                console.log(response.data.message);
                // Redirect to the home page
                window.location.href = "/";
            })
            .catch((error) => {
                console.error("Error leaving session:", error);
            });
    };

    return (
        <div>
            <h1>You have joined the Minute Beer Session {sessionCode}</h1>
            <p>Waiting for the host to start the session...</p>
            {started ? (
                <div>The game has started! Redirecting to the game view...</div>
            ) : (
                <div>
                    <button onClick={() => handleLeaveSession()}>Leave Session</button>
                </div>
            )}
        </div>
    );
};

export default ParticipantView;
