from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

# Initialize a patient counter
patient_counter = 1
treated_patients = 0
# Lists to store patient data
issued_numbers = []
office_pool = []
assigned_offices = {'Γραφείο1': [], 'Γραφείο2': [], 'Αιματολογικό': []}
treatment_waiting_pool = []
treatment_rooms = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

# Route to issue a new patient number (barcode)
@app.route('/issue-number')

def issue_number():
    global patient_counter
    barcode = 'A' + str(patient_counter)

    # Check if the barcode already exists in any pool
    while barcode in office_pool or any(barcode in barcodes for barcodes in assigned_offices.values()) or barcode in treatment_waiting_pool or any(barcode in barcodes for barcodes in treatment_rooms.values()):
        patient_counter += 1
        barcode = 'A' + str(patient_counter)

    # Add the generated barcode to the issued numbers list and office pool
    issued_numbers.append(barcode)
    office_pool.append(barcode)
    return jsonify({'barcode': barcode})

# Route to assign patients to an office
@app.route('/assign-office', methods=['POST'])

def assign_office():
    try:
        barcodes = request.json['barcodes']
        office_number = request.json['office_number']

        # Check if a doctor's office is selected and valid
        if office_number not in assigned_offices:
            return jsonify({'message': f'Δεν επιλέχθηκε γραφείο ιατρού'}), 400
        
        # Loop through the list of barcodes and process each one
        for barcode in barcodes:
            if barcode in office_pool:
                office_pool.remove(barcode)
                assigned_offices[office_number].append(barcode)
            else:
                # Handle cases where a barcode is not found
                return jsonify({'message': f'Barcode {barcode} not found in the office pool.'}), 404

        return jsonify({'message': f'Successfully assigned {len(barcodes)} barcode(s) to office {office_number}.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response

# Route to move patients to the chemo waiting pool
@app.route('/add-to-chemo-waiting', methods=['POST'])

def add_to_chemo_waiting():
    try:
        barcode = request.json['barcode']
        eligible = request.json['status']

        for office_number, barcodes in assigned_offices.items():
            if barcode in barcodes:
                barcodes.remove(barcode)
                if eligible:
                    treatment_waiting_pool.append(barcode)
                    return jsonify({'message': f'Patient with barcode {barcode} added to chemo waiting pool. Removed from office {office_number}.'})
                else:
                    return jsonify({'message': f'Patient with barcode {barcode} is not eligible for chemo. Removed from office {office_number}.'})

        return jsonify({'message': 'Barcode not found in the assigned offices.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response

# Route to assign patients to a treatment room
@app.route('/assign-treatment-room', methods=['POST'])

def assign_treatment_room():
    #global treated_patients
    try:
        room_number = int(request.json['room_number'])
        barcodes = request.json['barcodes']
        assigned_barcodes = []

        for barcode in barcodes:
            if barcode in treatment_waiting_pool:
                treatment_rooms[room_number].append(barcode)
                treatment_waiting_pool.remove(barcode)
                assigned_barcodes.append(barcode)
                #treated_patients += 1

        if assigned_barcodes:
            return jsonify({'barcodes': assigned_barcodes, 'message': f'Patients assigned to treatment room {room_number}.'})
        return jsonify({'barcodes': [], 'message': 'No patients found in the Chemo Waiting Pool.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response

# Route to remove patients from various pools
@app.route('/rmv-barcode', methods=['POST'])

def remove_barcode():
    try:
        barcode = request.json['barcode']

        if barcode in office_pool:
            office_pool.remove(barcode)
            issued_numbers.remove(barcode)
            return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left office'})

        for office_number, barcodes in assigned_offices.items():
            if barcode in barcodes:
                barcodes.remove(barcode)
                issued_numbers.remove(barcode)
                return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left offices'})

        for room_number, barcodes in treatment_rooms.items():
            if barcode in barcodes:
                barcodes.remove(barcode)
                issued_numbers.remove(barcode)
                return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left treatment'})

        if barcode in treatment_waiting_pool:
            treatment_waiting_pool.remove(barcode)
            issued_numbers.remove(barcode)
            return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left chemo pool'})

        return jsonify({'message': 'Barcode not found '}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response

# Route to import a patient ticket to a pool
@app.route('/import-ticket', methods=['POST'])

def import_ticket():
    try:
        data = request.json
        ticket = data['ticket']
        destination = data['destination']

        if ticket in office_pool:
            return jsonify({'message': f'Ticket {ticket} already exists.'})

        if ticket in treatment_waiting_pool:
            return jsonify({'message': f'Ticket {ticket} already exists.'})

        # Add the ticket to issued_numbers before adding to destination pool
        issued_numbers.append(ticket)
        
        if destination == 'office_pool':
            office_pool.append(ticket)
            return jsonify({'message': f'Ticket {ticket} imported to Office Pool.'})

        if destination == 'treatment_waiting_pool':
            treatment_waiting_pool.append(ticket)
            return jsonify({'message': f'Ticket {ticket} imported to Treatment Waiting Pool.'})

        return jsonify({'message': 'Invalid destination.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response
@app.route('/issued-numbers')
def get_issued_numbers():
    return jsonify({'issued_numbers': issued_numbers})
# Route to get the office pool
@app.route('/office-pool')
def get_office_pool():
    return jsonify({'office_pool': office_pool})

# Route to get the assigned offices
@app.route('/assigned-offices')
def get_assigned_offices():
    return jsonify({'assigned_offices': assigned_offices})

# Route to get the chemo waiting pool
@app.route('/chemo-waiting-pool')
def get_chemo_waiting_pool():
    return jsonify({'chemo_waiting_pool': treatment_waiting_pool})

# Route to get the treatment rooms
@app.route('/treatment-rooms')
def get_treatment_rooms():
    return jsonify({'treatment_rooms': treatment_rooms})

# Route to render the start page
@app.route('/')
def start():
    return render_template('buttons.html')

# Routes to render various pool views
@app.route('/nurses')
def view_pools():
    office_numbers = sorted(assigned_offices.keys())
    sorted_office_pool = sorted(office_pool, key=lambda x: int(x[1:]))
    return render_template('nurses.html', office_pool=sorted_office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)

@app.route('/doctors')
def view_pools2():
    office_numbers = sorted(assigned_offices.keys())
    return render_template('doctors.html', office_pool=office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)

@app.route('/patients')
def view_pools3():
    office_numbers = sorted(assigned_offices.keys())
    return render_template('patients.html', office_pool=office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)

# Route to get the list of issued patient numbers
@app.route('/numbers')
def view_numbers():
    # Get the total number of patients
    total_patients = len(issued_numbers)

    # Calculate the percentage of treated patients
    #treated_percentage = round(treated_patients / total_patients, 2)*100 + "%"
    if total_patients != 0:
        treated_percentage = round((treated_patients / total_patients) * 100, 2)
        treated_percentage = str(treated_percentage) + "%"
    else:
        treated_percentage = "0%"

    return {
        "total_patients": total_patients,
        "treated_patients": treated_patients,
        "treated_percentage": treated_percentage,
    }

# Route for patient chemo treatment completion
@app.route('/treatment-completion', methods=['POST'])
def treatment_completion():
    global treated_patients
    try:
        barcode = request.json['barcode']
        for room_number, barcodes in treatment_rooms.items():
            if barcode in barcodes:
                barcodes.remove(barcode)
                treated_patients += 1
                return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left treatment'})

        return jsonify({'message': 'Barcode not found '}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response


# Route to reset the system
@app.route('/reset')
def reset():
    global patient_counter
    patient_counter = 1
    global treated_patients
    treated_patients = 0
    issued_numbers.clear()
    office_pool.clear()
    global assigned_offices
    assigned_offices = {'Γραφείο1': [], 'Γραφείο2': [], 'Αιματολογικό': []}
    treatment_waiting_pool.clear()
    global treatment_rooms
    treatment_rooms = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    return jsonify({'message': 'System reset successfully.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
