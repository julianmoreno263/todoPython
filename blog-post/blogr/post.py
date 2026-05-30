from cmath import log

from flask import Blueprint,request,flash,redirect,url_for,g,render_template
from .auth import login_required
from .models import Post
from blogr import db

# 1. Definimos el Blueprint
bp=Blueprint("post",__name__,url_prefix="/post")

#2-creamos las vistas que despues se importaran en __init__.py
@bp.route("/posts")
@login_required
def posts():
    #recuperamos todos los post
    posts=Post.query.all()
    return render_template("admin/posts.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    #capturamos los datos del formulario
    if request.method=="POST":
        url=request.form.get("url")
        url=url.replace(" ","-") # type: ignore
        title=request.form.get("title")
        info=request.form.get("info")
        content=request.form.get("ckeditor")

        #creamos objeto de tipo Post
        post=Post(g.user.id,url,title,info,content)

        error=None

        #comparamos la url del post actual con los existentes, si existe no guardamos,si no existe lo guardamos en la bd
        post_url=Post.query.filter_by(url=url).first()

        if post_url==None:
            db.session.add(post)
            db.session.commit()
            flash(f"El blog {post.title} se registro correctamente")
            return redirect(url_for("post.posts"))
        else:
            error=f"La URL {url} ya está registrada"
        flash(error)
    return render_template("admin/create.html")

@bp.route("/update<int:id>", methods=("GET","POST"))
@login_required
def update(id):
    #creamos objeto Post con su id
    post=Post.query.get_or_404(id)

    #capturamos los datos del post editados, la url no se modifica
    if request.method=="POST":
        post.title=request.form.get("title")
        post.info=request.form.get("info")
        post.content=request.form.get("ckeditor")

        #guardamos los datos editados en la bd
        db.session.commit()
        flash(f"El blog {post.title} se actualizó correctamente")
        return redirect(url_for("post.posts"))

    return render_template("admin/update.html",post=post)


@bp.route("/delete<int:id>")
@login_required
def delete(id):
    #creamos objeto Post con su id
    post=Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash(f"El blog {post.title} se eliminó correctamente")
    return redirect(url_for("post.posts"))
