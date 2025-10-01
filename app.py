from flask import Flask, render_template,request,jsonify,redirect,url_for,session
from get_dados import *
import os 
import sqlite3

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_supersegura'
ACCESS_TOKEN = "APP_USR-5515393234086824-051409-a798dc3e1af15b38426c01b84b761393-1952959008"
PUBLIC_KEY = "APP_USR-1b3c0147-9080-4743-b327-109084494912"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
@app.route("/")
def redirec():
    session["edit"] = ["GABRIEL","Luan"]
    session["game_buy"] = ""
    return redirect(url_for("sobre"))


@app.route("/addGame",methods=["GET","POST"])
def add_game_page():
    if request.method == "POST":
        nome = request.form.get("Nome")
        preço = request.form.get("Preço")
        descrição = request.form.get("Descrição")
        img1 = request.form.get("IMG1")
        img2 = request.form.get("IMG2")
        img3 = request.form.get("IMG3")
        requisitos = request.form.get("Requisitos")
        classificação = request.form.get("Classificação")
        id = request.form.get("ID de download")
        personagem = request.form.get("Personagem Principal")
        import sqlite3 
        conn = sqlite3.connect("banco_games.db")
        conn.execute(""" 
        INSERT INTO games (nome,preço,descrição,img1,img2,img3,requisitos,classificação,download_id,personagem_principal) VALUES (?,?,?,?,?,?,?,?,?,?)
        """,(nome,preço,descrição,img1,img2,img3,requisitos,classificação,id,personagem))
        conn.commit()
        conn.close()
    return render_template("add_game.html")
def delete_game(game):
    import sqlite3

    conn = sqlite3.connect('banco_games.db')
    cursor = conn.cursor()

    # Deleta a linha com id = 5
    cursor.execute("DELETE FROM games WHERE nome = ?", (game,))

    conn.commit()
    conn.close()

