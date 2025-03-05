import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Reservations from "./pages/Reservations";
import Inventory from "./pages/Inventory";
import StaffSchedules from "./pages/CalendarSchedule";

export default function App() {
  const [user, setUser] = useState(null);

  return (
    <Router>
      <Routes>
        <Route path="/" element={!user ? <Login setUser={setUser} /> : <Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={user ? <Dashboard user={user} /> : <Navigate to="/" />} />
        <Route path="/reservations" element={<Reservations />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/schedules" element={<StaffSchedules />} />
      </Routes>
    </Router>
  );
}
