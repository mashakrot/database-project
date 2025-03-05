async function fetchAndPopulateTable() {
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/get_inventory", // Adjust URL to match Flask backend
        success: function(response) {
            if (response.status === "success") {
                let inventory = response.inventory;
                let tableBody = $("#inventory-table tbody"); // Get the table body element

                // Loop through each inventory item and create a row
                inventory.forEach(item => {
                    // Assuming item is a tuple or array like [id, name, description, quantity, price]
                    let row = "<tr>";
                    row += `<td>${item[0]}</td>`;  // Item ID
                    row += `<td>${item[1]}</td>`;  // Name
                    row += `<td>${item[2]}</td>`;  // Description
                    row += `<td>${item[3]}</td>`;  // Quantity
                    row += `<td>${item[4]}</td>`;  // Price
                    row += "</tr>";

                    // Append the row to the table
                    tableBody.append(row);
                });
            } else {
                console.log("Error:", response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}

document.addEventListener('DOMContentLoaded', fetchAndPopulateTable);






async function fetchSupplier(itemValue, searchType) {
    const data = searchType === "id" ? { itemid: itemValue } : { itemname: itemValue };

    $.ajax({
        type: "POST",
        url: "http://localhost:5000/get_supplier_by_itemname", // Adjust URL to match Flask backend
        contentType: 'application/json', // Set content type to JSON
        data: JSON.stringify(data), // Send data as JSON string
        success: function(response) {
            console.log("Response:", response); // DELETE
            let supplierField = $("#supplierData");

            if (response.status === "success") {
                let supplier = response.supplier;
                let supplierInfo = `Name: ${supplier[0]}, Phone: ${supplier[1]}, Email: ${supplier[2]}`;
                supplierField.val(supplierInfo);
            } else {
                supplierField.val("No supplier found.");
                console.log("Error:", response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
            $("#supplierData").val("Error fetching supplier data.");
        }
    });
}

$(document).ready(function() {
    $("#formItemID").on("submit", function(event) {
      event.preventDefault();
      let itemId = $("#itemid").val().trim();
      $("#itemid").val(itemId);
      if (itemId) fetchSupplier(itemId, "id");
    });
  
    $("#formItemName").on("submit", function(event) {
      event.preventDefault();
      let itemName = $("#itemname").val().trim();
      $("#itemname").val(itemName);
      if (itemName) fetchSupplier(itemName, "name");
    });
  });