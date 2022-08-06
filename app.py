
from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mmlvotvldfsess:6dc99dcb5f5ef404d5e9fbd15d31b515906008f2fe3abdb8ca6e94793a4ec0e0@ec2-34-235-31-124.compute-1.amazonaws.com:5432/ddru3rd8809buu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean)
    dueDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Description ID: {self.id}, name: {self.description}>'


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


@app.route('/tasks/create', methods=['POST'])
def create_task():
    error = False
    body = {}
    try:
        dueDate = request.form.get_json()['due-date']
        task = request.form.get_json()['description']
        todo = Todo(description=task, dueDate=dueDate)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        body['due-date'] = todo.dueDate

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

    # finally:
    #     db.session.close()
    #     return redirect(url_for('index'))
        # if not error:
        #     return jsonify(body)


# updating task
@app.route('/tasks/<taskId>/set-completed', methods=['POST'])
def set_completed(taskId):

    try:
        task_completed = request.form.get_json()['completed']
        todo = Todo.query.get(taskId)
        print(todo)
        todo.completed = task_completed

        db.session.commit()

    except:

        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    return redirect(url_for('index'))


# deleting task
@app.route('/tasks/<taskId>/delete', methods=['GET'])
def delete_task(taskId):

    try:

        Todo.query.filter_by(id=taskId).delete()

        db.session.commit()

    except:

        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    return redirect(url_for('index'))
