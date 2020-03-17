from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Imagen(db.Model):
    __tablename__ = 'Imagenes'

    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False) 
    Direccion = db.Column(db.String(100), nullable=False) 

    def json(self):
        return {
            'Id': self.Id,
            'Nombre': self.Nombre,
            'Direccion': self.Direccion
        }

