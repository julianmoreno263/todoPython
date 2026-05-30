#archivo para la autenticacion de usuario, aqui tambien utilizamos blueprint,flash sirve para enviar mensajes a nuestras plantillas,como errores,etc. Con werzeug tenemos funcionalidad para encriptar los passwords y poder validar los datos. El objeto g que importamos de flask sirve para almacenar la cookie de sesion

from flask import (Blueprint, render_template,request,url_for,redirect,flash,session,g)
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User  #con esta linea se migran los modelos para la bd
from todor import db
import functools

#instancia de blueprint,este es el prefijo para las demas rutas
bp=Blueprint("auth",__name__,url_prefix="/auth")


#ruta /list
@bp.route("/register", methods=("GET","POST"))
def register():
    #1-si usamos POST se deben capturara los datos del formulario primero
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        #2-ahora creamos un objeto de tipo User con el password encriptado
        user=User(username,generate_password_hash(password))
        #3-verificamos si nuestro username ya existe en la bd o no, si no existe lo agregamos a la bd, con session.commit() se guardan los datos, y luego hacemos que se redireccione al login
        user_name=User.query.filter_by(username=username).first()
        if user_name==None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
             error=f"El usuario {username} ya está registrado en la base de datos"

        flash(error)
          

    return render_template("auth/register.html")

#ruta /create
@bp.route("/login", methods=("GET", "POST"))
def login():
        #1-si usamos POST se deben capturar los datos del formulario primero
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        error=None
        #2-validamos datos
        user=User.query.filter_by(username=username).first()
        if user == None:
            error="Nombre de usuario incorrecto"
        elif not check_password_hash(user.password, password):
            error="Contraseña incorrecta"
        #3-iniciar sesion
        if error is None:
            session.clear()
            session['user_id']=user.id # type: ignore
            return redirect(url_for("todo.index"))

        flash(error)
    return render_template("auth/login.html")


#funcion para capturar el usuario que ha iniciado sesion por medio del id para poder mantener la sesion,con el decorador le indicamos que se ejecute en cada peticion,en cualquier parte de la aplicacion verifica si alguien ha iniciado sesion o no, con esto se mantiene el inicio de sesion
@bp.before_app_request
def loadLoggedUser():
    #capturamos el usuario que ha iniciado sesion
    user_id=session.get('user_id')
    #si nadie ha iniciado sesion user_id sera None,si alguien inicio sesion capturamos el id de ese usuario o sino devolvemos un error 404
    if user_id is None:
        g.user=None
    else:
        g.user=User.query.get_or_404(user_id)


#funcion para cerrar sesion
@bp.route("/logout") # type: ignore
def logout():
    session.clear()
    return redirect(url_for("index"))



#esta funcion permitira especificar que se debe iniciar sesion para poder acceder a las demas partes de la aplicacion, para esto usamos el paquete functools
def loginRequired(view):
    @functools.wraps(view)
    def wrapper_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapper_view


# Este código define lo que en Python conocemos como un decorador. Su función principal es actuar como un "guardia de seguridad" para tus rutas o funciones: antes de dejar entrar a alguien a una página, verifica si tiene las llaves (si ha iniciado sesión).

# Aquí tienes el desglose paso a paso:

# 1. La estructura del "Envoltorio"
# El decorador funciona como una caja de regalo.

# loginRequired(view): Es la caja exterior. Recibe la función original (la vista de tu página) que quieres proteger.

# @functools.wraps(view): Es un detalle técnico importante. Sirve para que la función no "olvide" su nombre original y sus metadatos después de ser decorada.

# wrapper_view: Es el papel de regalo o la lógica que envuelve a la función original.

# 2. La lógica de control (El "Guardia")
# Dentro de la función interna (wrapper_view), ocurre la magia:

# if g.user is None:: Aquí el código pregunta: "¿Hay un usuario identificado en la sesión actual?".

# return redirect(...): Si no hay un usuario (es None), el guardia no te deja pasar y te envía automáticamente a la página de inicio de sesión (auth.login).

# return view(kwargs): Si el usuario sí existe, el guardia te da el paso y ejecuta la función original que querías ver.

# 3. ¿Cómo se usa en la vida real?
# En lugar de escribir ese if en cada una de tus funciones, simplemente pones una etiqueta encima de ellas. Por ejemplo:

# Python
# @loginRequired
# def perfil_usuario():
#     return "Bienvenido a tu perfil"
# En resumen:
# ¿Tienes sesión iniciada? Entras a la función y ves el contenido.

# ¿No tienes sesión? Te expulsa y te manda al login.

# Es una forma elegante de reutilizar código y mantener tu aplicación segura sin repetir la misma validación una y otra vez.

#osea se crea esta funcion decoradora y se le pasa a las demas funciones donde necesitamos que se ejecute

# Imagina que tienes una aplicación con 20 funciones diferentes (ver perfil, editar fotos, borrar cuenta, etc.). Sin el decorador, tendrías que escribir el código de verificación de usuario dentro de cada una de esas 20 funciones. Con el decorador, solo escribes la lógica una vez.

# ¿Cómo funciona el flujo de ejecución?
# Cuando pones @loginRequired sobre una función, el flujo de tu programa cambia de una línea recta a un desvío de seguridad:

# Llamada: Intentas entrar a la función editar_perfil().

# Interceptación: El decorador se pone en medio. "¡Espera! Antes de ir a editar_perfil, pasa por aquí".

# Evaluación: Se ejecuta el if g.user is None.

# Decisión:

# Si es True: Te desvía a la página de Login. La función original editar_perfil nunca se llega a ejecutar.

# Si es False: Te deja pasar y finalmente se ejecuta editar_perfil.

# ¿Por qué se usa kwargs?
# Habrás notado que el código usa kwargs. Esto es para que el decorador sea universal.

# Algunas funciones de tu web no reciben parámetros.

# Otras reciben un id_usuario.


# ¿Por qué se usa kwargs?
# Habrás notado que el código usa kwargs. Esto es para que el decorador sea universal.

# Algunas funciones de tu web no reciben parámetros.

# Otras reciben un id_usuario.

# Otras reciben un slug_articulo.

# Al usar kwargs (y a veces también *args), le dices al decorador: "No importa qué argumentos necesite la función original, tú simplemente recíbelos todos y pásaselos cuando le des permiso de ejecutarse".