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

    const handleKickPlayer = (playerId) => {
        axios
            .post("http://localhost:5000/remove_participant", { code: sessionCode, playerId })
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
            {!Object.keys(players).length ? (
                <p>No players have joined yet.</p>
            ) : (
                <>
                    <h2>Players:</h2>
                    <ul>
                        {Object.keys(players).map((playerId) => (
                            <li key={playerId}>
                                {players[playerId].name}{" "}
                                <button onClick={() => handleKickPlayer(playerId)}>Kick</button>
                            </li>
                        ))}
                    </ul>
                    <button onClick={handleStartGame}>Start Game</button>
                </>
            )}
        </div>
    );
};

export default HostView;
