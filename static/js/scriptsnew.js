/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/

// This file is intentionally blank
// Use this file to add JavaScript to your project

// Function to print a barcode
function printBarcode(barcode) {
    // Create a new window
    var newWindow = window.open("", "Print Ticket", "width=800,height=800");

    // Add the print-specific styles to the new window
    var cssLink = document.createElement("link");
    cssLink.href = "print-styles.css"; // Adjust the path to your CSS file
    cssLink.rel = "stylesheet";
    cssLink.type = "text/css";
    newWindow.document.head.appendChild(cssLink);

    // Define your custom message as HTML
    var customMessage = `
        <div style="text-align: center;">
            <p>-------------------------------</p>
            <p>Γ.Α.Ν.Π. ΜΕΤΑΞΑ</p>
            <p>ΜΟΝΑΔΑ ΗΜΕΡΗΣΙΑΣ<br>ΝΟΣΗΛΕΙΑΣ</p>
            <p>Ο ΑΡΙΘΜΟΣ ΔΕΝ ΑΝΤΙΣΤΟΙΧΕΙ ΣΕ ΣΕΙΡΑ ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ</p>
            <p style="font-size: 24px;">${barcode}</p> <!-- Change the font-size here -->
            <p>-------------------------------</p>
        </div>
    `;

    // Write the custom message to the new window
    newWindow.document.write(customMessage);

    newWindow.document.title = "Print Ticket";

    // Add a delay to allow content to load before printing
    setTimeout(function () {
        // Print the new window
        newWindow.print();

        // Close the new window
        newWindow.close();
    }, 3000); // Adjust the delay (in milliseconds) as needed
}

// Function to issue a ticket
async function issueTicket() {
    // Check if the "Print Ticket" checkbox is checked
    const printOption = document.getElementById('printTicket').checked;
    // Get the number of tickets from the input field
    const numTickets = parseInt(document.getElementById('numTickets').value);

    try {
        const barcodes = [];
    
        for (let i = 0; i < numTickets; i++) {
          const response = await fetch('/issue-number');
          const data = await response.json();
          const barcode = data.barcode;
          barcodes.push(barcode);
        }
    
        // Create formatted ticket content (HTML structure)
        let ticketData = `<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Tickets</title>
      <style>
        /* Add your desired CSS styles for formatting tickets here */
      </style>
    </head>
    <body>`;
    
        for (const barcode of barcodes) {
          ticketData += `
          <div class="ticket">
            <p>-------------------------------</p>
            <p>Γ.Α.Ν.Π. ΜΕΤΑΞΑ</p>
            <p>ΜΟΝΑΔΑ ΗΜΕΡΗΣΙΑΣ<br>ΝΟΣΗΛΕΙΑΣ</p>
            <p>Ο ΑΡΙΘΜΟΣ ΔΕΝ ΑΝΤΙΣΤΟΙΧΕΙ ΣΕ ΣΕΙΡΑ ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ</p>
            <p>${barcode}</p> <p>-------------------------------</p>
          </div>
          `;
        }
    
        ticketData += `</body></html>`;
    
        // Open a print dialog
        const printWindow = window.open("", "PRINT");
        printWindow.document.write(ticketData);
        printWindow.document.close(); // Important for print functionality
        //printWindow.focus(); // Necessary for some browsers
        printWindow.print(); // Trigger print dialog
        // Delay closing the window after a short timeout (adjust as needed)
        setTimeout(function() {
        printWindow.close();
      }, 500);  // Adjust timeout in milliseconds
        // ... reload the page (optional)
        setTimeout(function () {
                            location.reload();
                        }, 1000); // Refresh after 1 second

      } catch (error) {
        console.error('Error:', error);
      }
    }

