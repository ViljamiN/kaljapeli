import React, { useState } from "react";
import axios from "axios";
import HostView from "./components/HostView";
import ParticipantView from "./components/ParticipantView";

function App() {
    const [code, setCode] = useState("");
    const [name, setName] = useState("");
    const [choice, setChoice] = useState("");
    const [error, setError] = useState("");
    const [hosting, setHosting] = useState(false);
    const [sessionJoined, setSessionJoined] = useState(false);

    const handleCodeChange = (e) => {
        setCode(e.target.value);
    };

    const handleNameChange = (e) => {
        setName(e.target.value);
    };

    const handleChoiceChange = (e) => {
        setChoice(e.target.value);
    };

    const handleStartSession = () => {
        if (code.trim() === "") {
            setError("Please enter a valid code.");
            return;
        }
        // Make a POST request to start the session
        axios
            .post("http://localhost:5000/start_session", { code })
            .then((response) => {
                console.log(response.data.message);
                setHosting(true);
            })
            .catch((error) => {
                console.error("Error starting session:", error);
            });
    };

    const handleJoinSession = () => {
        if (code.trim() === "") {
            setError("Please enter a valid code.");
            return;
        }
        // Make a POST request to join the session
        axios
            .post("http://localhost:5000/join_session", { code })
            .then((response) => {
                console.log(response.data.message);
                setSessionJoined(true);
            })
            .catch((error) => {
                console.error("Error joining session:", error);
            });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (choice === "") {
            setError("Please select an option.");
            return;
        }
        if (choice === "start") {
            handleStartSession();
        }
        if (choice === "join") {
            handleJoinSession();
        }
    };

    return (
        <div>
            {!hosting && !sessionJoined ? (
                <div>
                    <h1>Welcome to the Session App</h1>
                    <form onSubmit={handleSubmit}>
                        <label>
                            Enter Code:
                            <input
                                type="text"
                                value={code}
                                onChange={handleCodeChange}
                            />
                        </label>
                        <br />
                        <label>
                            Enter Your Name:
                            <input
                                type="text"
                                value={name}
                                onChange={handleNameChange}
                            />
                        </label>
                        <br />
                        <label>
                            Choose:
                            <select
                                value={choice}
                                onChange={handleChoiceChange}
                            >
                                <option value="join">Join Session</option>
                                <option value="start">Start Session</option>
                            </select>
                        </label>
                        <br />
                        <button type="submit">Submit</button>
                    </form>
                    {error && <p style={{ color: "red" }}>{error}</p>}
                </div>
            ) : hosting ? (
                <HostView />
            ) : (
                <ParticipantView />
            )}
        </div>
    );
}

export default App;
