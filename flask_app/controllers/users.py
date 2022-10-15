from flask import render_template, request, redirect, session, url_for
from flask_app.models.user import User  #change this import line based on your extra .py file for generating OOP instances
from flask_app import app

@app.route("/list-users")     # lines 6 through 11 can be changed depending on what we need server.py to do.
def r_list_users():
    # call the get all classmethod to get all users
    session.clear()
    users = User.get_all()
    return render_template("read_all.html", users = users)

@app.route('/new')
def r_new_user():
    return render_template('create.html')

@app.route('/process_user', methods=['POST'])
def f_process_user():
    data = {
        'fname':request.form['fname'],
        'lname':request.form['lname'],
        'email':request.form['email']
    }
    if request.form['handle_type'] == 'create':
        User.add_user(data)
        return redirect('/list-users')
    elif request.form['handle_type'] == 'edit':
        data['user_id'] = session['user_id']
        User.update_user(data)
        return redirect(url_for('r_display_user', id = int(session['user_id'])))

@app.route('/user/<int:id>')
def r_display_user(id):
    user_id = id
    session['user_id'] = user_id
    data = {
        'user_id': user_id
    }
    user = User.get_one(data)
    return render_template('read_one.html', user_id = user_id, user = user )

@app.route('/edit/<int:id>')
def r_edit_user(id):
    user_id = id
    session['user_id'] = user_id
    data = {
        'user_id': user_id
    }
    user = User.get_one(data)
    return render_template('edit.html', user_id= user_id, user = user)

@app.route('/user/perm/delete/<int:id>')
def rd_delete(id):
    session['user_id'] = id
    data = {
        'user_id':session['user_id']
    }
    User.delete_user(data)
    return redirect('/list-users')