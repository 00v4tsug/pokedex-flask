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

def inserir_pokemons():
   if Pokedex.query.count() == 0:
      pokemons = [
            Pokedex(nome='Bulbasaur', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/001.png', tipo='Planta e Venenoso', descricao='Um Pokémon pequeno com uma planta nas costas.'),
            Pokedex(nome='Ivysaur', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/002.png', tipo='Planta e Venenoso', descricao='Quando a flor na sua costa floresce, significa que ele está pronto para evoluir.'),
            Pokedex(nome='Venusaur', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/003.png', tipo='Planta e Venenoso', descricao='Possui uma enorme flor na costa que exala um aroma doce.'),
            Pokedex(nome='Charmander', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/004.png', tipo='Fogo', descricao='O Pokémon que solta fogo quando feliz.'),
            Pokedex(nome='Charmeleon', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/005.png', tipo='Fogo', descricao='Se fica muito irritado, a chama na sua cauda queima com mais intensidade.'),
            Pokedex(nome='Charizard', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/006.png', tipo='Fogo e Voador', descricao='Se Charizard ficar realmente irritado, a chama na ponta de sua cauda queima em um tom azul claro.'),
            Pokedex(nome='Squirtle', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/007.png', tipo='Água', descricao='Ele pode usar a água que armazena na sua concha para se defender.'),
            Pokedex(nome='Wartortle', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/008.png', tipo='Água', descricao='Ele é conhecido por ser um Pokémon que se preocupa com sua aparência.'),
            Pokedex(nome='Blastoise', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/009.png', tipo='Água', descricao='Possui canhões que dispara água com força devastadora.'),
            Pokedex(nome='Caterpie', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/010.png', tipo='Inseto', descricao='É um Pokémon pequeno que se alimenta de folhas.'),
            Pokedex(nome='Metapod', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/011.png', tipo='Inseto', descricao='Um Pokémon que se transforma em Butterfree.'),
            Pokedex(nome='Butterfree', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/012.png', tipo='Inseto e Voador', descricao='Conhecido por seu pólen e sua bela aparência.'),
            Pokedex(nome='Weedle', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/013.png', tipo='Inseto e Venenoso', descricao='Um Pokémon pequeno que pode envenenar seus oponentes.'),
            Pokedex(nome='Kakuna', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/014.png', tipo='Inseto e Venenoso', descricao='Um Pokémon que está em transformação para se tornar Beedrill.'),
            Pokedex(nome='Beedrill', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/015.png', tipo='Inseto e Venenoso', descricao='Possui um ferrão venenoso.'),
            Pokedex(nome='Pidgey', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/016.png', tipo='Normal e Voador', descricao='Um Pokémon comum que pode ser encontrado em muitos lugares.'),
            Pokedex(nome='Pidgeotto', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/017.png', tipo='Normal e Voador', descricao='Um Pokémon que se torna mais forte com o tempo.'),
            Pokedex(nome='Pidgeot', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/018.png', tipo='Normal e Voador', descricao='O Pokémon mais poderoso de sua linha evolutiva.'),
            Pokedex(nome='Rattata', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/019.png', tipo='Normal', descricao='Um Pokémon pequeno que se esconde em buracos.'),
            Pokedex(nome='Raticate', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/020.png', tipo='Normal', descricao='Um Pokémon que pode ser muito feroz quando ameaçado.'),
            Pokedex(nome='Spearow', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/021.png', tipo='Normal e Voador', descricao='Um Pokémon que gosta de viver em grandes grupos.'),
            Pokedex(nome='Fearow', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/022.png', tipo='Normal e Voador', descricao='É conhecido por sua velocidade e força.'),
            Pokedex(nome='Ekans', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/023.png', tipo='Venenoso', descricao='Um Pokémon que pode se esconder em lugares apertados.'),
            Pokedex(nome='Arbok', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/024.png', tipo='Venenoso', descricao='Um Pokémon que pode ser muito agressivo quando ameaçado.'),
            Pokedex(nome='Pikachu', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/025.png', tipo='Elétrico', descricao='O Pokémon mascote da franquia, conhecido por seu poder elétrico.'),
            Pokedex(nome='Raichu', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/026.png', tipo='Elétrico', descricao='A evolução final de Pikachu.'),
            Pokedex(nome='Sandshrew', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/027.png', tipo='Terra', descricao='Um Pokémon que se esconde sob a areia.'),
            Pokedex(nome='Sandslash', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/028.png', tipo='Terra', descricao='Possui espinhos que pode usar para se defender.'),
            Pokedex(nome='Nidoran♀', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/029.png', tipo='Venenoso', descricao='Um Pokémon pequeno que é um ótimo companheiro.'),
            Pokedex(nome='Nidorina', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/030.png', tipo='Venenoso e Terra', descricao='Um Pokémon que é conhecido por sua força.'),
            Pokedex(nome='Nidoqueen', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/031.png', tipo='Venenoso e Terra', descricao='Um Pokémon muito poderoso com habilidades defensivas.'),
            Pokedex(nome='Nidoran♂', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/032.png', tipo='Venenoso', descricao='Um Pokémon pequeno que pode ser muito gentil.'),
            Pokedex(nome='Nidorino', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/033.png', tipo='Venenoso', descricao='Um Pokémon que é muito ágil.'),
            Pokedex(nome='Nidoking', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/034.png', tipo='Venenoso e Terra', descricao='Um Pokémon muito forte e temido.'),
            Pokedex(nome='Clefairy', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/035.png', tipo='Fada', descricao='Um Pokémon que gosta de dançar à luz da lua.'),
            Pokedex(nome='Clefable', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/036.png', tipo='Fada', descricao='É conhecido por ser um Pokémon muito feliz.'),
            Pokedex(nome='Vulpix', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/037.png', tipo='Fogo', descricao='Um Pokémon que tem uma linda pelagem.'),
            Pokedex(nome='Ninetales', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/038.png', tipo='Fogo', descricao='Um Pokémon conhecido por sua beleza e poder.'),
            Pokedex(nome='Jigglypuff', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/039.png', tipo='Normal e Fada', descricao='Um Pokémon que gosta de cantar para adormecer os outros.'),
            Pokedex(nome='Wigglytuff', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/040.png', tipo='Normal e Fada', descricao='Um Pokémon que pode ser muito persistente.'),
            Pokedex(nome='Zubat', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/041.png', tipo='Venenoso e Voador', descricao='Um Pokémon que vive em cavernas.'),
            Pokedex(nome='Golbat', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/042.png', tipo='Venenoso e Voador', descricao='Um Pokémon que se alimenta de sangue.'),
            Pokedex(nome='Oddish', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/043.png', tipo='Planta e Venenoso', descricao='Um Pokémon que se esconde à sombra das plantas.'),
            Pokedex(nome='Gloom', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/044.png', tipo='Planta e Venenoso', descricao='Um Pokémon que tem um odor forte.'),
            Pokedex(nome='Vileplume', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/045.png', tipo='Planta e Venenoso', descricao='Possui uma enorme flor que exala um aroma doce.'),
            Pokedex(nome='Paras', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/046.png', tipo='Inseto e Planta', descricao='Um Pokémon que se esconde sob os fungos.'),
            Pokedex(nome='Parasect', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/047.png', tipo='Inseto e Planta', descricao='Um Pokémon que controla fungos.'),
            Pokedex(nome='Venonat', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/048.png', tipo='Inseto e Venenoso', descricao='Um Pokémon que pode envenenar seus oponentes.'),
            Pokedex(nome='Venomoth', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/049.png', tipo='Inseto e Venenoso', descricao='Um Pokémon que pode usar seu pólen como arma.'),
            Pokedex(nome='Diglett', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/050.png', tipo='Terra', descricao='Um Pokémon que vive em buracos.'),
            Pokedex(nome='Dugtrio', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/051.png', tipo='Terra', descricao='Um Pokémon que se move rapidamente sob a terra.'),
            Pokedex(nome='Meowth', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/052.png', tipo='Normal', descricao='Um Pokémon que é conhecido por sua astúcia.'),
            Pokedex(nome='Persian', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/053.png', tipo='Normal', descricao='Um Pokémon elegante e rápido.'),
            Pokedex(nome='Psyduck', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/054.png', tipo='Água', descricao='Um Pokémon que frequentemente sofre dores de cabeça.'),
            Pokedex(nome='Golduck', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/055.png', tipo='Água', descricao='Um Pokémon que pode nadar rapidamente.'),
            Pokedex(nome='Poliwag', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/056.png', tipo='Água', descricao='Um Pokémon que se parece com um girino.'),
            Pokedex(nome='Poliwhirl', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/057.png', tipo='Água', descricao='Um Pokémon que pode nadar rapidamente.'),
            Pokedex(nome='Poliwrath', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/058.png', tipo='Água e Luta', descricao='Um Pokémon que é muito forte.'),
            Pokedex(nome='Abra', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/059.png', tipo='Psíquico', descricao='Um Pokémon que dorme muito.'),
            Pokedex(nome='Kadabra', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/060.png', tipo='Psíquico', descricao='Um Pokémon que possui habilidades psíquicas.'),
            Pokedex(nome='Alakazam', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/061.png', tipo='Psíquico', descricao='Um Pokémon com uma inteligência incrível.'),
            Pokedex(nome='Machop', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/062.png', tipo='Luta', descricao='Um Pokémon muito forte e determinado.'),
            Pokedex(nome='Machoke', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/063.png', tipo='Luta', descricao='Um Pokémon que é muito forte e pode levantar pesos enormes.'),
            Pokedex(nome='Machamp', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/064.png', tipo='Luta', descricao='Um Pokémon que possui quatro braços e é muito poderoso.'),
            Pokedex(nome='Bellsprout', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/065.png', tipo='Planta e Venenoso', descricao='Um Pokémon que pode usar sua cauda para atacar.'),
            Pokedex(nome='Weepinbell', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/066.png', tipo='Planta e Venenoso', descricao='Um Pokémon que é muito ágil.'),
            Pokedex(nome='Victreebel', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/067.png', tipo='Planta e Venenoso', descricao='Um Pokémon que usa sua habilidade para capturar presas.'),
            Pokedex(nome='Tentacool', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/068.png', tipo='Água e Venenoso', descricao='Um Pokémon que vive em águas profundas.'),
            Pokedex(nome='Tentacruel', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/069.png', tipo='Água e Venenoso', descricao='Um Pokémon que é conhecido por seu veneno.'),
            Pokedex(nome='Geodude', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/070.png', tipo='Pedra e Terra', descricao='Um Pokémon que vive em montanhas.'),
            Pokedex(nome='Graveler', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/071.png', tipo='Pedra e Terra', descricao='Um Pokémon que pode rolar muito rápido.'),
            Pokedex(nome='Golem', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/072.png', tipo='Pedra e Terra', descricao='Um Pokémon muito forte e resistente.'),
            Pokedex(nome='Ponyta', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/073.png', tipo='Fogo', descricao='Um Pokémon rápido e ágil.'),
            Pokedex(nome='Rapidash', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/074.png', tipo='Fogo', descricao='Um Pokémon conhecido por sua velocidade.'),
            Pokedex(nome='Slowpoke', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/075.png', tipo='Água e Psíquico', descricao='Um Pokémon que é conhecido por sua lentidão.'),
            Pokedex(nome='Slowbro', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/076.png', tipo='Água e Psíquico', descricao='Um Pokémon que é mais inteligente do que parece.'),
            Pokedex(nome='Magnemite', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/077.png', tipo='Elétrico e Aço', descricao='Um Pokémon que pode gerar eletricidade.'),
            Pokedex(nome='Magneton', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/078.png', tipo='Elétrico e Aço', descricao='Um Pokémon que pode criar campos magnéticos.'),
            Pokedex(nome='Farfetch\'d', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/079.png', tipo='Normal e Voador', descricao='Um Pokémon que sempre leva seu alho-poró.'),
            Pokedex(nome='Doduo', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/080.png', tipo='Normal e Voador', descricao='Um Pokémon com duas cabeças.'),
            Pokedex(nome='Dodrio', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/081.png', tipo='Normal e Voador', descricao='Um Pokémon que pode correr rapidamente.'),
            Pokedex(nome='Seel', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/082.png', tipo='Água', descricao='Um Pokémon que vive em ambientes frios.'),
            Pokedex(nome='Dewgong', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/083.png', tipo='Água e Gelo', descricao='Um Pokémon que pode nadar em águas geladas.'),
            Pokedex(nome='Grimer', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/084.png', tipo='Venenoso', descricao='Um Pokémon que vive em áreas poluídas.'),
            Pokedex(nome='Muk', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/085.png', tipo='Venenoso', descricao='Um Pokémon que é feito de sujeira.'),
            Pokedex(nome='Shellder', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/086.png', tipo='Água', descricao='Um Pokémon que se esconde em sua concha.'),
            Pokedex(nome='Cloyster', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/087.png', tipo='Água e Gelo', descricao='Um Pokémon que pode se fechar em sua concha para se proteger.'),
            Pokedex(nome='Gastly', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/088.png', tipo='Fantasma e Venenoso', descricao='Um Pokémon que se dissolve em fumaça.'),
            Pokedex(nome='Haunter', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/089.png', tipo='Fantasma e Venenoso', descricao='Um Pokémon que gosta de assustar os outros.'),
            Pokedex(nome='Gengar', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/090.png', tipo='Fantasma e Venenoso', descricao='Um Pokémon que é conhecido por suas travessuras.'),
            Pokedex(nome='Onix', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/091.png', tipo='Pedra e Terra', descricao='Um Pokémon que pode passar por rochas.'),
            Pokedex(nome='Drowzee', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/092.png', tipo='Psíquico', descricao='Um Pokémon que se alimenta de sonhos.'),
            Pokedex(nome='Hypno', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/093.png', tipo='Psíquico', descricao='Um Pokémon que pode controlar os sonhos.'),
            Pokedex(nome='Krabby', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/094.png', tipo='Água', descricao='Um Pokémon que vive na praia.'),
            Pokedex(nome='Kingler', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/095.png', tipo='Água', descricao='Um Pokémon que é conhecido por sua força.'),
            Pokedex(nome='Voltorb', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/096.png', tipo='Elétrico', descricao='Um Pokémon que se parece com uma esfera.'),
            Pokedex(nome='Electrode', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/097.png', tipo='Elétrico', descricao='Um Pokémon que pode explodir.'),
            Pokedex(nome='Exeggcute', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/098.png', tipo='Planta e Psíquico', descricao='Um Pokémon que se parece com ovos.'),
            Pokedex(nome='Exeggutor', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/099.png', tipo='Planta e Psíquico', descricao='Um Pokémon que tem várias cabeças.'),
            Pokedex(nome='Cubone', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/100.png', tipo='Terra', descricao='Um Pokémon que usa um osso como arma.'),
            Pokedex(nome='Marowak', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/101.png', tipo='Terra', descricao='Um Pokémon que é conhecido por sua coragem.'),
            Pokedex(nome='Hitmonlee', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/102.png', tipo='Luta', descricao='Um Pokémon especialista em chutes.'),
            Pokedex(nome='Hitmonchan', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/103.png', tipo='Luta', descricao='Um Pokémon especialista em socos.'),
            Pokedex(nome='Lickitung', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/104.png', tipo='Normal', descricao='Um Pokémon que pode estender sua língua.'),
            Pokedex(nome='Koffing', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/105.png', tipo='Venenoso', descricao='Um Pokémon que exala gases tóxicos.'),
            Pokedex(nome='Weezing', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/106.png', tipo='Venenoso', descricao='Um Pokémon que pode criar fumaça.'),
            Pokedex(nome='Rhyhorn', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/107.png', tipo='Terra e Rocha', descricao='Um Pokémon que é muito forte.'),
            Pokedex(nome='Rhydon', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/108.png', tipo='Terra e Rocha', descricao='Um Pokémon que pode quebrar pedras.'),
            Pokedex(nome='Chansey', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/109.png', tipo='Normal', descricao='Um Pokémon que é muito gentil e cuida dos outros.'),
            Pokedex(nome='Tangela', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/110.png', tipo='Planta', descricao='Um Pokémon coberto de vinhas.'),
            Pokedex(nome='Kangaskhan', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/111.png', tipo='Normal', descricao='Um Pokémon que cuida de seu filhote.'),
            Pokedex(nome='Horsea', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/112.png', tipo='Água', descricao='Um Pokémon que vive em águas rasas.'),
            Pokedex(nome='Seadra', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/113.png', tipo='Água e Dragão', descricao='Um Pokémon que pode nadar rapidamente.'),
            Pokedex(nome='Goldeen', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/114.png', tipo='Água', descricao='Um Pokémon que pode nadar bem.'),
            Pokedex(nome='Seaking', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/115.png', tipo='Água', descricao='Um Pokémon que pode pular para fora da água.'),
            Pokedex(nome='Staryu', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/116.png', tipo='Água', descricao='Um Pokémon que pode regenerar seus membros.'),
            Pokedex(nome='Starmie', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/117.png', tipo='Água e Psíquico', descricao='Um Pokémon que é muito rápido.'),
            Pokedex(nome='Mr. Mime', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/118.png', tipo='Psíquico e Fada', descricao='Um Pokémon que é um artista.'),
            Pokedex(nome='Scyther', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/119.png', tipo='Inseto e Voador', descricao='Um Pokémon que é muito rápido e tem lâminas nos braços.'),
            Pokedex(nome='Jynx', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/120.png', tipo='Gelo e Psíquico', descricao='Um Pokémon que pode causar sono.'),
            Pokedex(nome='Electabuzz', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/121.png', tipo='Elétrico', descricao='Um Pokémon que gosta de eletricidade.'),
            Pokedex(nome='Magmar', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/122.png', tipo='Fogo', descricao='Um Pokémon que pode gerar fogo.'),
            Pokedex(nome='Pinsir', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/123.png', tipo='Inseto', descricao='Um Pokémon que tem grandes garras.'),
            Pokedex(nome='Tauros', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/124.png', tipo='Normal', descricao='Um Pokémon que é muito forte.'),
            Pokedex(nome='Magikarp', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/125.png', tipo='Água', descricao='Um Pokémon que é muito fraco.'),
            Pokedex(nome='Gyarados', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/126.png', tipo='Água e Dragão', descricao='Um Pokémon que é muito poderoso.'),
            Pokedex(nome='Lapras', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/127.png', tipo='Água e Gelo', descricao='Um Pokémon que pode nadar em águas profundas.'),
            Pokedex(nome='Ditto', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/128.png', tipo='Normal', descricao='Um Pokémon que pode se transformar em outros Pokémon.'),
            Pokedex(nome='Eevee', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/133.png', tipo='Normal', descricao='Um Pokémon com várias evoluções.'),
            Pokedex(nome='Vaporeon', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/134.png', tipo='Água', descricao='Uma das evoluções de Eevee.'),
            Pokedex(nome='Jolteon', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/135.png', tipo='Elétrico', descricao='Uma das evoluções de Eevee.'),
            Pokedex(nome='Flareon', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/136.png', tipo='Fogo', descricao='Uma das evoluções de Eevee.'),
            Pokedex(nome='Porygon', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/137.png', tipo='Normal', descricao='Um Pokémon feito de código.'),
            Pokedex(nome='Omanyte', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/138.png', tipo='Pedra e Água', descricao='Um Pokémon que vive em águas rasas.'),
            Pokedex(nome='Omastar', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/139.png', tipo='Pedra e Água', descricao='Um Pokémon que pode nadar rapidamente.'),
            Pokedex(nome='Kabuto', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/140.png', tipo='Pedra e Água', descricao='Um Pokémon que vive em águas rasas.'),
            Pokedex(nome='Kabutops', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/141.png', tipo='Pedra e Água', descricao='Um Pokémon que pode atacar rapidamente.'),
            Pokedex(nome='Aerodactyl', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/142.png', tipo='Pedra e Voador', descricao='Um Pokémon que pode voar.'),
            Pokedex(nome='Snorlax', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/143.png', tipo='Normal', descricao='Um Pokémon que dorme muito.'),
            Pokedex(nome='Articuno', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/144.png', tipo='Gelo e Voador', descricao='Um Pokémon lendário conhecido por seu poder.'),
            Pokedex(nome='Zapdos', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/145.png', tipo='Elétrico e Voador', descricao='Um Pokémon lendário que controla eletricidade.'),
            Pokedex(nome='Moltres', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/146.png', tipo='Fogo e Voador', descricao='Um Pokémon lendário que controla o fogo.'),
            Pokedex(nome='Dratini', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/147.png', tipo='Dragão', descricao='Um Pokémon que é muito raro.'),
            Pokedex(nome='Dragonair', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/148.png', tipo='Dragão', descricao='Um Pokémon que pode voar.'),
            Pokedex(nome='Dragonite', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/149.png', tipo='Dragão e Voador', descricao='Um Pokémon que é muito forte.'),
            Pokedex(nome='Mewtwo', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/150.png', tipo='Psíquico', descricao='Um Pokémon lendário conhecido por sua inteligência.'),
            Pokedex(nome='Mew', imagem='https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/151.png', tipo='Psíquico', descricao='Um Pokémon lendário que pode aprender qualquer movimento.'),
        ]

        db.session.bulk_save_objects(pokemons)
        db.session.commit()

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
      adicionar_pokemon()
      app.run(host='0.0.0.0', port=5000, debug=True)
