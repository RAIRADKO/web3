from flask import Flask, render_template, redirect, url_for, session, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'rahasia123'

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='kominfojaya',
    database='web_kominfo'
)
cursor = conn.cursor(dictionary=True)

# ========================
# ROUTE UNTUK HALAMAN BARU
# ========================

# Tampilkan data
@app.route('/')
def index():
    cursor.execute("SELECT * FROM halaman ORDER BY id DESC")
    data = cursor.fetchall()
    return render_template('halaman_baru.html', data=data)

# Tambah data
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        judul = request.form['judul']
        link = request.form['link']
        tanggal_posting = request.form['tanggal_posting']  # format: YYYY-MM-DD
        cursor.execute("INSERT INTO halaman (judul, link, tanggal_posting) VALUES (%s, %s, %s)",
                       (judul, link, tanggal_posting))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('tambah.html')

# Edit data
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        judul = request.form['judul']
        link = request.form['link']
        tanggal_posting = request.form['tanggal_posting']
        cursor.execute("UPDATE halaman SET judul=%s, link=%s, tanggal_posting=%s WHERE id=%s",
                       (judul, link, tanggal_posting, id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM halaman WHERE id = %s", (id,))
    halaman = cursor.fetchone()
    return render_template('edit.html', halaman=halaman)

# Hapus data
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM halaman WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('index'))

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
