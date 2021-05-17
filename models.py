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


class TiempoRecorrido(db.Model):
    __tablename__ = 'TiempoRecorrido'

    Id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    IdRecorrido = db.Column(db.Integer)
    Tiempo = db.column(db.Float)

    def json(self):
        return {
            'Id': self.Id,
            'Recorrido': self.IdRecorrido,
            'Tiempo': self.Tiempo
        }


class Usuario(db.Model):
    __tablename__ = 'Usuario'

    Id = db.Column(db.Integer, primary_key=True)
    Usuario = db.Column(db.String(50), nullable=False) 
    Contrasena = db.Column(db.String(100), nullable=False) 
    Nombre = db.Column(db.String(200), nullable=False) 
    Edad = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'Id': self.Id,
            'Nombre': self.Nombre,
            'Usuario': self.Usuario,
            'Contraseña': self.Contrasena,
            'Edad': self.Edad
        }


class Recorrido(db.Model):
    __tablename__ = 'Recorrido'

    Id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    #FechaRecorrido = db.Column(db.DateTime, default=db.func.current_timestamp())
    FechaRecorrido = db.Column(db.String(100), nullable=False) 
    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.Id'),primary_key=True)

    ImagenRecorrido = db.relationship('ImagenRecorrido')
    Usuario = db.relationship('Usuario')

    def json(self):
        return {
            'Id': self.Id,
            'FechaRecorrido': self.FechaRecorrido,
            #'Usuario': self.IdUsuario,
            'NombreUsuario': self.Usuario.Nombre,
            'Imagenes':[imagen.json() for imagen in self.ImagenRecorrido]
        }

class ImagenRecorrido(db.Model):
    __tablename__ = 'ImagenRecorrido'

    IdRecorrido = db.Column(db.Integer, db.ForeignKey('Recorrido.Id') ,primary_key=True)
    Calificacion = db.Column(db.Integer) 
    IdImagen = db.Column(db.Integer, db.ForeignKey('Imagenes.Id'),primary_key=True)

    Recorrido = db.relationship('Recorrido',back_populates="ImagenRecorrido")
    Imagen = db.relationship('Imagen')

    def json(self):
        return {
            #'Recorrido': self.Recorrido.Id,
            'IdImagen': self.IdImagen,
            'Calificacion': self.Calificacion,
            'NombreImagen':self.Imagen.Nombre,
            'DireccionImagen':self.Imagen.Direccion
        }

class PreguntaTest(db.Model):
    __tablename__ = 'PreguntaTest'

    IdPregunta = db.Column(db.Integer, primary_key=True)
    Pregunta = db.Column(db.String(200), nullable=False) 

    RespuestaPregunta = db.relationship('RespuestaPregunta')

    def json(self):
        return {
            'Id': self.IdPregunta,
            'Pregunta': self.Pregunta,            
            'Respuestas':[respuesta.json() for respuesta in self.RespuestaPregunta]
        }

class RespuestaPregunta(db.Model):
    __tablename__ = 'RespuestaPregunta'

    IdPregunta = db.Column(db.Integer, db.ForeignKey('PreguntaTest.IdPregunta') ,primary_key=True)
    IdRecorrido = db.Column(db.Integer, db.ForeignKey('Recorrido.Id') ,primary_key=True)
    Respuesta = db.Column(db.Integer)

    def json(self):
        return {
            'IdPregunta': self.IdPregunta,
            'IdRecorrido': self.IdRecorrido,
            'Respuesta':self.Respuesta
        }



