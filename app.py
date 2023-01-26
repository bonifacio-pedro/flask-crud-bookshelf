from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy # Importando
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db' # Configurando e dizendo ao app qual banco utilizar

db = SQLAlchemy(app)
class Books(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(150))
    adl = db.Column(db.DateTime)
    def __init__(self, titulo, adl):
        self.titulo = titulo
        self.adl = adl


@app.route('/')
def index():
   return redirect(url_for('home'))

@app.route('/home')
def home():
    bks = Books.query.all()
    print(bks)
    return render_template('home.html', books=bks)

@app.route('/home',methods=['POST'])
def create_book():
    if request.method == 'POST':
        book = Books(request.form['title'],datetime.strptime(request.form['data'], '%Y-%m-%d'))
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/delete/<id>")
def delete_book(id):
    find_book = Books.query.filter_by(id=id).first()
    db.session.delete(find_book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
   
    app.run(debug=True)