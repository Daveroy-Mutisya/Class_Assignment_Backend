from datetime import datetime
import random
from flask import Flask
from models import db, Tasks, DueDate, Subtask, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

def seed_data():
    with app.app_context():
       
        print("Seeding Tasks")

        tasks_data = [
            {"title": "Dishes", "description": "Clean Dishes for the weekend"},
            {"title": "Shopping", "description": "For the month"}
        ]

        for task_data in tasks_data:
            task = Tasks(title=task_data['title'], description=task_data['description'])
            db.session.add(task)

        db.session.commit()
        print("Tasks seeded successfully")

        print("Seeding Due Dates")

        due_dates_data = [
            {"due_date": datetime.strptime("2024-04-15", "%Y-%m-%d")},
            {"due_date": datetime.strptime("2024-04-20", "%Y-%m-%d")}
        ]

        for due_date_data in due_dates_data:
            due_date = DueDate(due_date=due_date_data['due_date'])
            db.session.add(due_date)

        db.session.commit()
        print("Due Dates seeded successfully")

        print("Seeding Subtasks")

        subtasks_data = [
            {"title": "Return the clean dishes", "task_id": 1},
            {"title": "Put the groceries in the fridge", "task_id": 2}
        ]

        for subtask_data in subtasks_data:
            subtask = Subtask(title=subtask_data['title'], task_id=subtask_data['task_id'])
            db.session.add(subtask)

        db.session.commit()
        print("Subtasks seeded successfully")

        print("Seeding Users")

        users_data = [
            {"username": "Dave", "email": "user1@example.com", "password": "456"},
            {"username": "Roy", "email": "user2@example.com", "password": "123"}
        ]

        for user_data in users_data:
            user = User(username=user_data['username'], email=user_data['email'], password=user_data['password'])
            db.session.add(user)

        db.session.commit()
        print("Users seeded successfully")

if __name__ == "__main__":
    seed_data()
