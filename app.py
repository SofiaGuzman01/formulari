from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Crear o conectar a la base de datos
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return redirect(url_for('formulario'))

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        # Guardar en la base de datos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, telefono, email) VALUES (?, ?, ?)",
        (nombre, telefono, email))
        conn.commit()
        conn.close()
        return redirect(url_for('usuarios'))
    return render_template('formulario.html')

@app.route('/usuarios')
def usuarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios_list = cursor.fetchall()
    conn.close()
    return render_template('usuario.html', usuarios=usuarios_list)

if __name__ == '__main__':
    app.run(debug=True)
