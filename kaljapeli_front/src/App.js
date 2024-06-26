import React, { useState } from "react";
import axios from "axios";
import HostView from "./components/HostView";
import ParticipantView from "./components/ParticipantView";
import "./App.css"; // Import the CSS file

function App() {
    const [personalDetails, setPersonalDetails] = useState({
        name: "",
        weight: "",
        gender: "",
        drink_strength: "",
    });
    const [playerId, setPlayerId] = useState(""); // State to hold player's ID
    const [code, setCode] = useState("");
    const [choice, setChoice] = useState("");
    const [error, setError] = useState("");
    const [hosting, setHosting] = useState(false);
    const [sessionJoined, setSessionJoined] = useState(false);

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
                setCode(code);
            })
            .catch((error) => {
                console.error("Error starting session:", error);
                if (error.response && error.response.data && error.response.data.message) {
                    setError("Error starting session. Details: " + error.response.data.message);
                } else {
                    setError("Unknown error. Please try again later.");
                }
            });
    };

    const handleJoinSession = () => {
        if (code.trim() === "") {
            setError("Please enter a valid code.");
            return;
        }
        if (
            !personalDetails.name ||
            !personalDetails.weight ||
            !personalDetails.gender ||
            !personalDetails.drink_strength
        ) {
            setError("Please fill in all personal details.");
            return;
        }
        // Make a POST request to join the session with personal data
        axios
            .post("http://localhost:5000/join_session", {
                code,
                personalDetails,
            })
            .then((response) => {
                console.log(response.data.message);
                setSessionJoined(true);
                setPlayerId(response.data.participant_id); // Set player's ID
            })
            .catch((error) => {
                console.error("Error joining session:", error);
                if (error.response && error.response.data && error.response.data.message) {
                    setError("Error joining session. Details: " + error.response.data.message);
                } else {
                    setError("Unknown error. Please try again later.");
                }
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

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setPersonalDetails({
            ...personalDetails,
            [name]: value,
        });
    };

    return (
        <div className="container">
            {!hosting && !sessionJoined ? (
                <div>
                    <h1>Welcome to the Minute Beer App</h1>
                    <form onSubmit={handleSubmit}>
                        <p>Session details</p>
                        <label>
                            Enter code:
                            <input
                                type="text"
                                value={code}
                                name="code"
                                onChange={(e) => setCode(e.target.value)}
                            />
                        </label>
                        <br />
                        <label>
                            Choose:
                            <select
                                value={choice}
                                name="choice"
                                onChange={(e) => setChoice(e.target.value)}
                            >
                                <option value="">Select</option>
                                <option value="join">Join Session</option>
                                <option value="start">Start Session</option>
                            </select>
                        </label>
                        {choice === "join" && (
                            <>
                                <p>Personal details</p>
                                <label>
                                    Enter your name:
                                    <input
                                        type="text"
                                        value={personalDetails.name}
                                        name="name"
                                        onChange={handleInputChange}
                                    />
                                </label>
                                <br />
                                <label>
                                    Enter your weight:
                                    <input
                                        type="number"
                                        value={personalDetails.weight}
                                        name="weight"
                                        onChange={handleInputChange}
                                    />
                                </label>
                                <br />
                                <label>
                                    Are you male or female?
                                    <select
                                        value={personalDetails.gender}
                                        name="gender"
                                        onChange={handleInputChange}
                                    >
                                        <option value="">Select</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                    </select>
                                </label>
                                <br />
                                <label>
                                    What is the strength of your beer? (%)
                                    <input
                                        type="number"
                                        value={personalDetails.drink_strength}
                                        name="drink_strength"
                                        onChange={handleInputChange}
                                    />
                                </label>
                            </>
                        )}
                        <button type="submit">Submit</button>
                    </form>
                    {error && <p style={{ color: "red" }}>{error}</p>}
                </div>
            ) : hosting ? (
                <HostView sessionCode={code} />
            ) : (
                <ParticipantView
                    sessionCode={code}
                    playerId={playerId}
                />
            )}
        </div>
    );
}

export default App;
