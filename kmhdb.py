import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Create a SQLite database in-memory
db = sqlite3.connect(':memory:')
cursor = db.cursor()

# Define tables for storing data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT,
        office TEXT,
        status BOOLEAN,
        room_number INTEGER
    )
''')

@app.route('/issue-number')
def issue_number():
    # Logic for issuing numbers
    barcode = 'A123'  # Replace with your logic to generate barcodes
    
    # Insert data into the SQLite database
    cursor.execute("INSERT INTO patient_data (barcode, office, status, room_number) VALUES (?, ?, ?, ?)",
                   (barcode, '', False, 0))
    db.commit()
    
    return jsonify({'barcode': barcode})

@app.route('/assign-office', methods=['POST'])
def assign_office():
    try:
        barcode = request.json['barcode']
        office_number = request.json['office_number']
        
        # Update data in the SQLite database
        cursor.execute("UPDATE patient_data SET office = ?, room_number = ? WHERE barcode = ?",
                       (office_number, 0, barcode))
        db.commit()
        
        return jsonify({'message': f'Patient with barcode {barcode} assigned to office {office_number}.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add-to-chemo-waiting', methods=['POST'])
def add_to_chemo_waiting():
    try:
        barcode = request.json['barcode']
        eligible = request.json['status']

        # Update data in the SQLite database
        cursor.execute("UPDATE patient_data SET status = ?, room_number = ? WHERE barcode = ?",
                       (eligible, 0, barcode))
        db.commit()
        
        if eligible:
            return jsonify({'message': f'Patient with barcode {barcode} added to chemo waiting pool.'})
        else:
            return jsonify({'message': f'Patient with barcode {barcode} is not eligible for chemo.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/assign-treatment-room', methods=['POST'])
def assign_treatment_room():
    try:    
        room_number = int(request.json['room_number'])
        barcode = request.json['barcode']

        # Update data in the SQLite database
        cursor.execute("UPDATE patient_data SET room_number = ? WHERE barcode = ?",
                       (room_number, barcode))
        db.commit()
        
        return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} assigned to treatment room {room_number}.'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rmv-barcode', methods=['POST'])
def remove_barcode():
    try:
        barcode = request.json['barcode']

        # Delete data from the SQLite database
        cursor.execute("DELETE FROM patient_data WHERE barcode = ?", (barcode,))
        db.commit()

        return jsonify({'barcode': barcode, 'message': f'Patient with barcode {barcode} removed.'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/import-ticket', methods=['POST'])
def import_ticket():
    try:
        data = request.json
        ticket = data['ticket']
        destination = data['destination']
        
        # Insert data into the SQLite database
        cursor.execute("INSERT INTO patient_data (barcode, office, status, room_number) VALUES (?, ?, ?, ?)",
                       (ticket, '', False, 0))
        db.commit()
        
        return jsonify({'message': f'Ticket {ticket} imported to {destination}.'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_application():
    try:
        # Delete all data from the SQLite database
        cursor.execute("DELETE FROM patient_data")
        db.commit()

        return jsonify({'message': 'Application reset.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/office-pool')
def get_office_pool():
    cursor.execute("SELECT barcode FROM patient_data WHERE office = ''")
    data = cursor.fetchall()
    office_pool = [row[0] for row in data]
    return jsonify({'office_pool': office_pool})

@app.route('/assigned-offices')
def get_assigned_offices():
    cursor.execute("SELECT DISTINCT office FROM patient_data WHERE office != ''")
    data = cursor.fetchall()
    assigned_offices = [row[0] for row in data]
    return jsonify({'assigned_offices': assigned_offices})

@app.route('/chemo-waiting-pool')
def get_chemo_waiting_pool():
    cursor.execute("SELECT barcode FROM patient_data WHERE status = 1")
    data = cursor.fetchall()
    chemo_waiting_pool = [row[0] for row in data]
    return jsonify({'chemo_waiting_pool': chemo_waiting_pool})

@app.route('/treatment-rooms')
def get_treatment_rooms():
    cursor.execute("SELECT DISTINCT room_number FROM patient_data WHERE room_number != 0")
    data = cursor.fetchall()
    treatment_rooms = [row[0] for row in data]
    return jsonify({'treatment_rooms': treatment_rooms})

@app.route('/pools')
def view_pools():
    cursor.execute("SELECT DISTINCT office FROM patient_data WHERE office != ''")
    data = cursor.fetchall()
    office_numbers = [row[0] for row in data]
    return render_template('nurses.html', office_pool=get_office_pool(),
                           assigned_offices=office_numbers,
                           chemo_waiting_pool=get_chemo_waiting_pool(),
                           treatment_rooms=get_treatment_rooms(),
                           office_numbers=office_numbers)

@app.route('/pools3')
def view_pools3():
    cursor.execute("SELECT DISTINCT office FROM patient_data WHERE office != ''")
    data = cursor.fetchall()
    office_numbers = [row[0] for row in data]
    return render_template('doctors.html', office_pool=get_office_pool(),
                           assigned_offices=office_numbers,
                           chemo_waiting_pool=get_chemo_waiting_pool(),
                           treatment_rooms=get_treatment_rooms(),
                           office_numbers=office_numbers)

if __name__ == '__main__':
    app.run(debug=True)
