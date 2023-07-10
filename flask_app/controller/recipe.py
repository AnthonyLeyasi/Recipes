from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#create a new recipe
@app.route('/new/recipe')
def new_user():
    return render_template('new_recipe.html')



@app.route('/recipes/new/made', methods=['POST'])
def process_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')

    form_data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30'],
    }
    Recipe.save(form_data)
    return redirect('/all/recipes')

#Delete Recipe
@app.route('/destroy/recipe/<int:id>')
def delete(id):
    Recipe.destroy({'id': id})
    return redirect('/all/recipes')


#View Recipe
@app.route('/view/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    return render_template('view_recipe.html',recipe=Recipe.get_by_id({'id': id}))

#Edit Recipe
@app.route('/recipe/edit/<int:id>')
def edit_ninja(id):
    recipe = Recipe.get_one({'id':id})
    return render_template('edit_recipe.html', recipe=recipe)





@app.route('/recipes/edit/<int:id>', methods=['POST'])
def process_edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/edit/{id}')

    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30'],
    }
    Recipe.update(data)
    return redirect('/all/recipes')

