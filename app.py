from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configurar la URL de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://vehiculos_pmvk_user:Q1FO9JdIExObcFMCzTottMs6z4dYPMLv@dpg-csrke8d6l47c73fggau0-a/vehiculos_pmvk')

# Corregir el esquema si es necesario
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Función para obtener conexión a la base de datos
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise

# Ruta para obtener todos los vehículos
@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM vehiculo;')
        vehiculos = cur.fetchall()
        cur.close()
        conn.close()

        # Mapear resultados a un JSON
        vehiculos_list = [
            {"id": v[0], "placa": v[1], "color": v[2], "modelo": v[3], "marca": v[4]}
            for v in vehiculos
        ]
        return jsonify(vehiculos_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para agregar un nuevo vehículo
@app.route('/vehiculo', methods=['POST'])
def add_vehiculo():
    try:
        new_vehiculo = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO vehiculo (placa, color, modelo, marca) VALUES (%s, %s, %s, %s)',
            (new_vehiculo['placa'], new_vehiculo['color'], new_vehiculo['modelo'], new_vehiculo['marca'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(new_vehiculo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
