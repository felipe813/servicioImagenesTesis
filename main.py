from flask import Flask
from flask import jsonify
from config import config
from models import db
from models import Imagen

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

@app.route('/')
def inicio():
    response = {'message': 'API IMAGENES'}
    return jsonify(response)

@app.route('/api/imagenes',methods=['GET'])
def get_imagenes():
    app.logger.warning('get_imagenes')
    imagenes = [ imagen.json() for imagen in Imagen.query.all() ] 
    return jsonify({'imagenes': imagenes })

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80)

