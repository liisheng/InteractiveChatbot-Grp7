import React, { useState } from "react";
import axios from "axios";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      // No need to store the response if you are not using it
      await axios.post("http://localhost:8000/register", {
        username,
        password,
      });
      alert("Registration successful");
    } catch (error) {
      console.error(error);
      alert("Registration failed");
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
