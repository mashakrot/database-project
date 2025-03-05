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

  // Sorting function
  const sortedReservations = [...reservations].sort((a, b) => {
    if (!sortConfig.key) return 0; // If no sorting key is selected, return as is

    const keyIndex = sortConfig.key;
    const valueA = a[keyIndex];
    const valueB = b[keyIndex];

    if (typeof valueA === "string") {
      return sortConfig.direction === "asc"
        ? valueA.localeCompare(valueB)
        : valueB.localeCompare(valueA);
    } else {
      return sortConfig.direction === "asc" ? valueA - valueB : valueB - valueA;
    }
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
      <div className="flex-1 ml-60 p-5">

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
    </div>
  );
}
