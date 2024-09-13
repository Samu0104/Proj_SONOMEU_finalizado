from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('BancoDeDados.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_sobrenome TEXT NOT NULL,
            data_nasc TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            nTelefone TEXT NOT NULL,
            cep TEXT NOT NULL,
            nCasa TEXT NOT NULL,
            idproduto INTEGER NOT NULL,
            qtd INTEGER NOT NULL,
            FOREIGN KEY (idproduto) REFERENCES Produto(id)
        )
    ''')
    conn.commit()
    conn.close()



@app.route('/')
def homepage():
    return render_template("index.html")



@app.route('/feminino')
def feminino():
    return render_template("feminino.html")



@app.route('/masculino')
def masculino():
    return render_template("masculino.html")



@app.route('/infantil')
def infantil():
    return render_template("infantil.html")



@app.route('/plus-size')
def plusSize():
    return render_template("plus-size.html")



@app.route('/comprar', methods=['GET', 'POST'])
def comprar():
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        nTelefone = request.form['telefone']
        cep = request.form['cep']
        nCasa = request.form['nCasa']
        idproduto = request.form['idproduto']
        qtd = request.form['quantidade']

        if not nome or not email or not nTelefone or not cep or not nCasa or not idproduto or not qtd:
            return "Erro: Todos os campos são obrigatórios."

        try:
            idproduto = int(idproduto)
            qtd = int(qtd)
        except ValueError:
            return "Erro: Produto e quantidade devem ser valores numéricos."

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT * FROM conta WHERE nome_sobrenome = ? AND email = ?
            ''', (nome, email))
            usuario = cursor.fetchone()
            
            if not usuario:
                return "Erro: Usuário não encontrado."

            cursor.execute('''
                SELECT * FROM Produto WHERE id = ?
            ''', (idproduto,))
            produto = cursor.fetchone()
            
            if not produto:
                return "Erro: Produto não encontrado."

            cursor.execute('''
                INSERT INTO compra (nome, email, nTelefone, cep, nCasa, idproduto, qtd)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email, nTelefone, cep, nCasa, idproduto, qtd))
            conn.commit()
            return "Compra realizada com sucesso!"
        except sqlite3.IntegrityError as e:
            return f"Erro ao realizar a compra: {str(e)}"
        finally:
            conn.close()

    return render_template('comprar.html')



@app.route('/confirmacao')
def confirmacao():
    return render_template("confirmacao.html")



@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome_sobrenome = request.form['name']
        data_nasc = request.form['dob']
        email = request.form['email']
        senha = request.form['password']

        if not nome_sobrenome or not data_nasc or not email or not senha:
            return "Erro: Todos os campos são obrigatórios."

        print(f"Dados recebidos: {nome_sobrenome}, {data_nasc}, {email}, {senha}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO conta (nome_sobrenome, data_nasc, email, senha) 
                VALUES (?, ?, ?, ?)''', (nome_sobrenome, data_nasc, email, senha))
            conn.commit()
            return "Usuário cadastrado com sucesso!"
        except sqlite3.IntegrityError:
            return "Erro: Este usuário ou email já está cadastrado."
        finally:
            conn.close()
    return render_template('cadastrar.html')




@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
    
        if not email or not senha:
            return "Erro: Todos os campos são obrigatórios."
        
        print(f"Dados recebidos: {email}, {senha}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM conta WHERE email = ? AND senha = ?
            ''', (email, senha))
            usuario = cursor.fetchone()
            
            if usuario:
                return "Usuário encontrado com sucesso!"
            else:
                return "Erro: Usuário ou senha inválidos."
        except sqlite3.Error as e:
            return f"Erro no banco de dados: {str(e)}"
        finally:
            conn.close()
    return render_template("entrar.html")


@app.route('/deletar', methods=['GET', 'POST'])
def deletar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
    
        if not email or not senha:
            return "Erro: Todos os campos são obrigatórios."
        
        print(f"Dados recebidos: {email}, {senha}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Verifica se o usuário existe
            cursor.execute('''
                SELECT * FROM conta WHERE email = ? AND senha = ?
            ''', (email, senha))
            usuario = cursor.fetchone()
            
            if usuario:
                # Deleta o usuário
                cursor.execute('''
                    DELETE FROM conta WHERE email = ? AND senha = ?
                ''', (email, senha))
                conn.commit()
                return "Usuário deletado com sucesso!"
            else:
                return "Erro: Usuário ou senha inválidos."
        except sqlite3.Error as e:
            return f"Erro no banco de dados: {str(e)}"
        finally:
            conn.close()
    return render_template("deletar.html")



if __name__ == "__main__":
    create_table()
    app.run(debug=True)
