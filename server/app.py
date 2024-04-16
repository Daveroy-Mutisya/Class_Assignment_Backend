from functools import wraps
from uuid import uuid4
from flask import Flask, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Tasks, DueDate, Subtask, User
from pyjwt_lib import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = '886738700dab460b90091e196b99dfa5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)  # Initialize db with Flask app

# Database creation and initialization
# with app.app_context():
#     db.create_all()


# Token required decorator
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            session['user'] = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Invalid Token!'}), 401
        return func(*args, **kwargs)
    return decorated

@app.route('/', methods=["GET"])
def index():
    return f"Hello World! The server is running."

# Registration route
@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")  
    if not username or not password or not email:  
        return jsonify({"message": "Missing username, email, and/or password"}), 400
    
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "User already exists."}), 400

    new_user = User(username=username, email=email, public_id=str(uuid4()))  
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully.", "public_id": new_user.public_id})


# Login Route
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Username or Password incorrect"})

    token = jwt.encode({'public_id': user.public_id}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({"token": token})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

# Route to create a new task
@app.route('/tasks', methods=['POST'])
@token_required
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    new_task = Tasks(title=title, description=description)
    if due_date:
        new_due_date = DueDate(due_date=due_date)
        new_task.due_date = new_due_date

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Tasks.query.all()
    if not tasks:
        return jsonify({'error': 'No tasks found'}), 404
    task_list = [{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks]
    return jsonify(task_list)


# Route to get a specific task by ID

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first_or_404()
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.due_date if task.due_date else None
    }
    return jsonify(task_data)


@app.route("/tasks/<string:task_name>", methods =['GET'])
def search_by_name(task_name):
    result = Tasks.search_by_name(task_name)
    output = []
    
    # If the search returned multiple entries, iterate through them and add to list
    if len(result)>1:
        for item in result:
            output.append({"ID":item[0], "Name":item[1]})  
    elif result:
        # If only one entry was found, just send that back as a dictionary instead of a list
        output.append(output[0])
        
    return jsonify(output)

# Route to update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    task = task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    due_date = data.get('due_date')
    if due_date:
        if task.due_date:
            task.due_date.due_date = due_date
        else:
            new_due_date = DueDate(due_date=due_date)
            task.due_date = new_due_date

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

# Route to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    task = task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

# Route to create a new subtask for a task
@app.route('/tasks/<int:task_id>/subtasks', methods=['POST'])
@token_required
def create_subtask(task_id):
    task = task.query.get_or_404(task_id)
    data = request.get_json()
    title = data.get('title')
    # Check if the task exists
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    # Create the subtask
    new_subtask = Subtask(title=title, task_id=task_id)
    db.session.add(new_subtask)
    db.session.commit()
    return jsonify({'message': 'Subtask created successfully'}), 201


# Route to get all subtasks for a task
@app.route('/tasks/<int:task_id>/subtasks', methods=['GET'])
def get_all_subtasks(task_id):
    task = Tasks.query.get_or_404(task_id)
    # Check if the task exists
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    subtasks = Subtask.query.filter_by(task_id=task_id).all()
    subtask_list = [{'id': subtask.id, 'title': subtask.title} for subtask in subtasks]
    return jsonify(subtask_list)


# Route to get a specific subtask by ID
@app.route('/subtasks/<int:subtask_id>', methods=['GET'])
def get_subtask(subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    return jsonify({'id': subtask.id, 'title': subtask.title, 'task_id': subtask.task_id})

# Route to update a subtask
@app.route('/subtasks/<int:subtask_id>', methods=['PUT'])
@token_required
def update_subtask(subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    data = request.get_json()
    subtask.title = data.get('title', subtask.title)
    db.session.commit()
    return jsonify({'message': 'Subtask updated successfully'})

# Route to delete a subtask
@app.route('/subtasks/<int:subtask_id>', methods=['DELETE'])
@token_required
def delete_subtask(subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return jsonify({'message': 'Subtask deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
