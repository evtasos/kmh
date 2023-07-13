from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

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
    patient_counter += 1
    issued_numbers.append(barcode)
    office_pool.append(barcode)
    return jsonify({'barcode': barcode})

@app.route('/assign-office', methods=['POST'])
def assign_office():
    barcode = request.json['barcode']
    office_number = request.json['office_number']
    if barcode in office_pool:
        office_pool.remove(barcode)
        assigned_offices[office_number].append(barcode)
        return jsonify({'message': f'Patient with barcode {barcode} assigned to office {office_number}.'})
    return jsonify({'message': 'Barcode not found in the office pool.'}), 404

@app.route('/add-to-chemo-waiting', methods=['POST'])
def add_to_chemo_waiting():
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

@app.route('/assign-treatment-room', methods=['POST'])
def assign_treatment_room():
    room_number = int(request.json['room_number'])
    barcode = request.json['barcode']

    if barcode in treatment_waiting_pool:
        treatment_rooms[room_number].append(barcode)
        treatment_waiting_pool.remove(barcode)
        return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} assigned to treatment room {room_number}.'})
    return jsonify({'message': 'Barcode not found in the Chemo Waiting Pool.'}), 404

@app.route('/rmv-barcode', methods=['POST'])
def remove_barcode():
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
    return render_template('test.html', office_pool=office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)

@app.route('/pools2')
def view_pools2():
    office_numbers = sorted(assigned_offices.keys())
    return render_template('poolsbare.html', office_pool=office_pool, assigned_offices=assigned_offices,
                           chemo_waiting_pool=treatment_waiting_pool, treatment_rooms=treatment_rooms,
                           office_numbers=office_numbers)

@app.route('/numbers')
def view_numbers():
    return render_template('numbers.html', issued_numbers=issued_numbers)


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

if __name__ == '__main__':
    app.run(host='0.0.0.0')