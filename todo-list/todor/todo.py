#archivo para las vistas de la aplicacion, utilizamos Blueprint para organizarlas, estas vistas con blueprint se deben de registrar en el archivo de configuracion __init__.py


from flask import Blueprint, render_template, request,redirect,url_for,g
from todor.auth import loginRequired
from .models import Todo,User
from todor import db

#instancia de blueprint,este es el prefijo para las demas rutas
bp=Blueprint("todo",__name__,url_prefix="/todo")


#ruta /list
@bp.route("/list")
@loginRequired
def index():
    todos=Todo.query.all()
    return render_template("todo/index.html", todos=todos)

#ruta /create
@bp.route("/create", methods=("GET","POST"))
@loginRequired
def create():
    #capturamos los datos del formulario de crear tarea
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]

        #creamos la tarea pasandole los datos capturados y el id del usuario
        todo=Todo(g.user.id, title,desc)

        #guardamos la tarea en la bd y redireccionamos al formulario
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo.index"))

    return render_template("todo/create.html")


#esta funcion nos captura una tarea por su id para poder editarla
def get_todo(id):
    todo=Todo.query.get_or_404(id)
    return todo

#esta ya es la vista para editar
@bp.route("/update/<int:id>", methods=("GET","POST"))
@loginRequired
def update(id):
    #usamos nuestra funcion get_todo
    todo=get_todo(id)
     #capturamos los datos del formulario de crear tarea usando nuestro objeto todo creado con la funcion get_todo y con el estado en True simplemente se guardan esos nuevos datos en la bd
    if request.method=="POST":
        todo.title=request.form["title"]
        todo.desc=request.form["desc"]
        todo.state= True if request.form.get("state")=="on" else False
        db.session.commit()
        return redirect(url_for("todo.index"))
    
    return render_template("todo/update.html", todo=todo)


#funcion para eliminar tarea
@bp.route("/delete/<int:id>")
@loginRequired
def delete(id):
    #usamos nuestra funcion get_todo para capturar la tarea a eliminar y despues redireccionamos a la lista de tareas
    todo=get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))