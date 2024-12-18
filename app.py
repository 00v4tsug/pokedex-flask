import os
from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'pokedex'

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:5432/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pokedex(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(300), nullable=False)

    def __init__(self, nome, imagem, descricao, tipo):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.tipo = tipo

@app.route('/')
def index():
    pokedex = Pokedex.query.all()
    return render_template('index.html', pokedex=pokedex)

@app.route('/new', methods=['GET', 'POST'])
def new():
   if request.method == 'POST':
      pokemon = Pokedex(
         request.form['nome'],
         request.form['imagem'],
         request.form['descricao'],
         request.form['tipo']
      )
      db.session.add(pokemon)
      db.session.commit() 
      flash('Projeto criado com sucesso!')
      return redirect('/') 

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
   pokemon = Pokedex.query.get(id)
   pokedex = Pokedex.query.all()
   if request.method == "POST":
      pokemon.nome = request.form['nome']
      pokemon.descricao = request.form['descricao']
      pokemon.imagem = request.form['imagem']
      pokemon.tipo = request.form['tipo']
      db.session.commit() 
      return redirect('/')
   return render_template('index.html', pokemon=pokemon, pokedex=pokedex) 

@app.route('/<id>')
def get_by_id(id):
   pokemonDelete = Pokedex.query.get(id) 
   pokedex = Pokedex.query.all()
   return render_template('index.html', pokemonDelete=pokemonDelete, pokedex=pokedex)

@app.route('/delete/<id>') 
def delete(id):
   pokemon = Pokedex.query.get(id) 
   db.session.delete(pokemon) 
   db.session.commit() 
   return redirect('/')

@app.route('/filter', methods=['GET', 'POST']) 
def filter():
   tipo = request.form['search']
   pokedex = Pokedex.query.filter(Pokedex.tipo.ilike(f'%{tipo}%')).all()
   return render_template('index.html', pokedex=pokedex)

@app.route('/filter/<param>') 
def filter_by_param(param):
   pokedex = Pokedex.query.filter_by(tipo=param).all()
   return render_template('index.html', pokedex=pokedex)

if __name__ == '__main__':
   with app.app_context():
      db.create_all()
      app.run(host='0.0.0.0', port=5000, debug=True)
