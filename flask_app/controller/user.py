from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#login and register
@app.route('/')
def index():
    return redirect('/dash')


@app.route('/dash')
def dashboard():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if is_valid:
        pw_hash = None
        if request.form['password']:
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash,
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        print(user_id)
        return redirect('/all/recipes')
    else:
        return redirect('/')




@app.route('/login/user',methods=['POST'])
def user_login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/all/recipes')





@app.route('/all/recipes')
def all_recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    user = User.get_one(data)
    recipes = Recipe.get_all()
    return render_template('all_recipes.html',user=user,recipes=recipes)






