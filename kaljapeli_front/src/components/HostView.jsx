import React, { useEffect, useState } from "react";
import axios from "axios";

const HostView = ({ sessionCode }) => {
    const [players, setPlayers] = useState(null);

    const fetchParticipants = () => {
        axios
            .get(`http://localhost:5000/get_participants?code=${sessionCode}`)
            .then((response) => {
                console.log(response.data.participants);
                setPlayers(response.data.participants);
            })
            .catch((error) => {
                console.error("Error getting players:", error);
            });
    };

    const handleStartGame = () => {
        axios
            .post("http://localhost:5000/start_game", { code: sessionCode })
            .then((response) => {
                console.log(response.data.message);
                // Redirect to the game view
            })
            .catch((error) => {
                console.error("Error starting game:", error);
            });
    };

    useEffect(() => {
        fetchParticipants();
        const intervalId = setInterval(fetchParticipants, 5000);
        return () => clearInterval(intervalId);
    }, [sessionCode]);

    return (
        <div>
            <h1>You are hosting a Minute Beer</h1>
            {!players ? (
                <p>No players have joined yet.</p>
            ) : (
                (console.log(players),
                (
                    <div>
                        <h2>Players:</h2>
                        <ul>
                            {players.map((player) => (
                                <li key={player}>{player}</li>
                            ))}
                        </ul>
                        // when the host clicks this button, the game will start and the players will be redirected to
                        the game view
                        <button onClick={handleStartGame}>Start session</button>
                    </div>
                ))
            )}
        </div>
    );
};

export default HostView;
