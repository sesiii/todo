from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import redirect

app = Flask(__name__) # create an instance of the Flask class
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # configure the database
db=SQLAlchemy(app) # create an instance of the SQLAlchemy class

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
with app.app_context():
    db.create_all()

@app.route('/',methods=['POST','GET']) # use the route() decorator to tell Flask what URL should trigger our function
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')# use the route() decorator to tell Flask what URL should trigger our function
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)# get the task by id

    try:
        db.session.delete(task_to_delete)# delete the task
        db.session.commit()# commit the changes to the database
        return redirect('/')# redirect to the home page
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])# use the route() decorator to tell Flask what URL should trigger our function
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update = Todo.query.get_or_404(id)
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        task = Todo.query.get_or_404(id)
        return render_template('update.html', task=task)

if __name__=="__main__":
    app.run(debug=True) # run the application