import urllib

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True

   
    SQLALCHEMY_DATABASE_URI = 'sqlite:///repositorio_imagenes.db'

    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:bartolomeo@localhost:5432/proyectoTesis'

    #params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};SERVER=Felipe;DATABASE=ProyectoTesis;UID=sa;PWD=felipe")
    #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
}