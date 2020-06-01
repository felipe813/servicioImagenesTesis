from flask import Flask
from flask import jsonify
from flask import request 
from config import config
from models import db
from dao import DAO


#https://codigofacilito.com/articulos/api-flask

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


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=16790)

