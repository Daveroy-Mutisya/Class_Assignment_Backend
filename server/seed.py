from datetime import datetime
import random
from uuid import uuid4
from flask import Flask
from models import db, Task, DueDate, Subtask, User  # Updated model names

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)


def seed_data():
    with app.app_context():
        # Seeding Tasks
        tasks_data = [
            {"title": "Dishes", "description": "Clean Dishes for the weekend"},
            {"title": "Shopping", "description": "For the month"}
        ]

        for task_data in tasks_data:
            task = Task(title=task_data['title'], description=task_data['description'])
            db.session.add(task)

        db.session.commit()
        print("Tasks seeded successfully")

        # Seeding Due Dates
        due_dates_data = [
            {"due_date": datetime.strptime("2024-04-15", "%Y-%m-%d")},
            {"due_date": datetime.strptime("2024-04-20", "%Y-%m-%d")}
        ]

        for due_date_data in due_dates_data:
            due_date = DueDate(due_date=due_date_data['due_date'])
            db.session.add(due_date)

        db.session.commit()
        print("Due Dates seeded successfully")

        # Seeding Subtasks
        subtasks_data = [
            {"title": "Return the clean dishes", "task_id": 1},
            {"title": "Put the groceries in the fridge", "task_id": 2}
        ]

        for subtask_data in subtasks_data:
            subtask = Subtask(title=subtask_data['title'], task_id=subtask_data['task_id'])
            db.session.add(subtask)

        db.session.commit()
        print("Subtasks seeded successfully")

        # Seeding Users
        users_data = [
            {"username": "Roy", "email": "user2@example.com", "password": "123"},
            {"username": "Abel", "email": "user3@example.com", "password" : "456"}
        ]

        for user_data in users_data:
            public_id = str(uuid4())  # Generate a new UUID for each user
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                public_id=public_id  # Include the public_id field
            )
            db.session.add(user)

        db.session.commit()
        print("Users seeded successfully")

if __name__ == "__main__":
    seed_data()
