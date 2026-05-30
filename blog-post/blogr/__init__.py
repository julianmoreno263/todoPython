from flask import Flask
from flask_sqlalchemy import SQLAlchemy




#instancia de la db
db=SQLAlchemy()


#Este código define lo que en el mundo de Flask se conoce como una Application Factory (Fábrica de Aplicaciones).

# En lugar de crear la instancia de app de forma global en el cuerpo de tu archivo, la encapsulas dentro de una función. Esto es una práctica profesional recomendada para proyectos que escalan.

#Declara la función constructora. Al llamarla, esta "fabrica" y te devuelve una instancia lista de tu servidor.
def createApp():

    #crear app de flask, El argumento __name__ le dice a Flask dónde buscar recursos como plantillas y archivos estáticos.
    app=Flask(__name__)

    #aqui cargamos el archivo de configuracion
    app.config.from_object("config.Config")

    db.init_app(app)
    #cargamos los modelos de la bd
    from blogr import home,auth,post

    # db.init_app(app)

    #importamos ckeditor para crear nuestros posts
    from flask_ckeditor import CKEditor
    ckeditor = CKEditor(app)

    #configuracion del idioma de la app en español
    import locale
    locale.setlocale(locale.LC_ALL,"es_ES")


    #registrar vistas, estás diciéndole a la aplicación principal: "Oye, todas las rutas y funciones que definí en el Blueprint llamado 'home', o 'auth',etc, ahora forman parte de esta app".

    app.register_blueprint(home.bp) 
    app.register_blueprint(auth.bp)
    app.register_blueprint(post.bp) 

    #aqui migramos los modelos de las tablas a la bd
    from .models import User,Post
    with app.app_context():
        db.create_all()


        
    return app






