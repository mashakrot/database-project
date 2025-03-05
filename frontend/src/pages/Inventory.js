import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import '../css/Inventory.css'; 

const sanitizeWhitespace = (html) => {
  return html.replace(/>\s+</g, '><').trim();  
};

export default function Inventory() {
  const [inventory, setInventory] = useState([]);

  const [orderedQuantity, setOrderedQuantity] = useState(0);
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const response = await fetch("http://localhost:5000/get_inventory", { 
          method: "POST",
        });
        const data = await response.json();
        if (data.status === "success") {
          const sortedInventory = data.inventory.sort((a, b) => a[0] - b[0]); 
          setInventory(sortedInventory);
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

  const handleUpdateQuantity = () => {
    if (!searchValue) {
      alert("Please enter the item name.");
      return;
    }
  
    const updatedInventory = inventory.map(item => {
      if (item[1].toLowerCase() === searchValue.toLowerCase()) {  
        const newQuantity = item[2] + orderedQuantity;  
        fetch("http://localhost:5000/update_inventory", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            itemName: searchValue,  
            orderedQuantity: orderedQuantity,  
          }),
        })
          .then(response => response.json())
          .then(data => {
            if (data.status === "success") {
              const sortedInventory = data.updatedInventory.sort((a, b) => a[0] - b[0]);
              setInventory(sortedInventory);  
              alert("Inventory updated successfully!");
            } else {
              alert("Error updating inventory: " + data.message);
            }
          })
          .catch((error) => {
            console.error("Error updating inventory:", error);
            alert("Error updating inventory.");
          });
      }
      return item;
    });
  };

  return (
    <div className="flex inventory-container">
      <Sidebar />
      <div className="flex-1 ml-60 p-5">
        <div className="po-6 w-full">
          <h1 className="text-2xl font-bold">Inventory Management</h1>
          <h2 className="font-bold mb-3">Update Inventory</h2>
          <div className="update-container">
            <div>
              <label htmlFor="itemname1">Item Name:</label>
              <input
                type="text"
                id="itemname1"
                name="itemname1"
                placeholder="Enter item name to update"
                value={searchValue}  
                onChange={(e) => setSearchValue(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="orderedQuantity">Ordered Quantity:</label>
              <input
                type="number"
                id="orderedQuantity"
                name="orderedQuantity"
                placeholder="Enter quantity to add"
                value={orderedQuantity}
                onChange={(e) => setOrderedQuantity(Number(e.target.value))}
              />
            </div>
            
            <button className="btn" id="btn-update" onClick={handleUpdateQuantity}>Update Inventory</button>
          </div>
          <h2 className="font-bold mb-3">Inventory List</h2>
          <table id="inventory-table"> 
            <thead>
              <tr>
                <th>Item ID</th>
                <th>Name</th>
                <th>Quantity</th>
                <th>Supplier ID</th>
                <th>Reorder Level</th>
              </tr>
            </thead>
            <tbody>
              {inventory.map(item => (
                <tr key={item[0]}>
                  <td>{item[0]}</td>
                  <td>{item[1]}</td>
                  <td>{item[2]}</td>
                  <td>{item[3]}</td>
                  <td>{item[4]}</td>
                </tr>
              ))}
            </tbody>
          </table>


          <h2 className="font-bold mb-3 mt-3">Search information about Suppliers</h2>
          <div className="search-container">
            <form id="formItemID" onSubmit={(e) => handleTrimmedSubmit(e, "itemid", "id")}>
              <label htmlFor="itemid">Search by item ID:</label>
              <input type="text" id="itemid" name="itemid"/>
              <button className="btn">Search</button>
            </form>

            <form id="formItemName" onSubmit={(e) => handleTrimmedSubmit(e, "itemname", "name")}>
              <label htmlFor="itemname">Search by item name:</label>
              <input type="text" id="itemname" name="itemname"/>
              <button className="btn">Search</button>
            </form>
          </div>
          <label htmlFor="supplierData">Supplier Info:</label>
          <input type="text" id="supplierData" readOnly />
        </div>
        </div>
      </div>
  );
}
