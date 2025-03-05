import React from "react";
import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="fixed top-0 left-0 w-60 bg-gray-900 text-white h-screen p-5">
      <h2 className="text-lg font-semibold mb-5">Menu</h2>
      <ul className="space-y-2">
        <li>
          <Link
            to="/reservations"
            className="block py-3 px-4 rounded-md transition bg-gray-900 hover:bg-gray-700"
          >
            Reservations
          </Link>
        </li>
        <li>
          <Link
            to="/inventory"
            className="block py-3 px-4 rounded-md transition bg-gray-900 hover:bg-gray-700"
          >
            Inventory
          </Link>
        </li>
        <li>
          <Link
            to="/schedules"
            className="block py-3 px-4 rounded-md transition bg-gray-900 hover:bg-gray-700"
          >
            Schedules
          </Link>
        </li>
        <li>
          <Link
            to="/users"
            className="block py-3 px-4 rounded-md transition bg-gray-900 hover:bg-gray-700"
          >
            Users Management
          </Link>
        </li>
        <li>
          <Link
            to="/dashboard"
            className="block py-3 px-4 rounded-md transition bg-gray-900 hover:bg-gray-700"
          >
            Log out
          </Link>
        </li>
      </ul>
    </div>
  );
}
