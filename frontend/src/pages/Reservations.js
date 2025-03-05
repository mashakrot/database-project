import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

const API_URL = "http://localhost:5000";

export default function Reservations() {
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/get_reservations`)
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        setReservations(data.reservations);
      } else {
        console.error("Error fetching reservations:", data.message);
      }
    })
    .catch((err) => console.error("Fetch error:", err));
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="p-6 w-full">
        <h1 className="text-2xl font-bold">Reservations</h1>
        <table id="reservations-table" className="w-full mt-4 border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-200">
              <th className="border border-gray-300 p-2">Reservation ID</th>
              <th className="border border-gray-300 p-2">Table ID</th>
              <th className="border border-gray-300 p-2">Customer name</th>
              <th className="border border-gray-300 p-2">Telephone Number</th>
              <th className="border border-gray-300 p-2">Status</th>
              <th className="border border-gray-300 p-2">Timeslot</th>
            </tr>
          </thead>
          <tbody>
          {reservations.map(item => (
              <tr key={item[0]}>
                <td>{item[0]}</td> {/* Reservation ID */}
                <td>{item[1]}</td> {/* Table ID */}
                <td>{item[2]}</td> {/* Customer name */}
                <td>{item[3]}</td> {/* Tel. Number */}
                <td>{item[4]}</td> {/* Status */}
                <td>{item[5]}</td> {/* Timeslot */}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