@app.route("/editGame",methods=["GET","POST"])
def edit_game_page():
    nome = session.get("game_buy", "NÃO DEFINIDO")

    if request.method == "POST":
        # Salvar os dados editados no banco
        nome_a = request.form.get("Nome")
        preço = request.form.get("Preço")
        descrição = request.form.get("Descrição")
        img1 = request.form.get("IMG1")
        img2 = request.form.get("IMG2")
        img3 = request.form.get("IMG3")
        requisitos = request.form.get("Requisitos")
        classificação = request.form.get("Classificação")
        id = request.form.get("ID de download")
        personagem = request.form.get("Personagem Principal")

        import sqlite3 
        conn = sqlite3.connect("banco_games.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM games WHERE nome = ?",
            (nome,)
        )
        conn.execute("""
            INSERT INTO games (nome,preço,descrição,img1,img2,img3,requisitos,classificação,download_id,personagem_principal)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (nome_a, preço, descrição, img1, img2, img3, requisitos, classificação, id, personagem))
        conn.commit()
        conn.close()
        return redirect("/games")  # opcional

    else:
        # Buscar dados do jogo para preencher no formulário
        import sqlite3
        conn = sqlite3.connect("banco_games.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games WHERE nome = ?", (nome,))
        game_data = cursor.fetchone()
        conn.close()

        # Se não encontrou o jogo, pode tratar isso
        if not game_data:
            return "Jogo não encontrado"

        # Mapear os dados
        game_dict = {
            "nome":game_data[1],
            "preço": game_data[2],
            "descrição": game_data[3],
            "img1": game_data[4],
            "img2": game_data[5],
            "img3": game_data[6],
            "requisitos": game_data[7],
            "classificação": game_data[8],
            "download_id": game_data[9],
            "personagem": game_data[10]
        }
        
        return render_template("editgame.html", game=game_dict,nome=nome,delete_game = delete_game)

@app.route("/sites",methods=["GET","POST"])
def my_games():
    
    valor_game_buy = session.get("game_buy", "NÃO DEFINIDO")
    print(f"Valor atual de game_buy na sessão: '{valor_game_buy}'")

    if valor_game_buy == "":
        print("O valor de game_buy está vazio")
    else:
        print("O valor de game_buy NÃO está vazio:", valor_game_buy)

    #img_user = session["img_user"] 
    img_user = session.get('img_user', 'Visitante') 
    usuario = session.get('username', 'Visitante') 
    from get_dados import return_outnames_imgs
    vals = return_outnames_imgs(usuario)
    if request.method=="POST":
        session["game"] = request.form.get("game")
        session["game_buy"] = request.form.get("game")
        
        return redirect(url_for("game"))  
    return render_template("sites.html",jogos=vals,usuario=usuario,img_user=img_user,contem_https=contem_https)


@app.route("/sobre")
def sobre():
    
    valor_game_buy = session.get("game_buy", "NÃO DEFINIDO")
    print(f"Valor atual de game_buy na sessão: '{valor_game_buy}'")

    if valor_game_buy == "":
        print("O valor de game_buy está vazio")
    else:
        print("O valor de game_buy NÃO está vazio:", valor_game_buy)

    img_user = session.get('img_user', 'Visitante') 
    usuario = session.get('username', 'Visitante') 
    return render_template("sobre.html",usuario=usuario,img_user=img_user)

@app.route("/games",methods=["GET","POST"])
def games():
    
    valor_game_buy = session.get("game_buy", "NÃO DEFINIDO")
    print(f"Valor atual de game_buy na sessão: '{valor_game_buy}'")

    if valor_game_buy == "":
        print("O valor de game_buy está vazio")
    else:
        print("O valor de game_buy NÃO está vazio:", valor_game_buy)

    #img_user = session["img_user"] 
    img_user = session.get('img_user', 'Visitante') 
    usuario = session.get('username', 'Visitante') 
    from get_dados import return_names_imgs
    vals = return_names_imgs()
    print(vals)
    if request.method=="POST":
        session["game"] = request.form.get("game")
        session["game_buy"] = request.form.get("game")
        
        return redirect(url_for("game"))  # IMPORTANTE: return aqui!
    return render_template("games.html",jogos=vals,usuario=usuario,img_user=img_user,contem_https=contem_https)

def contem_https(texto):
    return 'https://' in texto

@app.route('/game', methods=['GET', 'POST'])
def game():
    session["add"] = False
    session['botao_foi_clicado'] = True
    valor_game_buy = session.get("game_buy", "NÃO DEFINIDO")
    print(f"Valor atual de game_buy na sessão: '{valor_game_buy}'")
    users = ["GABRIEL","Juan1234"]
    if valor_game_buy == "":
        print("O valor de game_buy está vazio")
    else:
        print("O valor de game_buy NÃO está vazio:", valor_game_buy)
    from games_bc import get_games
    games_str = get_games(session.get('username', 'Visitante'))

    if games_str is not None:
        # Divide a string em lista, removendo espaços extras
        games = [g.strip() for g in games_str.split(',')]
        game = session.get('game', 'Visitante')

        if game in games:
            index = games.index(game)  # Pega a posição do game na lista
            session["button_state"] = "Remover"
            print(f"Jogo '{game}' encontrado na posição {index}.")
        else:
            session["button_state"] = "Adquirir"
            print(f"Jogo '{game}' não encontrado.")
    else:
        session["button_state"] = "Adquirir"

    nome = session.get('game', 'Visitante') 
    usuario = session.get('username', 'Visitante') 

    if request.method == 'POST' and usuario !="Visitante":
        if session["button_state"] == "Adquirir":
            session['botao_foi_clicado'] = True
        else:
            session['botao_foi_clicado'] = False
        session["add"] = True
        return redirect(url_for('home'))
    img_user = session.get('img_user', 'Visitante') 
    take = return_dates(nome)
    preço = take[0]
    descrição = take[1]
    
    img1 = take[2]
    img2 = take[3]
    img3 = take[4]
    contem = False
    if not contem_https(img1):
        img1 = "img/"+take[2]
        img2 = "img/"+take[3]
        img3 = "img/"+take[4]
        contem = True
    
    requisitos = take[5]
    classificação = take[6]
    video = nome+".mp4"
    if nome == "Super Mario Farm (Fan Game)":
        video = "5LyfH_d2_zQ"
    elif nome == "Super Mario World (Fan Game)":
        video = "8pZwzUx9Bic"
    video = "https://www.youtube.com/embed/" + video
    return render_template("game.html",requisitos=requisitos,img3=img3,video=video,nome=nome,preço=preço,descrição=descrição,img1=img1,img2=img2,classificação=classificação,usuario=usuario,img_user=img_user,button_state = session['button_state'],user = session.get('game', 'Visitante'),contem=contem,contem_https=contem_https,users = users)

if __name__ == "__main__":
    app.run(debug=True)
