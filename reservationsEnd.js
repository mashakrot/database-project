async function fetchAndPopulateTable() {
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/get_reservations", // Adjust URL to match Flask backend
        success: function(response) {
            if (response.status === "success") {
                let reservations = response.reservations;
                let tableBody = $("#reservations-table tbody"); // Get the table body element

                // Loop through each reservations item and create a row
                reservations.forEach(item => {
                    // Assuming item is a tuple or array like [id, name, description, quantity, price]
                    let row = "<tr>";
                    row += `<td>${item[0]}</td>`;  // Reservation ID
                    row += `<td>${item[1]}</td>`;  // Table ID
                    row += `<td>${item[2]}</td>`;  // customer name
                    row += `<td>${item[3]}</td>`;  // Telephone number
                    row += `<td>${item[4]}</td>`; // Status
                    row += `<td>${item[5]}</td>`;  // Timeslot
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