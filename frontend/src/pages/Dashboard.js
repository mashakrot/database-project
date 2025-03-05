import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

const API_URL = "http://localhost:3000";

export default function Dashboard({ user }) {
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/reservations`)
      .then((res) => res.json())
      .then((data) => setReservations(data));
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 ml-60 p-5">

        <div className="p-6 w-full">
          <h1 className="text-2xl font-bold">Welcome, {user?.name}</h1>
          {/* <p>Your role: {user?.role}</p> */}

  {/* maybe add workers schedules here...now it is in staffschedules  */}
        </div>
      </div>
    </div>
  );
}
