from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///berita.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Berita
class Berita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)

# Route Tampil
@app.route('/berita')
def berita():
    data = Berita.query.order_by(Berita.tanggal.desc()).all()
    return render_template('berita.html', data=data)

# Route Tambah
@app.route('/berita/tambah', methods=['POST'])
def tambah_berita():
    judul = request.form['judul']
    isi = request.form['isi']
    berita_baru = Berita(judul=judul, isi=isi)
    db.session.add(berita_baru)
    db.session.commit()
    return redirect(url_for('berita'))

# Route Hapus
@app.route('/berita/hapus/<int:id>')
def hapus_berita(id):
    data = Berita.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('berita'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
