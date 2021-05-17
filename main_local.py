from flask import Flask
from flask import jsonify
from flask import request 
from config import config
from models import db
from dao import DAO



def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        #db.create_all()
    return app

enviroment = config['development']
app = create_app(enviroment)
dao = DAO()

@app.route('/')
def inicio():
    response = {'message': 'API IMAGENES'}
    return jsonify(response)

@app.route('/api/imagenes',methods=['GET'])
def get_imagenes():
    app.logger.warning('get_imagenes')
    #imagenes = [ imagen.json() for imagen in Imagen.query.all() ]  
    imagenes = dao.GetImagenes()
    return jsonify({'Imagenes': imagenes })

@app.route('/api/imagenes/<id>', methods=['GET'])
def get_imagen(id):
    imagen = dao.GetImagen(id)
    if imagen is None:
        return jsonify({'message': ' La imagen no existe'}), 404

    return jsonify({'Imagen': imagen.json() })

@app.route('/api/imagenes/', methods=['POST'])
def create_imagen():
    json = request.get_json(force=True)

    if json.get('Nombre') is None or  json.get('Direccion') is None or json.get('Fuente') is None :
        return jsonify({'message': 'Bad request'}), 400

    metadatos = []
    if json.get('Metadatos') is not None:
        for metadato in json['Metadatos']:
            if metadato["Nombre"] is not None and metadato["Valor"] is not None:
                metadatos.append([metadato["Nombre"],metadato["Valor"]])

    imagen = dao.InsertarImagen(json['Nombre'],json['Direccion'],json['Fuente'], metadatos)

    if imagen is not False:
        return jsonify({'Imagen': imagen.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400


@app.route('/api/imagenesMultiples/', methods=['POST'])
def create_imagen_multiple():
    jsonFull = request.get_json(force=True)
    contador = 0
    for json in jsonFull:
        if json.get('Nombre') is None or  json.get('Direccion') is None or json.get('Fuente') is None :
            #return jsonify({'message': 'Bad request'}), 400
            continue

        metadatos = []
        if json.get('Metadatos') is not None:
            for metadato in json['Metadatos']:
                if metadato["Nombre"] is not None and metadato["Valor"] is not None:
                    metadatos.append([metadato["Nombre"],metadato["Valor"]])

        imagen = dao.InsertarImagen(json['Nombre'],json['Direccion'],json['Fuente'], metadatos)

        if imagen is not False:
            contador = contador +1
            #return jsonify({'Imagen': imagen.json() })
        #else:
            #return jsonify({'message': 'Bad request'}), 400
    
    return jsonify({'Imagenes':str(contador) })

@app.route('/api/imagenes/<id>', methods=['PUT'])
def update_imagen(id):
    json = request.get_json(force=True)

    nombre = json.get('Nombre')
    direccion = json.get('Direccion')
    fuente = json.get('Fuente')

    imagen = dao.ActualizarImagen(id,nombre,direccion,fuente)

    if imagen is not False:
        return jsonify({'Imagen': imagen.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400

@app.route('/api/imagenes/<id>', methods=['DELETE'])
def delete_imagen(id):

    imagen = dao.EliminarImagen(id)

    if imagen is not False:
        return jsonify({'Imagen': imagen.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400





@app.route('/api/metadatoImagenes/', methods=['POST'])
def create_metadato_imagen():
    json = request.get_json(force=True)

    if json.get('IdImagen') is None or  json.get('IdMetadato') is None or json.get('Valor') is None :
        return jsonify({'message': 'Bad request'}), 400

    metadatoImagen = dao.InsertarMetadatoImagen(json['IdImagen'],json['IdMetadato'],json['Valor'])

    if metadatoImagen is not False:
        return jsonify({'MetadatoImagen': metadatoImagen.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400


@app.route('/api/metadatoImagenes/', methods=['PUT'])
def update_metadato_imagen():
    json = request.get_json(force=True)

    if json.get('IdImagen') is None or  json.get('IdMetadato') is None or json.get('Valor') is None :
        return jsonify({'message': 'Bad request'}), 400

    metadatoImagen = dao.ActualizarMetadatoImagen(json['IdImagen'],json['IdMetadato'],json['Valor'])

    if metadatoImagen is not False:
        return jsonify({'MetadatoImagen': metadatoImagen.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400

@app.route('/api/metadatoImagenes/<idMetadato>/<idImagen>', methods=['DELETE'])
def delete_metadato_imagen(idMetadato,idImagen):

    metadatoImagen = dao.EliminarMetadatoImagen(idMetadato,idImagen)

    if metadatoImagen is not False:
        return jsonify({'MetadatoImagen': metadatoImagen.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400





@app.route('/api/metadato/', methods=['POST'])
def create_metadato():
    json = request.get_json(force=True)

    if json.get('Nombre') is None or  json.get('Tipo') is None:
        return jsonify({'message': 'Bad request'}), 400

    metadato = dao.InsertarMetadato(json['Nombre'],json['Tipo'])

    if metadato is not False:
        return jsonify({'Metadato': metadato.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400


@app.route('/api/metadato/<id>', methods=['PUT'])
def update_metadato(id):
    json = request.get_json(force=True)

    if json.get('Nombre') is None:
        return jsonify({'message': 'Bad request'}), 400


    metadato = dao.ActualizarMetadato(id,json['Nombre'])

    if metadato is not False:
        return jsonify({'Metadato': metadato.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400

@app.route('/api/metadato/<idMetadato>', methods=['DELETE'])
def delete_metadato(idMetadato):

    metadato = dao.EliminarMetadato(idMetadato)

    if metadato is not False:
        return jsonify({'Metadato': metadato.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400

@app.route('/api/metadato',methods=['GET'])
def get_metadatos():
    metadatos = dao.GetMetadatos()
    return jsonify({'Metadatos': metadatos })

@app.route('/api/tipos',methods=['GET'])
def get_tipos():
    tipos = dao.GetTipos()
    return jsonify({'Tipos': tipos })



@app.route('/api/usuarios',methods=['GET'])
def get_usuarios():
    app.logger.warning('get_usuarios') 
    usuarios = dao.GetUsuarios()
    return jsonify({'Usuarios': usuarios })

@app.route('/api/recorridos',methods=['GET'])
def get_recorridos():
    app.logger.warning('get_recorridos') 
    recorridos = dao.GetRecorridos()
    return jsonify({'Recorridos': recorridos })

@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    json = request.get_json(force=True)

    if json.get('Usuario') is None or  json.get('Contrasena') is None or json.get('Nombre') is None or json.get('Edad') is None:
        return jsonify({'message': 'Bad request'}), 400

    usuario = dao.InsertarUsuario(json['Usuario'],json['Contrasena'],json['Nombre'],json['Edad'])

    if usuario is not False:
        return jsonify({'Usuario': usuario.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400

@app.route('/api/usuarios/<usuario>/<contrasena>', methods=['GET'])
def get_usuario(usuario,contrasena):
    usuario = dao.GetUsuario(usuario,contrasena)
    if usuario is None:
        return jsonify({'message': 'El usuario no existe'}), 404

    return jsonify({'Usuario': usuario.json() })


@app.route('/api/imagenesRandom/<cantidad>',methods=['GET'])
def get_imagenes_random(cantidad):
    app.logger.warning('get_imagenes')
    #imagenes = [ imagen.json() for imagen in Imagen.query.all() ]  
    imagenes = dao.GetRandomImagenes(cantidad)
    return jsonify({'Imagenes': imagenes })


@app.route('/api/recorridos', methods=['POST'])
def create_recorrido():
    json = request.get_json(force=True)

    if json.get('IdUsuario') is None :
        return jsonify({'message': 'Bad request'}), 400

    imagenes = []
    if json.get('IdImagenes') is not None:
        for img in json['IdImagenes']:
            imagenes.append(img)

    recorrido = dao.InsertarRecorrido(json['IdUsuario'], imagenes)

    if recorrido is not False:
        return jsonify({'Recorrido': recorrido.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400

@app.route('/api/recorridos', methods=['PUT'])
def update_imagen_recorrido():
    json = request.get_json(force=True)  
    if json.get('Calificacion') is None :
        return jsonify({'message': 'Bad request'}), 400

    if json.get('IdRecorrido') is None :
        return jsonify({'message': 'Bad request'}), 400

    if json.get('IdImagen') is None :
        return jsonify({'message': 'Bad request'}), 400

    calificacion = json.get('Calificacion')
    idRecorrido = json.get('IdRecorrido')
    idImagen = json.get('IdImagen')

   
    recorridoImagen = dao.CalificarImagen(idRecorrido,idImagen,calificacion)

    if recorridoImagen is not False:
        return jsonify({'RecorridoImagen': recorridoImagen.json() })
    else:
        return jsonify({'message': 'Bad request'}), 400


@app.route('/api/preguntasTest',methods=['GET'])
def get_preguntas():
    preguntas = dao.GetPreguntas()
    return jsonify({'Preguntas': preguntas })


@app.route('/api/RespuestasTest', methods=['POST'])
def create_respuesta():
    json = request.get_json(force=True)

    if json.get('IdRecorrido') is None :
        return jsonify({'message': 'Bad request1'}), 400

    if json.get('IdPregunta') is None :
        return jsonify({'message': 'Bad request2'}), 400

    if json.get('Respuesta') is None :
        return jsonify({'message': 'Bad request3'}), 400

    if json.get('Tiempo') is None :
        return jsonify({'message': 'Bad request4'}), 400

    respuesta = dao.ResponderPregunta(json['IdRecorrido'], json['IdPregunta'],json['Respuesta'])

    respuesta2 = dao.AgregarTiempo(json['IdRecorrido'],json['Tiempo'])
    print(respuesta2.json())

    if respuesta is not False:
        return jsonify({'Recorrido': respuesta.json() })
    else:
        return jsonify({'message': 'Bad request5'}), 400

@app.route('/api/tiemposRecorrido',methods=['GET'])
def get_tiempos():
    tiempos = dao.GetTiempos()
    return jsonify({'Tiempos': tiempos })

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=16790)