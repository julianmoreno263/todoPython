#archivo para el modelo de la base de datos, aqui usamos el orm sqlalchemy para trabajar con python las db y en segundo plano el orm lo que hace es realizar las consultas sql.

#NOTA: para hacer las pruebas a la bd usamos la flask shell, podemos abrir una nueva terminal y vamos a nuestro proyecto,activamos el entorno y ponemos:  flask --app todor shell  y se abre la shell de python en la carpeta instance que es donde esta nuestra bd. Para esto,ya dentro de la shell lo que hacemos es importar los modelos de la bd asi: from nombreAplicacion.models import "aqui van los modelos creados", y tambien el objeto db asi: from todor import db.  Ya con esto podemos por ejemplo crear un usuario utilizando python,usamos los modelos: user=User(parametros)

from todor import db


#creamos la clase para usuarios que hereda de db.Model
class User(db.Model):
    #creamos los campos para la tabla user
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.Text,nullable=False)

    #creamos un constructor para poder crear objetos de esta clase
    def __init__(self,username,password) -> None:
        self.username=username
        self.password=password

    #metodo para poder mostrar los datos, El método __repr__ es uno de los llamados "métodos mágicos" (o dunder methods) de Python. Su nombre viene de "representation" y su objetivo es definir cómo se debe mostrar un objeto cuando lo imprimes en la consola o lo inspeccionas durante la depuración.

    # Aquí te explico exactamente qué está haciendo en tu caso:

    # 1. ¿Para qué sirve?
    # Por defecto, si no defines este método, cuando intentas imprimir un objeto de tu clase (por ejemplo, un usuario de tu base de datos), Python te mostrará algo feo e ilegible como esto:
    # <todor.models.User object at 0x0000021A4B8>

    # Al definir __repr__, le dices a Python: "Oye, cuando alguien vea este objeto, muéstralo de esta forma clara".
    def __repr__(self) -> str:
        return f"<User: {self.username}>"
    




#creamos la clase o modelo para la lista de tareas,la relacion es que un usuario puede tener varias tareas,osea es de uno a muchos
class Todo(db.Model):
    #creamos los campos para la tabla user
    id=db.Column(db.Integer,primary_key=True)
    created_by=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    title=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.Text)
    state=db.Column(db.Boolean,default=False)#valor por defecto false porque al crear la tarea no esta completada

    #creamos un constructor para poder crear objetos de esta clase
    def __init__(self,created_by,title,desc,state=False) -> None:
        self.created_by=created_by
        self.title=title
        self.desc=desc
        self.state=state

    def __repr__(self) -> str:
        return f"<Todo: {self.title}>"



