from flask import Flask , render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///remember.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Remember(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc =db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"


@app.route('/' , methods=['GET', 'POST'])
def hello_world():
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        data = Remember(title = title , desc=desc)
        db.session.add(data)
        db.session.commit()
    allData = Remember.query.all()
    return render_template('index.html' , allData = allData)

@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        update = Remember.query.filter_by(sno=sno).first()
        update.title = title
        update.desc = desc
        db.session.add(update)
        db.session.commit()
        return redirect('/')
    update = Remember.query.filter_by(sno=sno).first()
    return render_template('update.html' , update = update)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    delete = Remember.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect('/')
    


if __name__ == "__main__":
    app.run(debug=True)

   
