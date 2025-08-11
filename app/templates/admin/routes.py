from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    data = {
        'berita': 6724,
        'kategori': 14,
        'tag': 25,
        'users': 8,
    }
    return render_template('dashboard.html', data=data)
