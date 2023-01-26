from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy # Importando
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db' # Configurando e dizendo ao app qual banco utilizar

db = SQLAlchemy(app)
class Books(db.Model): # Inicializando o modelo de Banco de dados
    """
    ID: Número auto-incrementado.
    Titulo: String grande, nome do livro
    Adl = Data de publicação do livro
    """
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(150))
    adl = db.Column(db.DateTime)
    def __init__(self, titulo, adl):
        self.titulo = titulo
        self.adl = adl


@app.route('/')
def index():
    """
    Utilizado apenas para redirecionar a página principal: Home
    """
    return redirect(url_for('home'))

@app.route('/home')
def home():
    bks = Books.query.all() # Procurando todos os livros para visualização
    return render_template('home.html', books=bks) # Retornando ao template com os livros.

@app.route('/home',methods=['POST'])
def create_book():
    # Se a requisição (na mesma página), for POST, criar um novo livro
    if request.method == 'POST':
        book = Books(request.form['title'],datetime.strptime(request.form['data'], '%Y-%m-%d')) # Pegando dados do formulário, convertendo data de HTML, para data comum em PYTHON
        db.session.add(book)
        db.session.commit()
        # Adicionando, atualizando e redirecionando a nova home, com o novo livro
        return redirect(url_for("home"))

@app.route("/delete/<id>")
def delete_book(id):
    # Primeiro fazendo um FIND, pelo ID ÚNICO, para assim que achar, deletar e atualizar, redirecionando para a nova home com o livro deletado.
    find_book = Books.query.filter_by(id=id).first()
    db.session.delete(find_book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)