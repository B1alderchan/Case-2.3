import sqlite3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Establish database connection
conn = sqlite3.connect('clever_power.db')
c = conn.cursor()

# CRUD operations for power_data table
@app.route('/power_data', methods=['POST'])
def add_power_data():
    # Get data from request
    data = request.json
    household_id = data['household_id']
    energy_consumed = data['energy_consumed']
    energy_produced = data['energy_produced']
    # Add new power data to database
    c.execute('INSERT INTO power_data (household_id, energy_consumed, energy_produced) VALUES (?, ?, ?)',
              (household_id, energy_consumed, energy_produced))
    conn.commit()
    return jsonify({'message': 'Power data added successfully!'})

@app.route('/power_data/<int:id>', methods=['GET'])
def get_power_data_by_id(id):
    # Connect to database
    conn = sqlite3.connect('clever_power.db')
    c = conn.cursor()

    # Get power data from database by id
    c.execute('SELECT * FROM power_data WHERE id = ?', (id,))
    power_data = c.fetchone()

    if power_data is not None:
        # Format response if power data exists
        response = {
            'id': power_data[0],
            'household_id': power_data[1],
            'timestamp': power_data[2],
            'energy_consumed': power_data[3],
            'energy_produced': power_data[4]
        }
    else:
        # Format response if power data does not exist
        response = {
            'message': 'Power data not found'
        }

    # Close database connection and return response
    conn.close()
    return jsonify(response)

try:
    # Open JSON file and load data
    with open('data.json') as f:
        data = json.load(f)

    # Connect to database
    conn = sqlite3.connect('clever_power.db')
    c = conn.cursor()
    
    
    # Loop through data and insert into power_data table
    for d in data:
        c.execute('''
            INSERT INTO power_data (household_id, energy_consumed, energy_produced)
            VALUES (?, ?, ?)
        ''', (d['household_id'], d['energy_consumed'], d['energy_produced']))
    
    # Commit changes and close connection
    conn.commit()
    

except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    conn.close()
