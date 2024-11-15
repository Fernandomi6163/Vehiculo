from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String)
    modelo = db.Column(db.String)
    año = db.Column(db.Integer)

    def __repr__(self):
        return f'<Vehiculo {self.marca} {self.modelo}>'