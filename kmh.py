from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['DEBUG'] = False

# Counter for generating patient numbers
patient_counter = 1

# Placeholder lists to store patient data
issued_numbers = []
office_pool = []
assigned_offices = {'Γραφείο1': [], 'Γραφείο2': [],'Αιματολογικό': []}
treatment_waiting_pool = []
treatment_rooms = {1: [], 2: [], 3: [],4: [], 5: [], 6: [], 7: [], 8: []}

@app.route('/issue-number')
def issue_number():
    global patient_counter
    barcode = 'A' + str(patient_counter)

    # Check if the barcode already exists in any other pool
    while barcode in office_pool or any(barcode in barcodes for barcodes in assigned_offices.values()) or barcode in treatment_waiting_pool or any(barcode in barcodes for barcodes in treatment_rooms.values()):
        patient_counter += 1
        barcode = 'A' + str(patient_counter)

    issued_numbers.append(barcode)
    office_pool.append(barcode)
    return jsonify({'barcode': barcode})

@app.route('/assign-office', methods=['POST'])
def assign_office():
    try:
        barcode = request.json['barcode']
        office_number = request.json['office_number']
        if barcode in office_pool:
            office_pool.remove(barcode)
            assigned_offices[office_number].append(barcode)
            return jsonify({'message': f'Patient with barcode {barcode} assigned to office {office_number}.'})
        return jsonify({'message': 'Barcode not found in the office pool.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response

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
    
@app.route('/assign-treatment-room', methods=['POST'])
def assign_treatment_room():
    try:    
        room_number = int(request.json['room_number'])
        barcode = request.json['barcode']

        if barcode in treatment_waiting_pool:
            treatment_rooms[room_number].append(barcode)
            treatment_waiting_pool.remove(barcode)
            return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} assigned to treatment room {room_number}.'})
        return jsonify({'message': 'Barcode not found in the Chemo Waiting Pool.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response
    
@app.route('/rmv-barcode', methods=['POST'])
def remove_barcode():
    try:
        barcode = request.json['barcode']

        if barcode in office_pool:
            office_pool.remove(barcode)
            return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left office'})
        for office_number, barcodes in assigned_offices.items():
            if barcode in barcodes:
                barcodes.remove(barcode)
                return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left offices'})
        for room_number, barcodes in treatment_rooms.items():
            if barcode in barcodes:
                barcodes.remove(barcode)
                return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left treatment'})
        if barcode in treatment_waiting_pool:
            treatment_waiting_pool.remove(barcode)
            return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} left chemo pool'})
        return jsonify({'message': 'Barcode not found '}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response
    
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
        if destination == 'office_pool':
            office_pool.append(ticket)
            return jsonify({'message': f'Ticket {ticket} imported to Office Pool.'})
        if destination == 'treatment_waiting_pool':
            treatment_waiting_pool.append(ticket)
            return jsonify({'message': f'Ticket {ticket} imported to Treatmet Waiting Pool.'})
        return jsonify({'message': 'Invalid destination.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle exceptions and return an error response
    
@app.route('/office-pool')
def get_office_pool():
    return jsonify({'office_pool': office_pool})

@app.route('/assigned-offices')
def get_assigned_offices():
    return jsonify({'assigned_offices': assigned_offices})

@app.route('/chemo-waiting-pool')
def get_chemo_waiting_pool():
    return jsonify({'chemo_waiting_pool': treatment_waiting_pool})

@app.route('/treatment-rooms')
def get_treatment_rooms():
    return jsonify({'treatment_rooms': treatment_rooms})

@app.route('/pools')
def view_pools():
    office_numbers = sorted(assigned_offices.keys())
    return render_template('nurses.html', office_pool=office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)
@app.route('/pools2')
def view_pools3():
    office_numbers = sorted(assigned_offices.keys())
    return render_template('doctors.html', office_pool=office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)

@app.route('/pools3')
def view_pools2():
    office_numbers = sorted(assigned_offices.keys())
    return render_template('nursesdb.html', office_pool=office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)

@app.route('/numbers')
def view_numbers():
    return jsonify({'issued_numbers': issued_numbers})


@app.route('/reset')
def reset():
    global patient_counter
    patient_counter = 1
    issued_numbers.clear()
    office_pool.clear()
    global assigned_offices
    assigned_offices = {'Γραφείο1': [], 'Γραφείο2': [], 'Αιματολογικό': []}
    treatment_waiting_pool.clear()
    global treatment_rooms
    treatment_rooms = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    return jsonify({'message': 'System reset successfully.'})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')