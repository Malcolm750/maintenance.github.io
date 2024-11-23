from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__, 
    static_folder='.',  
    template_folder='.'  
)

# Activation de CORS pour permettre les requêtes cross-origin
CORS(app)

# Configuration NocoDB
NOCODB_API_URL = os.environ.get('NOCODB_API_URL')
NOCODB_TOKEN = os.environ.get('NOCODB_TOKEN')
NOCODB_TABLE_ID = os.environ.get('NOCODB_TABLE_ID')

# Routes pour les pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription.html')
def inscription():
    return render_template('inscription.html')

@app.route('/confirmation.html')
def confirmation():
    return render_template('confirmation.html')

# Routes API pour NocoDB
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        headers = {
            'xc-auth': NOCODB_TOKEN,
            'Content-Type': 'application/json'
        }
        response = requests.get(
            f"{NOCODB_API_URL}/api/v2/tables/{NOCODB_TABLE_ID}/records/groupby",
            headers=headers
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inscription', methods=['POST'])
def submit_inscription():
    try:
        data = request.json
        headers = {
            'xc-auth': NOCODB_TOKEN,
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f"{NOCODB_API_URL}/api/v2/tables/{NOCODB_TABLE_ID}/records",
            headers=headers,
            json=data
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
