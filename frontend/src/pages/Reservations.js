import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

const API_URL = "http://localhost:5000";

export default function Reservations() {
  const [reservations, setReservations] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

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

  // Function to parse and format time slot
  const formatTimeslot = (timeslot) => {
    const date = new Date(timeslot);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    return `${day}/${month}/${year} ${hours}:${minutes}`;
  };

  // Sorting function
  const sortedReservations = [...reservations].sort((a, b) => {
    if (sortConfig.key === null) return 0;
  
    const keyIndex = sortConfig.key;
    let valueA = a[keyIndex];
    let valueB = b[keyIndex];
  
    if (keyIndex === 0) {
      valueA = Number(valueA);
      valueB = Number(valueB);
    } else if (keyIndex === 5) {
      valueA = new Date(valueA);
      valueB = new Date(valueB);
    }
  
    return sortConfig.direction === "asc" ? (valueA > valueB ? 1 : -1) : (valueA < valueB ? 1 : -1);
  });

  // Handle column click for sorting
  const handleSort = (key) => {
    setSortConfig((prevConfig) => ({
      key,
      direction: prevConfig.key === key && prevConfig.direction === "asc" ? "desc" : "asc",
    }));
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="p-6 w-full">
        <h1 className="text-2xl font-bold">Reservations</h1>
        <form id="searchResForm">
          <label for="searchRes">Search by:</label>
          <select name="searchRes" id="searchRes">
            <option value="customerName">Customer name</option>
            <option value="date">Date</option>
            <option value="status">Status</option>
            <option value="tableID">Table ID</option>
          </select>
          <input type="text" id="itemname" name="itemname"/>
          <input type="submit" value="Search"/>
        </form>
        <table
          id="reservations-table"
          className="w-full mt-4 border-collapse border border-gray-300"
        >
          <thead>
            <tr className="bg-gray-200">
              {[
                "Reservation ID",
                "Table ID",
                "Customer Name",
                "Telephone Number",
                "Status",
                "Timeslot",
              ].map((header, index) => (
                <th
                  key={index}
                  className="border border-gray-300 p-2 cursor-pointer hover:bg-gray-300"
                  onClick={() => handleSort(index)}
                >
                  {header} {sortConfig.key === index ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
                </th>
              ))}
            </tr>
          </thead>
            <tbody>
              {sortedReservations.map((item, i) => (
                <tr key={i} className="hover:bg-gray-100">
                  <td className="border border-gray-300 p-2">{item[0]}</td> {/* Reservation ID */}
                  <td className="border border-gray-300 p-2">{item[1]}</td> {/* Table ID */}
                  <td className="border border-gray-300 p-2">{item[2]}</td> {/* Customer Name */}
                  <td className="border border-gray-300 p-2">{item[3]}</td> {/* Telephone Number */}
                  <td className="border border-gray-300 p-2">{item[4]}</td> {/* Status */}
                  <td className="border border-gray-300 p-2">{item[5]}</td> {/* Timeslot */}
                </tr>
              ))}
            </tbody>
          </table>
          <form id="cancelResForm">
            <label for="cancelRes">Search by:</label>
            <select name="cancelRes" id="cancelRes">
              <option value="customerName">Customer name</option>
              <option value="date">Date</option>
              <option value="status">Status</option>
              <option value="tableID">Table ID</option>
            </select>
            <input type="text" id="itemname" name="itemname"/>
            <input type="submit" value="Search"/>
          </form>
        </div>
      </div>
  );
}
