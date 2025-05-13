from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        new_user = User(name=name, age=int(age))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('view_users'))
    return render_template('add_user.html')

@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@app.route('/')
def home():
    return redirect(url_for('view_users'))

if __name__ == '__main__':
    app.run(debug=True)
