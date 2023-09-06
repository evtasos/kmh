/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function printBarcode(barcode) {
    // Create a new window
    var newWindow = window.open("", "Print Ticket", "width=500,height=500");

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
            <p>Ο ΑΡΙΘΜΟΣ ΔΕΝ ΑΝΤΙΣΤΟΙΧΕΙ</p>
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
    }, 1000); // Adjust the delay (in milliseconds) as needed
}


// function printBarcode(barcode) {
// // Create a new window
// var newWindow = window.open("", "Print Ticket", "width=500,height=500");
// // Write the content to the new window with text-align: center and line-height: 150px
// newWindow.document.write(`<p style="text-align: center;">Your ticket is:</p><p style="text-align: center; ">${barcode}</p><p style="text-align: center; font-size: 8px;">Thank you!</p>`);
// newWindow.document.title = "Print Ticket";
// // Print the new window
// newWindow.print();
// // Close the new window
// newWindow.close();
// }

function issueTicket() {
    const printOption = document.getElementById('printTicket').checked;
    fetch('/issue-number')
        .then(response => response.json())
        .then(data => {
            var barcode = data.barcode;
            const resultMessage = document.getElementById('resultMessage');
            resultMessage.innerText = `New ticket issued: ${data.barcode}`;

            // Show the message container
            const messageContainer = document.querySelector('.message-container');
            messageContainer.style.display = 'block';

            //print(data.barcode)
            if (printOption){
                printBarcode(barcode);
            }

            setTimeout(function() {
            location.reload(); // Refresh the page after a certain duration
        }, 1000); // Refresh after 1 seconds (1000 milliseconds)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function assignToOffice() {
    const barcodeSelect = document.getElementById('barcodeSelect');
    const officeSelect = document.getElementById('officeSelect');
    const barcode = barcodeSelect.value;
    const officeNumber = officeSelect.value;

    fetch('/assign-office', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            barcode: barcode,
            office_number: officeNumber
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerText = data.message;
        // Show the message container
        const messageContainer = document.querySelector('.message-container');
        messageContainer.style.display = 'block';
        setTimeout(function() {
            location.reload(); // Refresh the page after a certain duration
        }, 1000); // Refresh after 1 seconds (5000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function proceedToChemo() {
    const chemoSelect = document.getElementById('chemoSelect');
    const barcode = chemoSelect.value;

    const eligibleYes = document.getElementById('eligibleYes');
    const eligibleNo = document.getElementById('eligibleNo');
    const eligibleStatus = eligibleYes.checked ? true : false;

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
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerText = data.message;
        // Show the message container

        const messageContainer = document.querySelector('.message-container');
        messageContainer.style.display = 'block';
        
        setTimeout(function() {
            location.reload(); // Refresh the page after a certain duration
        }, 1000); // Refresh after 5 seconds (5000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function proceedToTreatment() {
    const roomSelect = document.getElementById('roomSelect');
    const roomNumber = roomSelect.value;

    const chemoBarcodeSelect = document.getElementById('chemoBarcodeSelect');
    const barcode = chemoBarcodeSelect.value;

    fetch('/assign-treatment-room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            room_number: roomNumber,
            barcode: barcode
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultMessage = document.getElementById('resultMessage');
        if (data.barcode) {
            resultMessage.innerText = `Proceeded to Treatment Room ${roomNumber}. Barcode: ${data.barcode}`;
            // Show the message container
            const messageContainer = document.querySelector('.message-container');
            messageContainer.style.display = 'block';
        } 
        else {
            resultMessage.innerText = `No patient available in the Chemo Waiting Pool.`;
            // Show the message container
            const messageContainer = document.querySelector('.message-container');
            messageContainer.style.display = 'block';
        }
        setTimeout(function() {
            location.reload(); // Refresh the page after a certain duration
        }, 1000); // Refresh after 5 seconds (5000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function removeBarcode() {
    const barcodeInput = document.getElementById('removeBarcodeInput');
    const barcode = barcodeInput.value;

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
        const resultMessage = document.getElementById('resultMessage');
        if (data.message) {
            resultMessage.innerText = data.message;
            // Show the message container
            const messageContainer = document.querySelector('.message-container');
            messageContainer.style.display = 'block';
        } else {
            resultMessage.innerText = 'Error: Barcode not found';
            // Show the message container
            const messageContainer = document.querySelector('.message-container');
            messageContainer.style.display = 'block';
        }
        setTimeout(function() {
            location.reload(); // Refresh the page after a certain duration
        }, 1000); // Refresh after 5 seconds (5000 milliseconds)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function confirmAction() {
    
    if (confirm("Are you sure you want to perform this action?")) {
        // User confirmed, perform the action
        fetch('/reset')
        setTimeout(function() {
            location.reload(); // Refresh the page after a certain duration
        }, 1000); // Refresh after 5 seconds (5000 milliseconds)
    } else {
        // User canceled, do nothing
    }
}