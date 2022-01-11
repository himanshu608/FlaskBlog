from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import current_user,login_required
views = Blueprint('views', __name__)
from .models import User,Note
from . import db


@views.route('/',methods=['GET', 'POST'])
@login_required
def homepage():
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']

        if len(title) <3 :
            flash('title is too short', category='error')
        elif len(blog) <10:
            flash('blog is too short', category='error')
        else:
            new_note = Note(title=title,blog=blog,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('new note added', category='success')
            return redirect(url_for('views.blogs'))
    
    return render_template('home.html',user=current_user)


@views.route('/blogs')
@login_required
def blogs():
    return render_template('blogs.html',user=current_user)



@views.route('/deleteblog/<int:id>',methods=['GET'])
@login_required

def deleteblogs(id):
    blog = Note.query.filter_by(id=id).first()
    if blog:
        if blog.user_id == current_user.id:
            db.session.delete(blog)
            db.session.commit()
    return redirect(url_for('views.blogs'))


@views.route('/updateblog/<int:id>',methods=['GET','POST'])
@login_required
def updateblog(id):
    blog = Note.query.filter_by(id=id).first()
    if request.method == 'POST':
        if blog:
            if blog.user_id == current_user.id:
                blog.title = request.form['title']
                blog.blog = request.form['blog']
                db.session.add(blog)
                db.session.commit()
                return redirect(url_for('views.blogs'))
    return render_template('blogedit.html',user=current_user,blog=blog)