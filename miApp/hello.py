from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField #estas clases crean inputs de tipo str,password y submit
from wtforms.validators import DataRequired,Length
from datetime import datetime



#para correr la aplicacion en flask se usa este comando: flask --app "nombre aplicacion" --debug run, el modo --debug lo que hace es depurar, si hay errores en la app este modo los marca,y cada vez que haya un cambio en la app no hay que estar corriendo de nuevo la aplicacion,ella se reinicia automaticamente


#creamos aplicacion flask
app=Flask(__name__)

#cuando trabajamos con formularios creados con WTForms debemos generar una clave secreta para evitar ataques csrf
app.config.from_mapping(
    SECRET_KEY="dev"
)

#podemos crear filtros personalizados,son en si funciones,por ejemplo si queremos mostrar una fecha con un formato especifico,creamos esa funcion que se pasa como un filtro en la plantilla donde queremos mostrarla. Para que esta funcion flask la vea como un filtro la debemos agregar como una funcion decoradora poniendo: @app.add-template-filter,o tambien se puede registrar asi: app.add-template-filter(today,"today"),poniendo el nombre de la funcion.

# @app.add_template_filter
def today(date):
    return date.strftime("%d-%m-%Y")

app.add_template_filter(today,"today")#asi se registra el filtro personalizado

#tambien podemos pasar funciones personalizadas,por ejemplo hacemos una funcion que reciba un string y lo multiplique una cantidad de veces segun el numero que se le pase. Para no tener que pasarle como parametro el nombre de la funcion al render_template,la podemos pasar como una funcion decoradora global con add_template_global
@app.add_template_global
def repeat(s,n):
    return s*n

#creamos la ruta principal la cual debe ir asociada a una funcion, estas funciones representan las vistas de la aplicacion. Una vista puede tener varias rutas,por ejemplo la pagina principal puede tener la ruta "/" y la ruta     "/index". Con render_template renderizo las plantillas, tambien se pueden pasar parametros para mostrarlos desde la plantilla,en la plantilla html se reciben utilizando {{}}
@app.route("/")
def index():
    #con url_for contruyo rutas
    print(url_for("index"))
    print(url_for("hello"))
    print(url_for("code",code='print("hola")'))

    name="Julian"
    friends=["Ingrid","sandra","pepe","juan"]
    date=datetime.now()

    return render_template("index.html", name=name,friends=friends,date=date)


#las rutas pueden recibir parametros,se los indicamos en la ruta entre <>, y la funcion llevaria el parametro para poder usarlo. Tambien se pueden recibir diferentes tipos de parametros no solo string,tambiem int,float,etc,simplemente le indicamos el tipo de parametro. Como una funcion puede tener varias rutas podemos evaluar si una ruta tiene parametros o no y actuar en consecuencia asi:
@app.route("/hello")
@app.route("/hello/<name>")
@app.route("/hello/<name>/<int:age>")
@app.route("/hello/<name>/<int:age>/<email>")
def hello(name=None,age=None,email=None):
   myData={
       "name":name,
       "age":age,
       "email":email

   }

   return render_template("hello.html",data=myData)


#la funcion escape de la libreria de flask markupsafe sirve para escapar codigo que podria ser dañino para la aplicacion,por ejemplo en la url nos podrian inyectar codigo de javascript para vulnerar la aplicacion,entonces escape ayuda a que este codigo dañino no se ejecute sino que se muestre como un simple string. En la ruta se puede utilizar la etiqueta <code> para inyectar codigo, si no queremos que ese codigo se ejecute al visitar esa ruta lo escapamos con la funcion escape(), aqui en este caso el codigo que pasemos solo se mostrara como un string y no se ejecuta
from markupsafe import escape
@app.route("/code/<path:code>")
def code(code):
    return f"<code>{escape(code)}</code>"

#crear formularios con la biblioteca flask-wtf
#creamos una clase que herede de Flaskform
class RegisterForm(FlaskForm):
    username=StringField("Nombre de usuario: ", validators=[DataRequired(),Length(min=4,max=25)])
    password=PasswordField("Password: ", validators=[DataRequired(),Length(min=6,max=40)])
    submit=SubmitField("Registrar: ")


#Registrar usuario,se le puede especificar a la ruta los metodos con los que va a trabajar esta ruta,se debe importar el metodo request para hacer peticiones con python
@app.route("/auth/register",methods=["GET","POST"])
def register():

    #instancia de formulario creado con WTForms
    form=RegisterForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        return f"Nombre de usuario: {username}, Contraseña: {password}"


    return render_template("auth/register.html",form=form)


    