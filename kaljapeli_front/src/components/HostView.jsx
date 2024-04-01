import React, { useEffect, useState } from "react";
import axios from "axios";

// This component is displayed when the user is hosting a Minute Beer
// It gets the player names from the server and displays them

const HostView = () => {
    //get the players from the server
    const [players, setPlayers] = useState(null);

    useEffect(() => {
        axios
            .get("http://localhost:5000/get_participants")
            .then((response) => {
                console.log(response.data.players);
                setPlayers(response.data.players);
            })
            .catch((error) => {
                console.error("Error getting players:", error);
            });
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