// Function to assign tickets to an office
function assignToOffice() {
    // Get selected barcodes and office number from the form
    const barcodeSelect = document.getElementById('barcodeSelect');
    const officeSelect = document.getElementById('officeSelect');
    const selectedOptions = Array.from(barcodeSelect.selectedOptions);
    const selectedBarcodes = selectedOptions.map(option => option.value);
    const officeNumber = officeSelect.value;

    // Send a POST request to the server to assign tickets
    fetch('/assign-office', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            barcodes: selectedBarcodes,
            office_number: officeNumber
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update the result message
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerText = data.message;

        // Show the message container
        const messageContainer = document.querySelector('.message-container');
        messageContainer.style.display = 'block';

        // Reset the select elements
        const officeSelect = document.getElementById('officeSelect');
        officeSelect.selectedIndex = 0;
        const barcodeSelect = document.getElementById('barcodeSelect');
        barcodeSelect.selectedIndex = 0;

        // Refresh the page after a certain duration
        setTimeout(function () {
            location.reload();
        }, 1000); // Refresh after 1 second (1000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to proceed to chemo
function proceedToChemo() {
    // Get selected barcode and eligibility status from the form
    const chemoSelect = document.getElementById('chemoSelect');
    const barcode = chemoSelect.value;
    const eligibleYes = document.getElementById('eligibleYes');
    const eligibleNo = document.getElementById('eligibleNo');
    const eligibleStatus = eligibleYes.checked ? true : false;

    // Send a POST request to the server to proceed to chemo
    fetch('/add-to-chemo-waiting', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            barcode: barcode,
            status: eligibleStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update the result message
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerText = data.message;

        // Show the message container
        const messageContainer = document.querySelector('.message-container');
        messageContainer.style.display = 'block';

        // Reset the select element
        const chemoSelect = document.getElementById('chemoSelect');
        chemoSelect.selectedIndex = 0;

        // Refresh the page after a certain duration
        setTimeout(function () {
            location.reload();
        }, 1000); // Refresh after 1 second (1000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to proceed to treatment
function proceedToTreatment() {
    // Get selected room number and chemo barcodes from the form
    const roomSelect = document.getElementById('roomSelect');
    const roomNumber = roomSelect.value;
    const chemoBarcodeSelect = document.getElementById('chemoBarcodeSelect');
    const selectedOptions = Array.from(chemoBarcodeSelect.selectedOptions);
    const selectedBarcodes = selectedOptions.map(option => option.value);

    // Send a POST request to the server to assign treatment rooms
    fetch('/assign-treatment-room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            room_number: roomNumber,
            barcodes: selectedBarcodes
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update the result message
        const resultMessage = document.getElementById('resultMessage');
        if (data.barcodes.length > 0) {
            resultMessage.innerText = `Proceeded to Treatment Room ${roomNumber}. Barcode: ${data.barcodes}`;
        } else {
            resultMessage.innerText = `No patient available in the Chemo Waiting Pool.`;
        }

        // Show the message container
        const messageContainer = document.querySelector('.message-container');
        messageContainer.style.display = 'block';

        // Reset the select elements
        const roomSelect = document.getElementById('roomSelect');
        roomSelect.selectedIndex = 0;
        const chemoBarcodeSelect = document.getElementById('chemoBarcodeSelect');
        chemoBarcodeSelect.selectedIndex = -1;

        // Refresh the page after a certain duration
        setTimeout(function () {
            location.reload();
        }, 1000); // Refresh after 1 second (1000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function for treatment complete
function treatmentcomplete() {
    // Get the barcode input value
    const trtmntroomSelect = document.getElementById('trtmntroomSelect')
    const barcode = trtmntroomSelect.value;
    if (barcode.trim() === "") {
        alert("Please enter a ticket number.");
        return;
    }
    // Send a POST request to the server to remove a barcode
    fetch('/treatment-completion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            barcode: barcode
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display a message to the user.
        trtmntroomSelect.value = ''; // Clear the input field.

        // Refresh the page after a certain duration
        setTimeout(function () {
            location.reload();
        }, 1000); // Refresh after 1 second (1000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
// Function to remove a barcode
function removeBarcode() {
    // Get the barcode input value
    const barcodeInput = document.getElementById('removeBarcodeSelect');
    const barcode = barcodeInput.value;

    if (barcode.trim() === "") {
        alert("Please enter a ticket number.");
        return;
    }

    // Send a POST request to the server to remove a barcode
    fetch('/rmv-barcode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            barcode: barcode
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display a message to the user.
        barcodeInput.value = ''; // Clear the input field.

        // Refresh the page after a certain duration
        setTimeout(function () {
            location.reload();
        }, 1000); // Refresh after 1 second (1000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to import a ticket
function importTicket() {
    // Get ticket and destination values from the form
    const ticketInput = document.getElementById("importTicketInput");
    const destinationSelect = document.getElementById("importDestinationSelect");

    const ticket = ticketInput.value;
    const destination = destinationSelect.value;

    if (ticket.trim() === "") {
        alert("Please enter a ticket number.");
        return;
    }

    // Send a POST request to the server to handle the import action
    fetch('/import-ticket', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ticket: ticket,
            destination: destination,
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display a message to the user.
        ticketInput.value = ''; // Clear the input field.

        // Refresh the page after a certain duration
        setTimeout(function () {
            location.reload();
        }, 1000); // Refresh after 1 second (1000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
// Function to get stats
function showstats() {
    fetch('/numbers')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("total_patients").innerText = data.total_patients;
        document.getElementById("treated_patients").innerText = data.treated_patients;
        document.getElementById("treated_percentage").innerText = data.treated_percentage;
    })
    .catch(error => console.error('Error fetching statistics:', error));
}

// Function to confirm an action
function confirmAction() {
    if (confirm("Are you sure you want to perform this action?")) {
        // User confirmed, perform the action
        fetch('/reset');
        setTimeout(function () {
            location.reload(); // Refresh the page after a certain duration
        }, 1000); // Refresh after 1 second (1000 milliseconds)
    } else {
        // User canceled, do nothing
    }
}
