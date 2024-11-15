from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://vehiculos_pmvk_user:Q1FO9JdIExObcFMCzTottMs6z4dYPMLv@dpg-csrke8d6l47c73fggau0-a/vehiculos_pmvk')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM vehiculo;')
    vehiculos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(vehiculos)

@app.route('/vehiculo', methods=['POST'])
def add_vehiculo():
    new_vehiculo = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO vehiculo (placa, color, modeloc, marca) VALUES (%s, %s, %s, %s)',
                (new_vehiculo['placa'], new_vehiculo['color'], new_vehiculo['modeloc'], new_vehiculo['marca']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_vehiculo), 201

if __name__ == '__main__':
    app.run(debug=True)
    