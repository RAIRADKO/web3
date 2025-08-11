from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import check_password_hash

admin = Blueprint('admin', __name__, template_folder='templates')

def get_db():
    """Fungsi helper untuk koneksi ke database MySQL."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='web_kominfo'
    )

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        # FIX: Mengganti 'name' dengan 'usernama' sesuai dengan struktur tabel Anda
        cursor.execute('SELECT * FROM users WHERE usernama = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password_input):
            # FIX: Menyesuaikan kunci session dengan nama kolom yang benar
            session['user'] = user['usernama'] 
            return redirect(url_for('admin.dashboard'))
        else:
            return "Login Gagal. Periksa kembali username dan password Anda.", 401
    return render_template('admin/login.html')


@admin.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('admin.login'))
    return render_template('admin/dashboard.html')

@admin.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('admin.login'))

@admin.route('/identitas_website')
def identitas_website():
    """Menampilkan data dari tabel identitas_website."""
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM identitas_website')
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin/identitas_website.html', data=data)

@admin.route('/sensor_komentar')
def sensor_komentar():
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM sensor_komentar')
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin/sensor_komentar.html', data=data)

@admin.route('/tambah_sensor', methods=['GET', 'POST'])
def tambah_sensor():
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        kata = request.form['kata_jelek']
        ganti = request.form['ganti_menjadi']
        action = request.form['action']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sensor_komentar (kata_jelek, ganti_menjadi, action) VALUES (%s, %s, %s)', (kata, ganti, action))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin.sensor_komentar'))

    return render_template('admin/tambah_sensor.html')

@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_sensor(id):
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        kata = request.form['kata_jelek']
        ganti = request.form['ganti_menjadi']
        action = request.form['action']
        cursor.execute('UPDATE sensor_komentar SET kata_jelek=%s, ganti_menjadi=%s, action=%s WHERE id=%s', (kata, ganti, action, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin.sensor_komentar'))

    cursor.execute('SELECT * FROM sensor_komentar WHERE id = %s', (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('admin/edit_sensor.html', data=data)

@admin.route('/delete/<int:id>')
def delete_sensor(id):
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sensor_komentar WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin.sensor_komentar'))

# Tampilkan semua data halaman_baru
@admin.route('/halaman_baru')
def halaman_baru():
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM halaman_baru ORDER BY tanggal_posting DESC')
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin/halaman_baru.html', data=data)

# Tambah data baru
@admin.route('/tambah_halaman', methods=['GET', 'POST'])
def tambah_halaman():
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        judul = request.form['judul']
        link = request.form['link']
        tanggal_posting = request.form['tanggal_posting']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO halaman_baru (judul, link, tanggal_posting) VALUES (%s, %s, %s)',
            (judul, link, tanggal_posting)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('admin.halaman_baru'))

    return render_template('admin/tambah_halaman.html')

# Edit data
@admin.route('/edit_halaman/<int:id>', methods=['GET', 'POST'])
def edit_halaman(id):
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        judul = request.form['judul']
        link = request.form['link']
        tanggal_posting = request.form['tanggal_posting']

        cursor.execute(
            'UPDATE halaman_baru SET judul=%s, link=%s, tanggal_posting=%s WHERE id=%s',
            (judul, link, tanggal_posting, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin.halaman_baru'))

    cursor.execute('SELECT * FROM halaman_baru WHERE id = %s', (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('admin/edit_halaman.html', data=data)

@admin.route('/edit_postingan/<int:id>', methods=['GET', 'POST'])
def edit_postingan(id):
    # logika ambil data postingan
    # logika update postingan
    return render_template('admin/edit_postingan.html', data=data)


# Hapus data
@admin.route('/delete_halaman/<int:id>')
def delete_halaman(id):
    if 'user' not in session:
        return redirect(url_for('admin.login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM halaman_baru WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin.halaman_baru'))
