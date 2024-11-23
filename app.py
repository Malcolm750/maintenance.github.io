from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, 
    static_folder='.',  
    template_folder='.'  
)

# Configuration de la base de données
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle pour la table des inscriptions
class Inscription(db.Model):
    __tablename__ = 'inscriptions'
    id = db.Column(db.Integer, primary_key=True)
    projet = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    site = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date_inscription = db.Column(db.DateTime, server_default=db.func.now())

# Routes
@app.route('/')
def index():
    # Récupérer le nombre d'inscrits par projet
    stats_projets = db.session.query(
        Inscription.projet, 
        db.func.count(Inscription.id)
    ).group_by(Inscription.projet).all()
    
    # Créer un dictionnaire des statistiques
    stats = {projet: count for projet, count in stats_projets}
    return render_template('index.html', stats=stats)

@app.route('/inscription.html')
def inscription():
    return render_template('inscription.html')

@app.route('/inscription', methods=['POST'])
def traiter_inscription():
    if request.method == 'POST':
        nouvelle_inscription = Inscription(
            projet=request.form['projet'],
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            email=request.form['email'] + '@aphp.fr',
            site=request.form['site'],
            service=request.form['service']
        )
        db.session.add(nouvelle_inscription)
        db.session.commit()
        return redirect(url_for('confirmation'))

@app.route('/confirmation.html')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
