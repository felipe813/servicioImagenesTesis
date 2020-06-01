from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Imagen(db.Model):
    __tablename__ = 'Imagenes'

    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False) 
    Direccion = db.Column(db.String(100), nullable=False) 
    Fuente = db.Column(db.String(200), nullable=True) 

    MetadatoImagen = db.relationship('MetadatoImagen')

    def json(self):
        return {
            'Id': self.Id,
            'Nombre': self.Nombre,
            'Direccion': self.Direccion,
            'Fuente': self.Fuente,
            'Metadata':[metadato.json() for metadato in self.MetadatoImagen]
        }



class MetadatoImagen(db.Model):
    __tablename__ = 'MetadatoImagen'

    IdMetadato = db.Column(db.Integer, db.ForeignKey('Metadato.Id') ,primary_key=True)
    Valor = db.Column(db.String(50), nullable=False) 
    IdImagen = db.Column(db.Integer, db.ForeignKey('Imagenes.Id'),primary_key=True)

    Metadato = db.relationship('Metadato',back_populates="MetadatosImagenes")

    def json(self):
        return {
            'IdMetadato': self.IdMetadato,
            'Valor': self.Valor,
            #'IdImagenes': self.IdImagen,
            'Nombre':self.Metadato.Nombre
        }

class Metadato(db.Model):
    __tablename__ = 'Metadato'

    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False) 
    Tipo = db.Column(db.String(50), nullable=False) 

    MetadatosImagenes = db.relationship('MetadatoImagen',back_populates="Metadato")

    def json(self):
        return {
            'IdMetadato': self.Id,
            'Nombre': self.Nombre,
            'Tipo': self.Tipo,
        }

class Tipo(db.Model):
    __tablename__ = 'Tipo'

    Tipo = db.Column(db.String(50), primary_key=True)

    def json(self):
        return {
            'Tipo': self.Tipo
        }








