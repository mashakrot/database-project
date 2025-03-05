/* global $ */

async function fetchAndPopulateTable() {
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/get_reservations", 
        success: function(response) {
            if (response.status === "success") {
                let reservations = response.reservations;
                let tableBody = $("#reservations-table tbody"); 
                
                reservations.forEach(item => {
                    let row = "<tr>";
                    row += `<td>${item[0]}</td>`;
                    row += `<td>${item[1]}</td>`;
                    row += `<td>${item[2]}</td>`;
                    row += `<td>${item[3]}</td>`;
                    row += `<td>${item[4]}</td>`;
                    row += `<td>${item[5]}</td>`;
                    row += "</tr>";

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