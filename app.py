import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = 'notlar.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Notlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT NOT NULL,
            icerik TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Uygulama başladığında veritabanı ve tablo yoksa oluşturulur
init_db()

@app.route('/')
def ana_sayfa():
    conn = get_db_connection()
    notlar = conn.execute('SELECT * FROM Notlar ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', notlar=notlar)

@app.route('/ekle', methods=['POST'])
def not_ekle():
    baslik = request.form.get('baslik')
    icerik = request.form.get('icerik')
    if baslik and icerik:
        conn = get_db_connection()
        conn.execute('INSERT INTO Notlar (baslik, icerik) VALUES (?, ?)', (baslik, icerik))
        conn.commit()
        conn.close()
    return redirect(url_for('ana_sayfa'))

if __name__ == '__main__':
    app.run(debug=True)