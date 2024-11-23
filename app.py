from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, 
    static_folder='.',  # Pour servir les fichiers statiques depuis la racine
    template_folder='.'  # Pour servir les fichiers HTML depuis la racine
)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription.html')
def inscription():
    return render_template('inscription.html')

@app.route('/confirmation.html')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))