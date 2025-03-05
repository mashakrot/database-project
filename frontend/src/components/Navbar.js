import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-white shadow-md p-4 flex justify-between items-center">
      <h1 className="text-xl font-semibold text-gray-800">Smart Restaurant</h1>
      <div className="space-x-6">
        <Link to="/dashboard" className="hover:text-gray-400">Dashboard</Link>
        <Link to="/reservations" className="hover:text-gray-400">Reservations</Link>
        <Link to="/inventory" className="hover:text-gray-400">Inventory</Link>
      </div>
    </nav>
  );
}
