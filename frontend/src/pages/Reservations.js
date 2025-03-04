import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

const API_URL = "http://localhost:5000";

export default function Reservations() {
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/reservations`)
      .then((res) => res.json())
      .then((data) => setReservations(data));
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="p-6 w-full">
        <h1 className="text-2xl font-bold">Reservations</h1>
        <table className="w-full mt-4 border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-200">
              <th className="border border-gray-300 p-2">Customer</th>
              <th className="border border-gray-300 p-2">Table</th>
              <th className="border border-gray-300 p-2">Time</th>
            </tr>
          </thead>
          <tbody>
            {reservations.map((res) => (
              <tr key={res.id} className="text-center">
                <td className="border border-gray-300 p-2">{res.customer_name}</td>
                <td className="border border-gray-300 p-2">{res.table_id}</td>
                <td className="border border-gray-300 p-2">{res.time_slot}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
