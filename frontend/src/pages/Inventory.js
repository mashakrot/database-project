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


  const fetchSupplier = async (itemValue, searchType) => {
    const data = searchType === "id" ? { itemid: itemValue } : { itemname: itemValue };
  
    try {
      const response = await fetch("http://localhost:5000/get_supplier_by_itemname", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
  
      const result = await response.json();
      const supplierField = document.getElementById("supplierData");
  
      if (result.status === "success") {
        const supplier = result.supplier;
        supplierField.value = `Name: ${supplier[0]}, Phone: ${supplier[1]}, Email: ${supplier[2]}`;
      } else {
        supplierField.value = "No supplier found.";
      }
    } catch (error) {
      console.error("Error fetching supplier:", error);
      document.getElementById("supplierData").value = "Error fetching supplier data.";
    }
  };

  const handleTrimmedSubmit = (event, inputId, searchType) => {
    event.preventDefault();
    const inputElement = document.getElementById(inputId);
    const trimmedValue = inputElement.value.trim();
    inputElement.value = trimmedValue;
    if (trimmedValue) {
      fetchSupplier(trimmedValue, searchType);
    }
  };




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
        <form id="formItemID" onSubmit={(e) => handleTrimmedSubmit(e, "itemid", "id")}>
          <label htmlFor="itemid">Search by item ID:</label>
          <input type="text" id="itemid" name="itemid"/>
          <input type="submit" value="Search"></input>
        </form>
        <form id="formItemName" onSubmit={(e) => handleTrimmedSubmit(e, "itemname", "name")}>
          <label htmlFor="itemname">Search by item name:</label>
          <input type="text" id="itemname" name="itemname"/>
          <input type="submit" value="Search"></input>
        </form>
        <label htmlFor="supplierData">Supplier Info:</label>
        <input type="text" id="supplierData" readOnly />
      </div>
    </div>
  );
}
