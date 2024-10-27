// frontend/src/App.js
import React, { useState } from "react";
import axios from "axios";

function App() {
    const [text, setText] = useState("");
    const [skills, setSkills] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post("http://localhost:5000/extract-skills", { text });
            setSkills(response.data.skills);
        } catch (error) {
            console.error("Error extracting skills:", error);
        }
    };

    return (
        <div className="App">
            <h1>CV Skill Extractor</h1>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste CV text here"
                    rows="5"
                    cols="50"
                />
                <br />
                <button type="submit">Extract Skills</button>
            </form>
            <h2>Extracted Skills:</h2>
            <ul>
                {skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;
