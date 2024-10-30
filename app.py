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

def add_initial_pokemons():
    # Dados dos Pokémon de Kanto
   db.session.query(Pokedex).delete()
   db.session.commit()

   pokemons = [
      ('Bulbasaur', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/001.png', 'Planta e Venenoso', 'Um Pokémon pequeno com uma planta nas costas.'),
      ('Ivysaur', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/002.png', 'Planta e Venenoso', 'Quando a flor na sua costa floresce, significa que ele está pronto para evoluir.'),
      ('Venusaur', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/003.png', 'Planta e Venenoso', 'Possui uma enorme flor na costa que exala um aroma doce.'),
      ('Charmander', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/004.png', 'Fogo', 'O Pokémon que solta fogo quando feliz.'),
      ('Charmeleon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/005.png', 'Fogo', 'Se fica muito irritado, a chama na sua cauda queima com mais intensidade.'),
      ('Charizard', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/006.png', 'Fogo e Voador', 'Se Charizard ficar realmente irritado, a chama na ponta de sua cauda queima em um tom azul claro.'),
      ('Squirtle', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/007.png', 'Água', 'Ele pode usar a água que armazena na sua concha para se defender.'),
      ('Wartortle', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/008.png', 'Água', 'Ele é conhecido por ser um Pokémon que se preocupa com sua aparência.'),
      ('Blastoise', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/009.png', 'Água', 'Possui canhões que dispara água com força devastadora.'),
      ('Caterpie', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/010.png', 'Inseto', 'É um Pokémon pequeno que se alimenta de folhas.'),
      ('Metapod', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/011.png', 'Inseto', 'O casulo de um Caterpie, é protegido por uma casca dura.'),
      ('Butterfree', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/012.png', 'Inseto e Voador', 'Possui asas grandes e é conhecido por sua beleza.'),
      ('Weedle', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/013.png', 'Inseto e Venenoso', 'Ele possui um pequeno espinho em sua cabeça que pode envenenar.'),
      ('Kakuna', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/014.png', 'Inseto e Venenoso', 'A forma de larva do Weedle, ela se transforma em Butterfree.'),
      ('Beedrill', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/015.png', 'Inseto e Venenoso', 'Um Pokémon muito agressivo, com uma picada venenosa.'),
      ('Pidgey', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/016.png', 'Normal e Voador', 'Um Pokémon comum encontrado em muitos lugares.'),
      ('Pidgeotto', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/017.png', 'Normal e Voador', 'Um Pokémon mais forte que o Pidgey, se alimenta de insetos.'),
      ('Pidgeot', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/018.png', 'Normal e Voador', 'Um dos Pokémon voadores mais poderosos, com asas enormes.'),
      ('Rattata', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/019.png', 'Normal', 'Um Pokémon pequeno e rápido, comum em áreas urbanas.'),
      ('Ratic ate', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/020.png', 'Normal', 'Evolução do Rattata, conhecido por sua força.'),
      ('Spearow', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/021.png', 'Normal e Voador', 'Um Pokémon muito feroz e territorial.'),
      ('Fearow', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/022.png', 'Normal e Voador', 'A evolução de Spearow, é muito rápido e forte.'),
      ('Ekans', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/023.png', 'Venenoso', 'Um Pokémon que se esconde em lugares escuros e pode envenenar.'),
      ('Arbok', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/024.png', 'Venenoso', 'Tem um corpo longo e pode causar muito medo.'),
      ('Pikachu', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/025.png', 'Elétrico', 'O Pokémon mais famoso, conhecido por sua habilidade elétrica.'),
      ('Raichu', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/026.png', 'Elétrico', 'Evolução de Pikachu, é muito mais forte.'),
      ('Sandshrew', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/027.png', 'Terrestre', 'Um Pokémon que se esconde sob a areia.'),
      ('Sandslash', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/028.png', 'Terrestre', 'Evolução de Sandshrew, possui espinhos em suas costas.'),
      ('Nidoran (Fêmea)', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/029.png', 'Venenoso', 'Um pequeno Pokémon que se esconde em arbustos.'),
      ('Nidorina', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/030.png', 'Venenoso', 'Evolução de Nidoran (F), é mais forte.'),
      ('Nidoqueen', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/031.png', 'Venenoso e Terra', 'Um Pokémon forte e robusto.'),
      ('Nidoran (Macho)', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/032.png', 'Venenoso', 'Um pequeno Pokémon que pode evoluir.'),
      ('Nidorino', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/033.png', 'Venenoso', 'Evolução de Nidoran (M), tem um chifre forte.'),
      ('Nidoking', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/034.png', 'Venenoso e Terra', 'Um Pokémon muito poderoso com um grande chifre.'),
      ('Clefairy', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/035.png', 'Fada', 'Um Pokémon encantador que gosta de dançar.'),
      ('Clefable', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/036.png', 'Fada', 'Evolução de Clefairy, é muito rara.'),
      ('Vulpix', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/037.png', 'Fogo', 'Um Pokémon pequeno com pelagem quente.'),
      ('Ninetales', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/038.png', 'Fogo', 'Possui nove caudas e é muito bonito.'),
      ('Jigglypuff', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/039.png', 'Normal e Fada', 'Um Pokémon que pode colocar outros para dormir.'),
      ('Wigglytuff', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/040.png', 'Normal e Fada', 'Evolução de Jigglypuff, é muito fofinho.'),
      ('Zubat', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/041.png', 'Venenoso e Voador', 'Um Pokémon que vive em cavernas e se alimenta de inset os.'),
      ('Golbat', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/042.png', 'Venenoso e Voador', 'Evolução de Zubat, é muito rápido.'),
      ('Oddish', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/043.png', 'Planta e Venenoso', 'Um Pokémon que gosta de se esconder sob a sombra das árvores.'),
      ('Gloom', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/044.png', 'Planta e Venenoso', 'Um Pokémon que exala um odor horrível.'),
      ('Vileplume', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/045.png', 'Planta e Venenoso', 'Evolução de Gloom, possui uma enorme flor.'),
      ('Paras', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/046.png', 'Inseto e Venenoso', 'Um Pokémon que carrega fungos em suas costas.'),
      ('Parasect', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/047.png', 'Inseto e Venenoso', 'Evolução de Paras, muito forte.'),
      ('Venonat', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/048.png', 'Inseto e Venenoso', 'Um Pokémon que vive em florestas.'),
      ('Venomoth', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/049.png', 'Inseto e Venenoso', 'Evolução de Venonat, possui asas grandes.'),
      ('Diglett', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/050.png', 'Terrestre', 'Um Pokémon que vive debaixo da terra.'),
      ('Dugtrio', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/051.png', 'Terrestre', 'Evolução de Diglett, muito rápido.'),
      ('Meowth', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/052.png', 'Normal', 'Um Pokémon que gosta de colecionar moedas.'),
      ('Persian', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/053.png', 'Normal', 'Evolução de Meowth, muito elegante.'),
      ('Psyduck', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/054.png', 'Água', 'Um Pokémon que sofre de dores de cabeça.'),
      ('Golduck', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/055.png', 'Água', 'Evolução de Psyduck, é muito rápido.'),
      ('Mankey', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/056.png', 'Lutador', 'Um Pokémon muito agressivo.'),
      ('Primeape', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/057.png', 'Lutador', 'Evolução de Mankey, é muito forte.'),
      ('Growlithe', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/058.png', 'Fogo', 'Um pequeno Pokémon que adora brincar.'),
      ('Arcanine', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/059.png', 'Fogo', 'Evolução de Growlithe, é muito rápido.'),
      ('Poliwag', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/060.png', 'Água', 'Um pequeno Pokémon que vive em água.'),
      ('Poliwhirl', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/061.png', 'Água', 'Evolução de Poliwag, pode se esconder em sua concha.'),
      ('Poliwrath', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/062.png', 'Água e Lutador', 'Evolução de Poliwhirl, é muito forte.'),
      ('Abra', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/063.png', 'Psíquico', 'Um Pokémon que pode teleportar-se.'),
      ('Kadabra', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/064.png', 'Ps íquico', 'Evolução de Abra, é muito inteligente.'),
      ('Alakazam', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/065.png', 'Psíquico', 'A evolução mais forte de Abra, possui um QI elevado.'),
      ('Machop', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/066.png', 'Lutador', 'Um Pokémon muito forte que adora treinar.'),
      ('Machoke', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/067.png', 'Lutador', 'Evolução de Machop, é muito mais forte.'),
      ('Machamp', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/068.png', 'Lutador', 'Evolução de Machoke, tem quatro braços.'),
      ('Bellsprout', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/069.png', 'Planta e Venenoso', 'Um Pokémon que cresce em lugares úmidos.'),
      ('Weepinbell', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/070.png', 'Planta e Venenoso', 'Evolução de Bellsprout, possui uma flor.'),
      ('Victreebel', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/071.png', 'Planta e Venenoso', 'A evolução mais forte de Bellsprout, é muito perigoso.'),
      ('Tentacool', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/072.png', 'Água e Venenoso', 'Um Pokémon que vive no mar.'),
      ('Tentacruel', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/073.png', 'Água e Venenoso', 'Evolução de Tentacool, é muito perigoso.'),
      ('Geodude', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/074.png', 'Pedra e Terra', 'Um Pokémon que vive em montanhas.'),
      ('Graveler', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/075.png', 'Pedra e Terra', 'Evolução de Geodude, é mais forte.'),
      ('Golem', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/076.png', 'Pedra e Terra', 'Evolução de Graveler, é muito pesado.'),
      ('Ponyta', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/077.png', 'Fogo', 'Um Pokémon que vive em prados.'),
      ('Rapidash', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/078.png', 'Fogo', 'Evolução de Ponyta, é muito rápido.'),
      ('Slowpoke', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/079.png', 'Água e Psíquico', 'Um Pokémon que é muito lento.'),
      ('Slowbro', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/080.png', 'Água e Psíquico', 'Evolução de Slowpoke, é mais rápido.'),
      ('Magnemite', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/081.png', 'Elétrico e Aço', 'Um Pokémon que pode gerar eletricidade.'),
      ('Magneton', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/082.png', 'Elétrico e Aço', 'Evolução de Magnemite, muito poderoso.'),
      ('Farfetch’d', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/083.png', 'Normal e Voador', 'Um Pokémon que carrega um alho-poró.'),
      ('Doduo', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/084.png', 'Normal e Voador', 'Um Pokémon que tem duas cabeças.'),
      ('Dodrio', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/085.png', 'Normal e Voador', 'Evolução de Doduo, tem três cabeças.'),
      ('Seel', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/086.png', 'Água', 'Um Pokémon que vive em regiões frias.'),
      ('Dewgong', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/087.png', 'Água e Gelo', 'Evolução de Seel, pode nadar rapidamente.'),
      ('Grimer', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/088.png', 'Venenoso', 'Um Pokémon que é feito de lodo.'),
      ('Muk', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/089.png', 'Venenoso', 'Evolução de Grimer, muito grande.'),
      ('Shellder', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/090.png', 'Água', 'Um Pokémon que vive em água.'),
      ('Cloyster', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/091.png', 'Água e Gelo', 'Evolução de Shellder, é muito forte.'),
      ('Gastly', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/092.png', 'Fantasma e Venenoso', 'Um Pokémon que se dissolve no ar.'),
      ('Haunter', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/093.png', 'Fantasma e Venenoso', 'Evolução de Gastly, muito assustador.'),
      ('Gengar', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/094.png', 'Fantasma e Venenoso', 'Evolução de Haunter, é muito poderoso.'),
      ('Onix', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/095.png', 'Pedra e Terrestre', 'Um Pokémon que vive em cavernas.'),
      ('Drowzee', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/096.png', 'Psíquico', 'Um Pokémon que come sonhos.'),
      ('Hypno', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/097.png', 'Psíquico', 'Evolução de Drowzee, é muito bom em hipnose.'),
      ('Krabby', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/098.png', 'Água', 'Um Pokémon que vive em praias.'),
      ('Kingler', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/099.png', 'Água', 'Evolução de Krabby, é muito forte.'),
      ('Voltorb', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/100.png', 'Elétrico', 'Um Pokémon que se parece com uma bola.'),
      ('Electrode', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/101.png', 'Elétrico', 'Evolução de Voltorb, é muito rápido.'),
      ('Exeggcute', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/102.png', 'Planta e Psíquico', 'Um Pokémon que se parece com ovos.'),
      ('Exeggutor', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/103.png', 'Planta e Psíquico', 'Evolução de Exeggcute, tem três cabeças.'),
      ('Cubone', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/104.png', 'Terrestre', 'Um Pokémon que usa um crânio como capacete.'),
      ('Marowak', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/105.png', 'Terrestre', 'Evolução de Cubone, muito forte.'),
      ('Hitmonlee', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/106.png', 'Lutador', 'Um Pokémon que é especialista em chutes.'),
      ('Hitmonchan', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/107.png', 'Lutador', 'Um Pokémon que é especialista em socos.'),
      ('Lickitung', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/108.png', 'Normal', 'Um Pokémon que tem uma língua muito longa.'),
      ('Koffing', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/109.png', 'Venenoso', 'Um Pokémon que exala gases tóxicos.'),
      ('Weezing', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/110.png', 'Venenoso', 'Evolução de Koffing, é muito grande.'),
      ('Rhyhorn', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/111.png', 'Pedra e Terrestre', 'Um Pokémon que é muito forte.'),
      ('Rhydon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/112.png', 'Pedra e Terrestre', 'Evolução de Rhyhorn, é muito forte.'),
      ('Chansey', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/113.png', 'Normal', 'Um Pokémon que é muito gentil.'),
      ('Tangela', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/114.png', 'Planta', 'Um Pokémon que vive em florestas.'),
      ('Kangaskhan', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/115.png', 'Normal', 'Um Pokémon que cuida de seu filho em uma bolsa.'),
      ('Horsea', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/116.png', 'Água', 'Um pequeno Pokémon que vive em água.'),
      ('Seadra', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/117.png', 'Água', 'Evolução de Horsea, é muito rápido.'),
      ('Goldeen', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/118.png', 'Água', 'Um Pokémon que vive em rios.'),
      ('Seaking', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/119.png', 'Água', 'Evolução de Goldeen, é muito forte.'),
      ('Staryu', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/120.png', 'Água', 'Um Pokémon que vive em água.'),
      ('Starmie', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/121.png', 'Água e Psíquico', 'Evolução de Staryu, é muito forte.'),
      ('Mr. Mime', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/122.png', 'Psíquico e Fada', 'Um Pokémon que gosta de criar ilusões.'),
      ('Scyther', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/123.png', 'Inseto e Voador', 'Um Pokémon que tem lâminas nas mãos.'),
      ('Jynx', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/124.png', 'Água e Gelo', 'Um Pokémon que é muito bonito.'),
      ('Electabuzz', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/125.png', 'Elétrico', 'Um Pokémon que é muito rápido.'),
      ('Magmar', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/126.png', 'Fogo', 'Um Pokémon que é muito quente.'),
      ('Pinsir', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/127.png', 'Inseto', 'Um Pokémon que é muito forte.'),
      ('Tauros', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/128.png', 'Normal', 'Um Pokémon muito agressivo.'),
      ('Magikarp', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/129.png', 'Água', 'Um Pokémon que é muito fraco.'),
      ('Gyarados', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/130.png', 'Água e Voar', 'Evolução de Magikarp, é muito poderoso.'),
      ('Lapras', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/131.png', 'Água e Gelo', 'Um Pokémon que ajuda a cruzar lagos.'),
      ('Ditto', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/132.png', 'Normal', 'Um Pokémon que pode se transformar.'),
      ('Eevee', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/133.png', 'Normal', 'Um Pokémon que pode ev oluir de várias formas.'),
      ('Vaporeon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/134.png', 'Água', 'Evolução de Eevee, se adapta a ambientes aquáticos.'),
      ('Jolteon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/135.png', 'Elétrico', 'Evolução de Eevee, é muito rápido.'),
      ('Flareon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/136.png', 'Fogo', 'Evolução de Eevee, é muito quente.'),
      ('Porygon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/137.png', 'Normal', 'Um Pokémon feito de dados.'),
      ('Omanyte', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/138.png', 'Pedra e Água', 'Um Pokémon que vive em águas profundas.'),
      ('Omastar', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/139.png', 'Pedra e Água', 'Evolução de Omanyte, é muito forte.'),
      ('Kabuto', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/140.png', 'Pedra e Água', 'Um Pokémon que vive em água.'),
      ('Kabutops', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/141.png', 'Pedra e Água', 'Evolução de Kabuto, tem lâminas.'),
      ('Aerodactyl', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/142.png', 'Pedra e Voador', 'Um Pokémon que vive em cavernas.'),
      ('Snorlax', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/143.png', 'Normal', 'Um Pokémon que dorme muito.'),
      ('Articuno', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/144.png', 'Gelo e Voador', 'Um Pokémon lendário.'),
      ('Zapdos', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/145.png', 'Elétrico e Voador', 'Um Pokémon lendário.'),
      ('Moltres', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/146.png', 'Fogo e Voador', 'Um Pokémon lendário.'),
      ('Dratini', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/147.png', 'Dragão', 'Um pequeno Pokémon dragão.'),
      ('Dragonair', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/148.png', 'Dragão', 'Evolução de Dratini, é muito bonito.'),
      ('Dragonite', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/149.png', 'Dragão e Voador', 'Evolução de Dragonair, é muito poderoso.'),
      ('Mewtwo', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/150.png', 'Psíquico', 'Um Pokémon lendário criado em laboratório.'),
      ('Mew', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/151.png', 'Psíquico', 'Um Pokémon lendário e muito raro.')
   ]

   # Inserir os Pokémon no banco de dados
   for nome, imagem, descricao, tipo in pokemons:
        pokemon = Pokedex(nome=nome, imagem=imagem, descricao=descricao, tipo=tipo)
        db.session.add(pokemon)

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
      add_initial_pokemons()
      app.run(host='0.0.0.0', port=5000, debug=True)
