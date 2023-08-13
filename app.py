from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///todo.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db=SQLAlchemy(app)


class Task(db.Model):
    id= db.Column('id',db.Integer ,primary_key=True )
    name=db.Column("name",db.String(50))
    task=db.Column("task",db.String(100))
    date_joined=db.Column("date_joined",db.Date,default =datetime.utcnow)
    
    def __repr__(self)->str:
        return f"{self.name} {self.task}"
    
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        name1=request.form['name']
        taskname=request.form['task']
        task = Task(name=name1,task=taskname)
        db.session.add(task)
        db.session.commit()
       
    task = Task.query.all()
    return render_template('index.html' ,task=task)

@app.route('/show')
def about():
    task = Task.query.all()
    print(task)
    return render_template('index.html' ,task=task)

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
     if request.method=='POST':
        name1=request.form['name']
        taskname=request.form['task']
        task = Task.query.filter_by(id=id).first()
        task.name=name1
        task.task=taskname;
        db.session.add(task)
        db.session.commit()
        return redirect('/')
     task = Task.query.filter_by(id=id).first()
     return render_template('update.html' ,task=task)


if __name__=="__main__":
    app.run(debug=True,port=5000)
