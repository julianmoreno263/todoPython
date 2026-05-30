

#con Blueprint importamos vistas de forma mas facil, En el ecosistema de Flask, un Blueprint es una forma de organizar tu aplicación en componentes más pequeños y reutilizables. Si piensas en Flask como una caja de herramientas, el Blueprint es el separador que mantiene los destornilladores en un lado y las llaves en otro.

# A medida que tu aplicación crece, poner todas las rutas en un solo archivo app.py se vuelve un caos. Aquí es donde entran los Blueprints.

#¿Para qué sirve exactamente?
# La función principal de un Blueprint es la modularidad. Sus propósitos clave son:

# Organización Estructural: Permite dividir una aplicación grande en secciones lógicas (ej. auth, admin, api, blog).

# Escalabilidad: Facilita el trabajo en equipo, ya que cada desarrollador puede trabajar en un archivo de Blueprint distinto sin generar conflictos constantes.

# Reutilización: Puedes definir un Blueprint (como un sistema de comentarios) y llevarlo de un proyecto a otro fácilmente.

# Prefijos de URL: Permite agrupar rutas bajo un mismo camino. Por ejemplo, todas las rutas del Blueprint admin pueden empezar automáticamente con /admin/.

#Ejemplo de uso
# Imagina que tienes un módulo para el panel de usuario. En lugar de ensuciar el archivo principal, creas user_panel.py:

# Python
# from flask import Blueprint

# # 1. Definimos el Blueprint
# user_bp = Blueprint('user', __name__, url_prefix='/user')

# @user_bp.route('/profile')
# def profile():
#     return "Este es el perfil del usuario"

# @user_bp.route('/settings')
# def settings():
#     return "Configuración de cuenta"
# Luego, en tu archivo principal app.py:

# Python
# from flask import Flask
# from user_panel import user_bp

# app = Flask(__name__)

# # 2. Registramos el Blueprint
# app.register_blueprint(user_bp)
# Ahora, aunque en el Blueprint definiste la ruta como /profile, al registrarla con el prefijo /user, la URL final será tu_[dominio.com/user/profile](https://dominio.com/user/profile).

from flask import Blueprint,render_template,request
from .models import User,Post

# 1. Definimos el Blueprint
bp=Blueprint("home",__name__)

def get_user(id):
    user=User.query.get_or_404(id)
    return user

#metodo para implementar en el buscador de la app
def search_posts(query):
    #con esta consulta lo que traemos es una lista con la o las palabras que hagan match con nuestra busqueda para esto utilizamos el filtro y con el metodo ilike() le pasamos ese texto que queremos que busque,el buscara en el titulo del post si la palabra que ingresamos esta en el titulo y nos devuelve las coincidencias.
    posts=Post.query.filter(Post.title.ilike(f"%{query}%")).all() # type: ignore
    return posts


#2-creamos las vistas que despues se importaran en __init__.py
@bp.route("/",methods=("GET","POST"))
def index():
    #recuperamos los post y los enviamos a la plantilla para mostrarlos
    posts=Post.query.all()

    #aqui recuperamos el dato que enviamos desde el buscador de la app en su campo search, y ese dato recuperado es el que le pasamos como parametro a la funcion search_posts que buscara las coincidencias y nos traera los posts,la variable value="hidden" nos sirve para ocultar en la pagina principal la seccion que dice bienvenidos al blog,para que cuando busquemos algo en el buscador solo aparezcan los resultados nada mas.
    if request.method=="POST":
        query=request.form.get("search")
        posts=search_posts(query)
        value="hidden"
        return render_template("index.html",posts=posts, get_user=get_user,value=value)

    return render_template("index.html",posts=posts, get_user=get_user)

@bp.route("/blog/<url>")
def blog(url):
    #cuando queramos mostrar un blog especifico lo buscaremos por la url
    post=Post.query.filter_by(url=url).first()
    return render_template("blog.html",post=post , get_user=get_user)




