import React, { useEffect, useState } from "react";
import axios from "axios";

const HostView = ({ sessionCode }) => {
    const [players, setPlayers] = useState([]);

    const fetchParticipants = () => {
        axios
            .get(`http://localhost:5000/get_participants?code=${sessionCode}`)
            .then((response) => {
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

    const handleKickPlayer = (player) => {
        axios
            .post("http://localhost:5000/remove_participant", { code: sessionCode, player })
            .then((response) => {
                console.log(response.data.message);
            })
            .catch((error) => {
                console.error("Error removing player:", error);
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
            {players.length < 1 ? (
                <p>No players have joined yet.</p>
            ) : (
                <div>
                    <h2>Players:</h2>
                    <ul>
                        {players.map((player) => (
                            <li key={player}>
                                {player}
                                <button onClick={() => handleKickPlayer(player)}>X</button>
                            </li>
                        ))}
                    </ul>
                    <button onClick={handleStartGame}>Start Game</button>
                </div>
            )}
        </div>
    );
};

export default HostView;
