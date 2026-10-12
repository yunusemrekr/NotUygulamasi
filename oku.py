import sqlite3

# 1. Kütüphaneciyi çağır ve dosyayı aç
baglanti = sqlite3.connect('notlar.db')
kutuphaneci = baglanti.cursor()

# 2. SQL Komutu ver: SELECT (Seç/Getir) * (Her Şeyi) FROM (Nereden) Notlar tablosundan
kutuphaneci.execute('SELECT * FROM Notlar')

# 3. Gelen verileri al ve ekrana yazdır
okunan_notlar = kutuphaneci.fetchall()
print("Veritabanındaki Notlar:", okunan_notlar)

# 4. Dosyayı kapat
baglanti.close()