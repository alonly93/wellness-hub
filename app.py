from flask import Flask, render_template, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ---------------------
# Database Configuration
# ---------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

# ---------------------
# Database Model
# ---------------------

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

# ---------------------
# Routes
# ---------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/save', methods=['POST'])
def save_note():
    data = request.get_json()
    text = data.get('text', '')

    note = Note(text=text)
    db.session.add(note)
    db.session.commit()

    return jsonify({"status": "saved", "id": note.id})

@app.route('/get/<int:note_id>')
def get_note(note_id):
    note = Note.query.get(note_id)
    if note:
        return jsonify({"id": note.id, "text": note.text})
    return jsonify({"error": "Not found"}), 404

# ---------------------
# Local Development Only
# ---------------------
# This block NEVER runs on Koyeb/Gunicorn.
# It only runs if you type: python app.py
# ---------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Safe to run only locally
    app.run(debug=True, port=5000)
