from flask import Blueprint,render_template,request,flash,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Note
from . import db
from flask_login import current_user,login_user,logout_user,login_required
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user :
            if check_password_hash(user.password, password):
                flash('Logged in successfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Invalid password try again',category='error')
        else:
            flash('User does not exist',category='error')
    return render_template('login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if user :
            flash('User already exists',category='error')

        elif len(name) < 3:
            flash('name must be at least 3 characters long',category='error')
        elif len(password1) < 6 or len(password2) <6 :
            flash('password must be at least 6 characters long',category='error')
        elif password1 != password2:
            flash('password does not match',category='error')
        else :
            new_user = User(name=name,email=email,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created !!',category='success')
            login_user(new_user,remember=True)
            return redirect(url_for('views.homepage'))
    return render_template('signup.html',user=current_user)