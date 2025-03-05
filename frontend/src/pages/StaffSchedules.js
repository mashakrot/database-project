import React from "react";
import Sidebar from "../components/Sidebar";

export default function StaffSchedules() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="p-6 w-full">
        <h1 className="text-2xl font-bold">Staff Schedules</h1>
        <p>Manage staff shifts here...</p>
      </div>
    </div>
  );
}
