import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = "http://localhost:5000";

export default function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const login = async (event) => {
    event.preventDefault(); 
    setError(null);

    
    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok) {
        console.log("Login successful:", data);
        localStorage.setItem("token", data.access_token); // Save token
        setUser(data.user); // Store user in state
        navigate("/dashboard"); // Redirect to dashboard
      } else {
        setError(data.message || "Invalid credentials");
      }
    } catch (err) {
      setError("Server error, please try again later.");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold text-center mb-4">Login</h2>
        {error && <p className="text-red-500 text-center mb-2">{error}</p>}
        <input
          className="w-full border rounded p-2 mb-3"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="w-full border rounded p-2 mb-3"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white w-full py-2 rounded hover:bg-blue-600"
          onClick={login}
        >
          Login
        </button>
      </div>
    </div>
  );
}
