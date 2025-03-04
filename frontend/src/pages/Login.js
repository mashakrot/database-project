import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-toastify";


const API_URL = "http://localhost:5000";

export default function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const login = async () => {
    setError(null);
    try {
      const response = await axios.post("http://localhost:5000/login", { email, password });
      localStorage.setItem("token", response.data.access_token);
      setUser(response.data.user);
      navigate("/dashboard");
      toast.success("Login successful!");
    } catch (error) {
      toast.error("Invalid credentials!");
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
        <p className="text-sm mt-3">Don't have an account? <Link to="/register" className="text-blue-500">Register here</Link></p>
      </div>
    </div>
  );
}
