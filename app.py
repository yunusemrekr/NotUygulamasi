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
                icerik TEXT NOT NULL,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                kategori TEXT DEFAULT 'Genel'
            )
        ''')
    # Var olan veritabanında 'kategori' sütunu yoksa ekle (Migration)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Notlar)")
    sutunlar = [kolon[1] for kolon in cursor.fetchall()]
    if 'kategori' not in sutunlar:
        conn.execute("ALTER TABLE Notlar ADD COLUMN kategori TEXT DEFAULT 'Genel'")
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
    baslik = (request.form.get('baslik') or '').strip()
    icerik = (request.form.get('icerik') or '').strip()
    kategori = (request.form.get('kategori') or 'Genel').strip()
    if baslik and icerik:
        conn = get_db_connection()
        conn.execute('INSERT INTO Notlar (baslik, icerik, kategori) VALUES (?, ?, ?)', (baslik, icerik, kategori))
        conn.commit()
        conn.close()
    return redirect(url_for('ana_sayfa'))

@app.route('/sil/<int:id>', methods=['POST'])
def not_sil(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Notlar WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('ana_sayfa'))

@app.route('/duzenle/<int:id>', methods=['GET', 'POST'])
def not_duzenle(id):
    conn = get_db_connection()
    if request.method == 'POST':
        baslik = (request.form.get('baslik') or '').strip()
        icerik = (request.form.get('icerik') or '').strip()
        kategori = (request.form.get('kategori') or 'Genel').strip()
        if baslik and icerik:
            conn.execute('UPDATE Notlar SET baslik = ?, icerik = ?, kategori = ? WHERE id = ?', (baslik, icerik, kategori, id))
            conn.commit()
            conn.close()
            return redirect(url_for('ana_sayfa'))
    
    kayit = conn.execute('SELECT * FROM Notlar WHERE id = ?', (id,)).fetchone()
    conn.close()
    if kayit is None:
        return redirect(url_for('ana_sayfa'))
    return render_template('duzenle.html', kayit=kayit)

if __name__ == '__main__':
    app.run(debug=True)
