from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///halaman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database
class Halaman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(150), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    tanggal_posting = db.Column(db.Date, default=datetime.utcnow)

# Route untuk menampilkan halaman baru
@app.route('/')
def index():
    data = Halaman.query.order_by(Halaman.id.desc()).all()
    return render_template('halaman_baru.html', data=data)

# Route untuk menambahkan data
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        judul = request.form['judul']
        link = request.form['link']
        tanggal_posting = datetime.strptime(request.form['tanggal_posting'], '%Y-%m-%d')
        halaman = Halaman(judul=judul, link=link, tanggal_posting=tanggal_posting)
        db.session.add(halaman)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('tambah.html')

# Route untuk mengedit data
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    halaman = Halaman.query.get_or_404(id)
    if request.method == 'POST':
        halaman.judul = request.form['judul']
        halaman.link = request.form['link']
        halaman.tanggal_posting = datetime.strptime(request.form['tanggal_posting'], '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', halaman=halaman)

# Route untuk menghapus data
@app.route('/delete/<int:id>')
def delete(id):
    halaman = Halaman.query.get_or_404(id)
    db.session.delete(halaman)
    db.session.commit()
    return redirect(url_for('index'))

# Menjalankan aplikasi
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
