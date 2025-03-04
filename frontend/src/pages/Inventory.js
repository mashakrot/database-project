import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";

export default function Inventory() {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    // Fetch data from the Flask backend
    const fetchInventory = async () => {
      try {
        const response = await fetch("http://localhost:5000/get_inventory", { // Adjust URL
          method: "POST",
        });
        const data = await response.json();
        if (data.status === "success") {
          setInventory(data.inventory);
        } else {
          console.log("Error:", data.message);
        }
      } catch (error) {
        console.error("Error fetching inventory:", error);
      }
    };

    fetchInventory();
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="p-6 w-full">
        <h1 className="text-2xl font-bold">Inventory Management</h1>
        <h2>Inventory List</h2>
        <table id="inventory-table">
          <thead>
            <tr>
              <th>Item ID</th>
              <th>Name</th>
              <th>Quantity</th>
              <th>Category</th> {/* Renamed this for clarity */}
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map(item => (
              <tr key={item[0]}>
                <td>{item[0]}</td> {/* Item ID */}
                <td>{item[1]}</td> {/* Item Name */}
                <td>{item[2]}</td> {/* Quantity */}
                <td>{item[3]}</td> {/* Category */}
                <td>${item[4]}</td> {/* Price */}
              </tr>
            ))}
          </tbody>
        </table>
        <form>
          <input type="text" id="itemid" name="itemid"/>
          <input type="submit" value="Search"></input>
        </form>
        <form>
          <input type="text" id="itemname" name="itemname"/>
          <input type="submit" value="Search"></input>
        </form>
      </div>
    </div>
  );
}
