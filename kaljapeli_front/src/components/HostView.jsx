import React, { useEffect, useState } from "react";
import axios from "axios";

const HostView = ({ sessionCode }) => {
    const [players, setPlayers] = useState(null);

    // Function to fetch participants from the server
    const fetchParticipants = () => {
        axios
            .get("http://localhost:5000/get_participants")
            .then((response) => {
                console.log(response.data.participants);
                setPlayers(response.data.participants);
            })
            .catch((error) => {
                console.error("Error getting players:", error);
            });
    };

    useEffect(() => {
        // Fetch participants when the component mounts
        fetchParticipants();

        // Polling to fetch participants every 5 seconds
        const intervalId = setInterval(fetchParticipants, 5000);

        // Cleanup function to clear the interval
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h1>You are hosting a Minute Beer</h1>
            {!players ? (
                <p>No players have joined yet.</p>
            ) : (
                <div>
                    <h2>Players:</h2>
                    <ul>
                        {players.map((player) => (
                            <li key={player}>{player}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default HostView;
