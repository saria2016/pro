from flask import Flask, abort, flash, render_template, request, jsonify
from models import storage
import bcrypt
import json
import requests
from models.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'os.urandom(32)'  # Replace with your secret key


@app.teardown_appcontext
def teardown_db(exception):
    """Close the database at the end of the request."""
    storage.close()

@app.route('/', strict_slashes=False)
@app.route('/login', strict_slashes=False)
def index():
    """The homepage of the application."""    
    return render_template('login.html')
  
  
@app.route('/login/user', methods=['POST'], strict_slashes=False)
def login_user():
    """Render the Login page."""
    url = "http://127.0.0.1:5100/api/v1/users/verify"
    print("Debug is here")  
    if "email" not in request.form or "password" not in request.form:
      abort(400)    
    email = request.form['email']
    password = request.form['password']    
    obj = {
        'email': email,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=obj, headers=headers)
    print("Hi", response.status_code)
    if response.status_code == 201:
        # just remember, we need to render this page base on his credentials
        flash("Successfully logged in", "success")
        user_id = response.json().get('id')
        user_obj = storage.get(User, user_id)
        print(user_obj.id)
        print(user_obj.name)
        print(user_obj.email)        
        return render_template('tasks.html', user_obj=user_obj)
    else:
        flash("Wrong email or password")
        return render_template('login.html')
    
@app.route('/register', strict_slashes=False)
def register():
    """Render the Register page."""
    return render_template('register.html')

@app.route('/register/new', methods=['POST'], strict_slashes=False)
def register_new():
    """Render the Register page."""
    # data = request.form.json()
    # name = data.get('name')
    # email = data.get('email')
    # password = data.get('password')
    # confirm_password = data.get('confirm_password')
    # or
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash("Password mismatch", "danger")
        return "Password mismatch", (400)
    obj = {
        'name': name,
        'email': email,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = "http://127.0.0.1:5100/api/v1/users"
    response = requests.post(url, json=obj, headers=headers)
    if response.status_code == 201:
        flash("Successfully registered", "success")
        return render_template('login.html')
    else:
        flash("Email already exists", "danger")
        return render_template('login.html')

@app.route('/update_user/<user_id>', methods=['POST'], strict_slashes=False)
def update_user(user_id):
    """Create a new instance of user."""
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    url = f"http://127.0.0.1:5100/api/v1/users/{user_id}"
    obj = {
        'name': name,
        'email': email,
        'password': password
        }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.put(url, json=obj, headers=headers)
    if response.status_code == 200:
        flash("Profile Successfully updated", "success")
        return render_template('tasks.html', user_id=user_id)
    else:
        flash("Faile to update credentials", "danger")
        return render_template('login.html')
    pass
    

@app.route('/tasks', strict_slashes=False)
def tasks():
    """Render the Task page."""
    return render_template('tasks.html')


@app.route('/add_tasks', strict_slashes=False)
def add_task():
  """ Render the task page for Adding a new obj insance"""
  return render_template('tasks.html')


# @app.route('/create_task', methods=['POST'], strict_slashes=False)
# def create_task():
#   """Get the properties of this new obj instance of task create this obj via API"""



@app.route('/edit_task/<task_id>', strict_slashes=False)
def edit_task(task_id):
  """Render the edit page with necessary information to Edit a task."""
  return render_template('edit_task.html')

@app.route('/update_task/<task_id>', methods=['POST'], strict_slashes=False)
def update_task(task_id):
  """Edit a task and send this update to the database using API."""
  return render_template('tasks.html')
 

  
@app.route('/delete_task/<task_id>', methods=['GET'], strict_slashes=False)
def delete_task(task_id):
  """Delete a task."""
  return render_template('tasks.html')



if __name__ == '__main__':
    app.run(debug=True)
