import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-toastify";

const API_URL = "http://localhost:5000";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Staff");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await axios.post(API_URL, { name, email, password, role });
      toast.success(`User registered successfully! UserID: ${response.data.userid}`);
      navigate("/");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-96">
        <h2 className="text-xl font-semibold mb-4">Register</h2>
        <input className="border w-full p-2 mb-3 rounded" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input className="border w-full p-2 mb-3 rounded" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="border w-full p-2 mb-3 rounded" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <select className="border w-full p-2 mb-3 rounded" value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="Manager">Manager</option>
          <option value="Host">Host</option>
          <option value="Waiter">Waiter</option>
          <option value="Cook">Cook</option>
          <option value="Cleaning Staff">Cleaning Staff</option>
        </select>
        <button className="bg-blue-500 text-white w-full p-2 rounded hover:bg-blue-600" onClick={handleRegister}>Register</button>
        <p className="text-sm mt-3">Already have an account? <Link to="/login" className="text-blue-500">Login here</Link></p>
      </div>
    </div>
  );
}
