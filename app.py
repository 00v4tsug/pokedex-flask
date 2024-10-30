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
         ('Metapod', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/011.png', 'Inseto', 'É um casulo que protege o Caterpie durante a evolução.'),
         ('Butterfree', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/012.png', 'Inseto e Voador', 'Possui asas grandes e coloridas que podem hipnotizar seus inimigos.'),
         ('Weedle', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/013.png', 'Inseto e Venenoso', 'Possui um ferrão na cabeça que pode causar dor.'),
         ('Kakuna', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/014.png', 'Inseto e Venenoso', 'Ele evolui para Beedrill, mas está imobilizado em um casulo.'),
         ('Beedrill', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/015.png', 'Inseto e Venenoso', 'Possui agulhas afiadas em suas patas e pode atacar em alta velocidade.'),
         ('Pidgey', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/016.png', 'Normal e Voador', 'Um Pokémon comum que pode ser encontrado em qualquer lugar.'),
         ('Pidgeotto', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/017.png', 'Normal e Voador', 'Ele é um caçador habilidoso, conhecido por sua velocidade.'),
         ('Pidgeot', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/018.png', 'Normal e Voador', 'Possui asas grandes que lhe permitem voar rapidamente.'),
         ('Rattata', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/019.png', 'Normal', 'Um Pokémon pequeno e ágil que é difícil de capturar.'),
         ('Raticate', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/020.png', 'Normal', 'Possui dentes afiados que podem cortar quase qualquer coisa.'),
         ('Spearow', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/021.png', 'Normal e Voador', 'Um Pokémon agressivo que ataca em grupos.'),
         ('Fearow', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/022.png', 'Normal e Voador', 'Um Pokémon veloz que pode atingir sua presa rapidamente.'),
         ('Ekans', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/023.png', 'Venenoso', 'Um Pokémon que se esconde nas sombras e ataca de surpresa.'),
         ('Arbok', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/024.png', 'Venenoso', 'Possui um padrão hipnotizante em sua cabeça.'),
         ('Pikachu', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/025.png', 'Elétrico', 'O Pokémon mais famoso do mundo, conhecido por seu ataque elétrico.'),
         ('Raichu', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/026.png', 'Elétrico', 'Possui um poder elétrico muito forte.'),
         ('Sandshrew', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/027.png', 'Terra', 'Um Pokémon que se esconde sob a areia para se proteger.'),
         ('Sandslash', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/028.png', 'Terra', 'Possui garras afiadas para escavar.'),
         ('Nidoran♀', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/029.png', 'Venenoso', 'Um Pokémon pequeno e tímido.'),
         ('Nidorina', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/030.png', 'Venenoso', 'Um Pokémon elegante que se preocupa com sua aparência.'),
         ('Nidoqueen', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/031.png', 'Venenoso e Terra', 'Possui uma enorme força e pode usar ataques poderosos.'),
         ('Nidoran♂', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/032.png', 'Venenoso', 'Um Pokémon pequeno e energético.'),
         ('Nidorino', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/033.png', 'Venenoso', 'Possui chifres afiados e é conhecido por ser muito agressivo.'),
         ('Nidoking', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/034.png', 'Venenoso e Terra', 'É um Pokémon extremamente forte e tem um temperamento feroz.'),
         ('Clefairy', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/035.png', 'Fada', 'É um Pokémon que vive na montanha e se sente confortável sob a luz da lua.'),
         ('Clefable', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/036.png', 'Fada', 'Possui um coração gentil e ajuda os que precisam.'),
         ('Vulpix', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/037.png', 'Fogo', 'Um Pokémon bonito que possui uma cauda longa e elegante.'),
         ('Ninetales', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/038.png', 'Fogo', 'Possui um poder místico e é conhecido por ser muito sábio.'),
         ('Jigglypuff', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/039.png', 'Normal e Fada', 'Um Pokémon que canta uma canção suave para adormecer seus inimigos.'),
         ('Wigglytuff', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/040.png', 'Normal e Fada', 'Possui um corpo macio e é conhecido por sua força.'),
         ('Zubat', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/041.png', 'Venenoso e Voador', 'Um Pokémon que se move em grupos e é conhecido por sua agilidade.'),
         ('Golbat', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/042.png', 'Venenoso e Voador', 'Possui grandes dentes afiados que pode usar para morder.'),
         ('Oddish', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/043.png', 'Planta e Venenoso', 'Um Pokémon que se esconde sob a sombra das folhas.'),
         ('Gloom', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/044.png', 'Planta e Venenoso', 'Possui um cheiro forte que pode adormecer os inimigos.'),
         ('Vileplume', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/045.png', 'Planta e Venenoso', 'Possui uma grande flor que exala um aroma doce.'),
         ('Paras', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/046.png', 'Inseto e Planta', 'Um Pokémon que é encontrado em florestas e campos.'),
         ('Parasect', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/047.png', 'Inseto e Planta', 'Possui fungos que podem causar problemas aos inimigos.'),
         ('Venonat', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/048.png', 'Inseto e Venenoso', 'É um Pokémon que se move de forma silenciosa para evitar ser visto.'),
         ('Venomoth', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/049.png', 'Inseto e Venenoso', 'Possui grandes asas e pode causar paralisia com seu veneno.'),
         ('Diglett', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/050.png', 'Terra', 'Um Pokémon que escava buracos e é difícil de ver.'),
         ('Dugtrio', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/051.png', 'Terra', 'Três Diglett se movem juntos e podem causar muito dano.'),
         ('Meowth', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/052.png', 'Normal', 'Um Pokémon que gosta de colecionar moedas.'),
         ('Persian', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/053.png', 'Normal', 'É um Pokémon elegante e conhecido por sua agilidade.'),
         ('Psyduck', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/054.png', 'Água', 'Um Pokémon que sofre de dores de cabeça e pode usar poderes psíquicos.'),
         ('Golduck', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/055.png', 'Água', 'Um Pokémon que é rápido na água e tem uma força surpreendente.'),
         ('Poliwag', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/056.png', 'Água', 'Possui uma cauda que se move rapidamente na água.'),
         ('Poliwhirl', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/057.png', 'Água', 'É um Pokémon que pode usar ataques de água com força.'),
         ('Poliwrath', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/058.png', 'Água e Luta', 'Um Pokémon poderoso que pode nadar rapidamente.'),
         ('Abra', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/059.png', 'Psíquico', 'Ele pode usar poderes psíquicos para se teletransportar.'),
         ('Kadabra', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/060.png', 'Psíquico', 'Possui um poder psíquico que pode causar dor em seus inimigos.'),
         ('Alakazam', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/061.png', 'Psíquico', 'É um Pokémon extremamente inteligente e ágil.'),
         ('Machop', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/062.png', 'Luta', 'Um Pokémon forte e resistente.'),
         ('Machoke', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/063.png', 'Luta', 'Ele é conhecido por sua força bruta.'),
         ('Machamp', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/064.png', 'Luta', 'Possui quatro braços e é extremamente poderoso.'),
         ('Bellsprout', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/065.png', 'Planta e Venenoso', 'Um Pokémon que se alimenta de luz solar.'),
         ('Weepinbell', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/066.png', 'Planta e Venenoso', 'Ele pode usar sua boca para capturar presas.'),
         ('Victreebel', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/067.png', 'Planta e Venenoso', 'Possui uma boca grande e atrai presas com seu aroma.'),
         ('Tentacool', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/068.png', 'Água e Venenoso', 'Um Pokémon que flutua na água e pode causar envenenamento.'),
         ('Tentacruel', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/069.png', 'Água e Venenoso', 'Possui tentáculos que podem causar dor.'),
         ('Geodude', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/070.png', 'Pedra e Terra', 'Um Pokémon que se esconde sob pedras e rochas.'),
         ('Graveler', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/071.png', 'Pedra e Terra', 'Ele é muito pesado e pode causar danos ao cair.'),
         ('Golem', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/072.png', 'Pedra e Terra', 'É um Pokémon enorme e pode causar danos significativos.'),
         ('Ponyta', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/073.png', 'Fogo', 'Um Pokémon que é rápido e pode correr rapidamente.'),
         ('Rapidash', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/074.png', 'Fogo', 'Possui uma crina de fogo que brilha intensamente.'),
         ('Slowpoke', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/075.png', 'Água e Psíquico', 'Um Pokémon lento que pode ser muito poderoso.'),
         ('Slowbro', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/076.png', 'Água e Psíquico', 'Ele é um Pokémon que tem um temperamento calmo.'),
         ('Magnemite', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/077.png', 'Elétrico e Aço', 'Um Pokémon que pode causar choque elétrico.'),
         ('Magneton', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/078.png', 'Elétrico e Aço', 'Ele é formado por três Magnemites.'),
         ('Farfetch', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/079.png', 'Normal e Voador', 'Um Pokémon que é conhecido por carregar um alho-poró.'),
         ('Doduo', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/080.png', 'Normal e Voador', 'Um Pokémon de duas cabeças que pode correr rapidamente.'),
         ('Dodrio', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/081.png', 'Normal e Voador', 'Possui três cabeças que podem atacar rapidamente.'),
         ('Seel', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/082.png', 'Água', 'Um Pokémon que vive em águas frias e é muito amigável.'),
         ('Dewgong', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/083.png', 'Água e Gelo', 'Possui uma grande habilidade de nadar.'),
         ('Grimer', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/084.png', 'Venenoso', 'Um Pokémon feito de lixo e resíduos.'),
         ('Muk', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/085.png', 'Venenoso', 'Ele é conhecido por sua forte toxicidade.'),
         ('Shellder', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/086.png', 'Água', 'Um Pokémon que vive na água e tem uma concha dura.'),
         ('Cloyster', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/087.png', 'Água e Gelo', 'Ele pode usar sua concha para proteger-se de ataques.'),
         ('Gastly', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/088.png', 'Fantasma e Venenoso', 'Um Pokémon que é formado por gás e pode causar medo.'),
         ('Haunter', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/089.png', 'Fantasma e Venenoso', 'Ele pode passar através de objetos e causar terror.'),
         ('Gengar', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/090.png', 'Fantasma e Venenoso', 'Um Pokémon que se esconde nas sombras.'),
         ('Onix', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/091.png', 'Pedra e Terra', 'Um Pokémon em forma de serpente feito de rochas.'),
         ('Drowzee', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/092.png', 'Psíquico', 'Um Pokémon que pode causar sonolência em seus inimigos.'),
         ('Hypno', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/093.png', 'Psíquico', 'Ele pode fazer as pessoas dormirem e ter sonhos.'),
         ('Krabby', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/094.png', 'Água', 'Um Pokémon que vive na água e é conhecido por suas garras.'),
         ('Kingler', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/095.png', 'Água', 'Um Pokémon muito poderoso com grandes garras.'),
         ('Voltorb', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/096.png', 'Elétrico', 'Um Pokémon que se parece com uma esfera de energia.'),
         ('Electrode', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/097.png', 'Elétrico', 'Ele é conhecido por sua rapidez e explosões.'),
         ('Exeggcute', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/098.png', 'Planta e Psíquico', 'Um Pokémon que se assemelha a ovos.'),
         ('Exeggutor', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/099.png', 'Planta e Psíquico', 'Ele pode causar ataques psíquicos fortes.'),
         ('Cubone', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/100.png', 'Terra', 'Um Pokémon que usa um osso como arma.'),
         ('Marowak', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/101.png', 'Terra', 'Ele tem um temperamento forte e é muito protetor.'),
         ('Hitmonlee', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/102.png', 'Luta', 'Um Pokémon especialista em chutar.'),
         ('Hitmonchan', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/103.png', 'Luta', 'Um Pokémon especialista em socos.'),
         ('Lickitung', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/104.png', 'Normal', 'Um Pokémon que tem uma língua longa e pegajosa.'),
         ('Koffing', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/105.png', 'Venenoso', 'Um Pokémon que expele fumaça tóxica.'),
         ('Weezing', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/106.png', 'Venenoso', 'Ele é conhecido por seu gás venenoso.'),
         ('Rhyhorn', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/107.png', 'Terra e Rocha', 'Um Pokémon que é muito forte e resistente.'),
         ('Rhydon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/108.png', 'Terra e Rocha', 'Ele é considerado um dos primeiros Pokémon a evoluir.'),
         ('Chansey', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/109.png', 'Normal', 'Um Pokémon que é conhecido por sua bondade e carinho.'),
         ('Tangela', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/110.png', 'Planta', 'Um Pokémon que se esconde em sua folhagem.'),
         ('Kangaskhan', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/111.png', 'Normal', 'Um Pokémon que é muito protetor com seu filhote.'),
         ('Horsea', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/112.png', 'Água', 'Um Pokémon que vive em águas rasas.'),
         ('Seadra', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/113.png', 'Água', 'Um Pokémon que pode nadar rapidamente.'),
         ('Goldeen', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/114.png', 'Água', 'Possui uma linda aparência e é um ótimo nadador.'),
         ('Seaking', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/115.png', 'Água', 'É um Pokémon que é conhecido por sua força.'),
         ('Staryu', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/116.png', 'Água', 'Um Pokémon que brilha e é muito bonito.'),
         ('Starmie', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/117.png', 'Água e Psíquico', 'Possui uma habilidade incrível de nadar.'),
         ('Mr. Mime', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/118.png', 'Psíquico e Fada', 'Ele pode criar barreiras com poderes psíquicos.'),
         ('Scyther', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/119.png', 'Inseto e Voador', 'Um Pokémon que é rápido e possui garras afiadas.'),
         ('Jynx', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/120.png', 'Água e Gelo', 'Um Pokémon que é conhecido por seu canto hipnotizante.'),
         ('Electabuzz', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/121.png', 'Elétrico', 'Um Pokémon que é muito rápido e ágil.'),
         ('Magmar', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/122.png', 'Fogo', 'Um Pokémon que pode lançar chamas intensas.'),
         ('Pinsir', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/123.png', 'Inseto', 'Um Pokémon que possui grandes garras e é muito forte.'),
         ('Tauros', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/124.png', 'Normal', 'Um Pokémon que é conhecido por sua força.'),
         ('Magikarp', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/125.png', 'Água', 'Um Pokémon que é fraco, mas pode evoluir para um poderoso.'),
         ('Gyarados', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/126.png', 'Água e Voando', 'Um Pokémon que é muito forte e feroz.'),
         ('Lapras', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/127.png', 'Água e Gelo', 'Um Pokémon que é conhecido por sua bondade.'),
         ('Ditto', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/128.png', 'Normal', 'Um Pokémon que pode se transformar em qualquer outro Pokémon.'),
         ('Eevee', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/133.png', 'Normal', 'Um Pokémon que pode evoluir para várias formas diferentes.'),
         ('Vaporeon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/134.png', 'Água', 'Uma forma evoluída de Eevee que é muito bonita.'),
         ('Jolteon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/135.png', 'Elétrico', 'Uma forma evoluída de Eevee que é muito rápida.'),
         ('Flareon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/136.png', 'Fogo', 'Uma forma evoluída de Eevee que é muito poderosa.'),
         ('Porygon', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/137.png', 'Normal', 'Um Pokémon criado por tecnologia.'),
         ('Omanyte', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/138.png', 'Pedra e Água', 'Um Pokémon que é uma espécie antiga.'),
         ('Omastar', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/139.png', 'Pedra e Água', 'Ele tem um corpo robusto e forte.'),
         ('Kabuto', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/140.png', 'Pedra e Água', 'Um Pokémon que é uma espécie antiga.'),
         ('Kabutops', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/141.png', 'Pedra e Água', 'Ele é muito rápido e tem garras afiadas.'),
         ('Aerodactyl', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/142.png', 'Pedra e Voador', 'Um Pokémon pré-histórico que pode voar.'),
         ('Snorlax', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/143.png', 'Normal', 'Um Pokémon muito pesado que dorme a maior parte do tempo.'),
         ('Articuno', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/144.png', 'Gelo e Voador', 'Um Pokémon lendário conhecido por sua beleza.'),
         ('Zapdos', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/145.png', 'Elétrico e Voador', 'Um Pokémon lendário conhecido por sua rapidez.'),
         ('Moltres', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/146.png', 'Fogo e Voador', 'Um Pokémon lendário que é muito forte.'),
         ('Dratini', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/147.png', 'Dragão', 'Um Pokémon que é muito bonito e elegante.'),
         ('Dragonair', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/148.png', 'Dragão', 'Ele pode voar rapidamente.'),
         ('Dragonite', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/149.png', 'Dragão e Voador', 'Um Pokémon muito poderoso e amigável.'),
         ('Mewtwo', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/150.png', 'Psíquico', 'Um Pokémon que foi criado a partir de genética avançada.'),
         ('Mew', 'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/151.png', 'Psíquico', 'Um Pokémon mítico que é muito raro.');
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
