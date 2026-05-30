#configuraciones iniciales de la app

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # type: ignore



#creamos una funcion que crea la app, esta funcion nos permitira reutilizarla donde la necesitemos,por ejemplo  cuando necesitemos usar la bd con una instancia de la aplicacion podemos reutilizar esta funcion 

#crear instancia de sqlalchemy
db=SQLAlchemy()

def create_app():
    #creamos app
    app=Flask(__name__)
    #configuracion del proyecto
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///todolist.db"
    )

    #inicializamos la conexion a la db
    db.init_app(app)

    # --- MOVEMOS LAS IMPORTACIONES AQUÍ ABAJO ---
    # Esto rompe el círculo: 'db' ya existe cuando estos archivos se cargan
    # from . import todo
    # from . import auth

    from todor import todo
    from todor import auth

    #registrar blueprint
    app.register_blueprint(todo.bp)
    app.register_blueprint(auth.bp)



    @app.route("/")
    def index():
        return render_template("index.html")
    

    #con esto migramos el modelo de la db
    with app.app_context():
        db.create_all()
    
    return app
    