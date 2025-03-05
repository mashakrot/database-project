import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import '../css/Inventory.css'; 


export default function Inventory() {
  const [inventory, setInventory] = useState([]);

  const [orderedQuantity, setOrderedQuantity] = useState(0);
  const [price, setPrice] = useState(0);
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    // Fetch data from the Flask backend
    const fetchInventory = async () => {
      try {
        const response = await fetch("http://localhost:5000/get_inventory", { // Adjust URL
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
    // Ensure searchValue (itemname) is not empty
    if (!searchValue) {
      alert("Please enter the item name.");
      return;
    }
  
    // Check if item exists in the inventory list based on itemname
    const updatedInventory = inventory.map(item => {
      if (item[1].toLowerCase() === searchValue.toLowerCase()) {  // item[1] is itemname
        const newQuantity = item[2] + orderedQuantity;  // Update the quantity based on orderedQuantity
        // Send a request to the backend to update the inventory
        fetch("http://localhost:5000/update_inventory", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            itemName: searchValue,  // Send the item name to backend
            orderedQuantity: orderedQuantity,  // Send the ordered quantity
            price: price,  // Send the price (optional, if you're updating the price as well)
          }),
        })
          .then(response => response.json())
          .then(data => {
            if (data.status === "success") {
              const sortedInventory = data.updatedInventory.sort((a, b) => a[0] - b[0]);
              setInventory(sortedInventory);  // Update the inventory with the backend data
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
        <div className="p-6 w-full">
          <h1 className="text-2xl font-bold">Inventory Management</h1>
          <h2 className="font-bold mb-3">Update Inventory</h2>
          <div className="update-container">
            <div>
              <label htmlFor="itemname">Item Name:</label>
              <input
                type="text"
                id="itemname"
                name="itemname"
                placeholder="Enter item name to update"
                value={searchValue}  
                onChange={(e) => setSearchValue(e.target.value)}
              />
            </div>
            <div>
              <label for="orderedQuantity">Ordered Quantity:</label>
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


          <h2 className="font-bold mb-3 mt-3">Search information about Suppliers</h2>
          <div className="search-container">
            <form id="formItemID" onSubmit={(e) => handleTrimmedSubmit(e, "itemid", "id")}>
              <label htmlFor="itemid">Search by item ID:</label>
              <input type="text" id="itemid" name="itemid"/>
              {/* <input type="submit" id="button" value="Search"></input> */}
              <button className="btn">Search</button>
            </form>

            <form id="formItemName" onSubmit={(e) => handleTrimmedSubmit(e, "itemname", "name")}>
              <label htmlFor="itemname">Search by item name:</label>
              <input type="text" id="itemname" name="itemname"/>
              {/* <input type="submit" value="Search"></input> */}
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
