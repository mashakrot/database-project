import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

const API_URL = "http://localhost:5000";

export default function Dashboard({ user }) {
  const [reservations, setReservations] = useState([]);
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/reservations`)
      .then((res) => res.json())
      .then((data) => setReservations(data));

    fetch(`${API_URL}/inventory`)
      .then((res) => res.json())
      .then((data) => setInventory(data));
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="p-6 w-full">
        <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
        <h2 className="text-xl font-semibold mt-4">Reservations</h2>
        <ul>
          {reservations.map((res) => (
            <li key={res.id}>{res.customer_name} - Table {res.table_id} at {res.time_slot}</li>
          ))}
        </ul>

        <h2 className="text-xl font-semibold mt-4">Inventory</h2>
        <ul>
          {inventory.map((item) => (
            <li key={item.item_id}>{item.item_name} - {item.quantity} left</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
