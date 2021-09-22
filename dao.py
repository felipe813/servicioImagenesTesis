from models import Configuraciones, db
from models import Imagen
from models import Metadato
from models import MetadatoImagen
from models import Tipo
from models import Usuario
from models import Recorrido
from models import ImagenRecorrido
from models import PreguntaTest
from models import RespuestaPregunta
from models import TiempoRecorrido

from sqlalchemy import func
import time
from datetime import datetime

class DAO():
    def GetImagenes(self):
        return  [ imagen.json() for imagen in Imagen.query.all() ]  

    def GetImagen(self,id):
        return Imagen.query.filter_by(Id=id).first()

    def InsertarImagen (self,nombre, direccion, fuente,metadatos):
      
        imagen = Imagen(Nombre = nombre,Direccion = direccion, Fuente = fuente)
        try:
                db.session.add(imagen)
                db.session.commit()

                metadatosBD = []
                #Verificar que los metadatos estén en el sistema y que los tipos concuerden
                for meta in metadatos:
                    metaBD = Metadato.query.filter_by(Nombre = meta[0]).first()
                    if  metaBD is None:
                        print("El tipo "+meta[0]+" no está configurado")
                    else:
                        if metaBD.Tipo == "Fecha":
                            try:
                                time.strptime(meta[1], '%d/%m/%Y')
                                metadatosBD.append(MetadatoImagen(IdMetadato = metaBD.Id,Valor= meta[1], IdImagen = imagen.Id ))
                            except:
                                print("La fecha "+meta[1]+" no está en el formato correcto")
                                continue
                        else:
                            metadatosBD.append(MetadatoImagen(IdMetadato = metaBD.Id,Valor= meta[1], IdImagen = imagen.Id ))

                for m in metadatosBD:
                    db.session.add(m)
                db.session.commit()

                return imagen
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def ActualizarImagen (self,id, nombre, direccion, fuente):
      
        imagen = Imagen.query.filter_by(Id =id).first()

        if imagen is None:
            return imagen

        if nombre is not None:
            imagen.Nombre = nombre
        
        if direccion is not None:
            imagen.Direccion = direccion

        if fuente is not None:
            imagen.Fuente = fuente
        
        try:
            db.session.commit()
            return imagen
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def ActualizarImagen (self,id, nombre, direccion, fuente, nivelViolencia):
      
        imagen = Imagen.query.filter_by(Id =id).first()

        if imagen is None:
            return imagen

        if nombre is not None:
            imagen.Nombre = nombre
        
        if direccion is not None:
            imagen.Direccion = direccion

        if fuente is not None:
            imagen.Fuente = fuente

        if nivelViolencia is not None:
            imagen.NivelViolencia = nivelViolencia
        
        try:
            db.session.commit()
            return imagen
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def EliminarImagen (self,id):

        imagen = Imagen.query.filter_by(Id=id).first()
        metadatos = MetadatoImagen.query.filter_by(IdImagen=id).all()
        if imagen is None:
            print('La imagen no existe')
            return False

        try:
            for m in metadatos:
                db.session.delete(m)
                
            db.session.commit()
            db.session.delete(imagen)
            db.session.commit()
            return imagen
        except:
            return False



    def GetMetadato(self,id):
        return Metadato.query.filter_by(Id=id).first()


    def InsertarMetadatoImagen (self,idImagen, idMetadato, valor):  
        imagen = self.GetImagen(idImagen)
        metadato = self.GetMetadato(idMetadato)

        if imagen is None or metadato is None:
            print("No existe la imagen o el metadato seleccionados")
            return False

        if metadato.Tipo == "Fecha":
            try:
                time.strptime(valor, '%d/%m/%Y')
            except:
                print("La fecha "+valor+" no está en el formato correcto")
                return False
                       
        metadatoImagen = MetadatoImagen(IdMetadato = idMetadato,IdImagen = idImagen, Valor = valor)
        try:
                db.session.add(metadatoImagen)
                db.session.commit()

                return metadatoImagen
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def ActualizarMetadatoImagen (self,idImagen, idMetadato, valor):
      
        metadatoImagen = MetadatoImagen.query.filter_by(IdImagen = idImagen).filter_by(IdMetadato = idMetadato).first()

        if metadatoImagen is None:
            return metadatoImagen

        if valor is not None:
            metadatoImagen.Valor = valor
        
        try:
            db.session.commit()
            return metadatoImagen
        except Exception as e: 
            print("ERROR: "+str(e))
            return False

    def EliminarMetadatoImagen (self,idMetadato, idImagen):

        metadatoImagen = MetadatoImagen.query.filter_by(IdImagen = idImagen).filter_by(IdMetadato = idMetadato).first()
        
        if metadatoImagen is None:
            print('El metadato no existe')
            return False
        try:          
            db.session.delete(metadatoImagen)
            db.session.commit()
            return metadatoImagen
        except Exception as e: 
            print("ERROR: "+str(e))
            return False

    def GetTipo(self,tipo):
        return Tipo.query.filter_by(Tipo=tipo).first()

    def GetTipos(self):
        return  [ tipo.json() for tipo in Tipo.query.all() ]  

    def GetMetadatos(self):
        return  [ metadato.json() for metadato in Metadato.query.all() ]  
        
    def InsertarMetadato (self,nombre, tipo):  
        tipoBd = self.GetTipo(tipo)
        if tipoBd is None:
            print("El tipo no existe")
            return False
                       
        metadato = Metadato(Nombre = nombre,Tipo = tipo)
        try:
                db.session.add(metadato)
                db.session.commit()

                return metadato
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def ActualizarMetadato (self,idMetadato, nombre):
      
        metadato = Metadato.query.filter_by(Id = idMetadato).first()

        if metadato is None:
            return metadato

        if nombre is not None:
            metadato.Nombre = nombre
        
        try:
            db.session.commit()
            return metadato
        except Exception as e: 
            print("ERROR: "+str(e))
            return False

    def EliminarMetadato (self,idMetadato):

        metadato = Metadato.query.filter_by(Id = idMetadato).first()

        if metadato is None:
            print('El metadato no existe')
            return False
        try:          
            db.session.delete(metadato)
            db.session.commit()
            return metadato
        except Exception as e: 
            print("ERROR: "+str(e))
            return False


    def GetUsuarios(self):
        return  [ usuario.json() for usuario in Usuario.query.all() ]  

    def GetRecorridos(self):
        return  [ recorrido.json() for recorrido in Recorrido.query.all() ]  

    def InsertarUsuario (self,usuario, contrasena, nombre, edad):         
                       
        usuario = Usuario(Usuario = usuario,Contrasena = contrasena, Nombre = nombre, Edad = edad)
        try:
                db.session.add(usuario)
                db.session.commit()

                return usuario
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def GetUsuario(self,usuario,contrasena):
        return Usuario.query.filter_by(Usuario=usuario,Contrasena=contrasena).first()
        
    def GetRandomImagenes(self, cantidad):
        return  [ imagen.json() for imagen in Imagen.query.order_by(func.random()).limit(cantidad).all()] 

    def GetRandomImagenesNivelViolencia(self, cantidad, nivelViolencia):
        imagenes = Imagen.query.filter_by(NivelViolencia=nivelViolencia).count()
        if(imagenes > 0):
            return  [ imagen.json() for imagen in Imagen.query.filter_by(NivelViolencia=nivelViolencia).order_by(func.random()).limit(cantidad).all()]  
        else:
            print("No existen imágenes con nivel de violencia "+nivelViolencia)
            return  [ imagen.json() for imagen in Imagen.query.order_by(func.random()).limit(cantidad).all()]

    def InsertarRecorrido (self,idUsuario, idImagenes):
        now = datetime.now()
        recorrido = Recorrido(FechaRecorrido = now,IdUsuario = idUsuario)
        try:
                db.session.add(recorrido)
                db.session.commit()
            
                imagenesDB = []
                #Verificar que los metadatos estén en el sistema y que los tipos concuerden
                for img in idImagenes:
                    imgDB = Imagen.query.filter_by(Id = img).first()
                    if  imgDB is None:
                        print("La imagen con id "+img+" no existe en el sistema")
                    else:
                        imagenesDB.append(ImagenRecorrido(IdImagen = img,Calificacion= -1, IdRecorrido = recorrido.Id))

                for m in imagenesDB:
                    db.session.add(m)
                db.session.commit()

                return recorrido
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def CalificarImagen (self,idRecorrido, idImagen, calificacion):
      
        imagenRecorrido = ImagenRecorrido.query.filter_by(IdRecorrido =idRecorrido,IdImagen = idImagen).first()

        if imagenRecorrido is None:
            return imagenRecorrido

        if calificacion is not None:
            imagenRecorrido.Calificacion = calificacion
        
        try:
            db.session.commit()
            return imagenRecorrido
        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def GetPreguntas(self):
            return  [ pregunta.json() for pregunta in PreguntaTest.query.all() ]  

    def ResponderPregunta (self,idRecorrido, idPregunta, respuesta):

        respuesta = RespuestaPregunta( IdRecorrido= idRecorrido,IdPregunta = idPregunta, Respuesta = respuesta)
        try:
                db.session.add(respuesta)
                db.session.commit()        
                return respuesta

        except Exception as e: 
                print("ERROR: "+str(e))
                return False
                

    def AgregarTiempo (self,idRecorrido,tiempo):
        tiempo = TiempoRecorrido( IdRecorrido= idRecorrido,Tiempo = tiempo)
        try:
                db.session.add(tiempo)
                db.session.commit()      
                return tiempo

        except Exception as e: 
                print("ERROR: "+str(e))
                return False

    def GetTiempos(self):
            return  [ tiempo.json() for tiempo in TiempoRecorrido.query.all() ]

    def GetDireccionFTP(self):
            return  [ configuracion.json() for configuracion in Configuraciones.query.filter_by(Nombre ="FTP").all() ]  

    def ActualizarFTP(self,ftp):
        ftpExistente = Configuraciones.query.filter_by(Nombre ="FTP").first()

        if ftpExistente is None:
            return ftpExistente

        if ftp is not None:
            ftpExistente.Valor = ftp       
        try:
            db.session.commit()
            return ftpExistente.json()
        except Exception as e: 
            print("ERROR: "+str(e))
            return False