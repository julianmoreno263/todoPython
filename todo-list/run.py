#aqui ejecutamos la aplicacion importando una instancia d ela funcion create_app
from todor import create_app


#punto de entrada de una aplicacion en python
if __name__=="__main__":
    app=create_app()
    app.run()