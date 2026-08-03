from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION BASE DE DONNÉES ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horco_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- CONFIGURATION DU SERVEUR MAIL (Exemple avec Gmail) ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'salioungom018@gmail.com'  # <-- Votre email
app.config['MAIL_PASSWORD'] = 'eoacpbcidaloplle'  # <-- Votre mot de passe d'application
app.config['MAIL_DEFAULT_SENDER'] = ('Horco Beauté', 'salioungom018@gmail.com')

db = SQLAlchemy(app)
mail = Mail(app)

# Modèle de la table des réservations
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/booking', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'Données invalides.'}), 400

    try:
        # 1. Enregistrement dans la base de données
        new_booking = Booking(
            fullname=data.get('fullname'),
            email=data.get('email'),
            phone=data.get('phone'),
            service=data.get('service'),
            date=data.get('date'),
            time=data.get('time')
        )
        db.session.add(new_booking)
        db.session.commit()

        # 2. Envoi de l'e-mail de notification au salon
        msg_salon = Message(
            subject=f"✨ Nouvelle Réservation VIP - {new_booking.fullname}",
            recipients=['salioungom01L@gmail.com'] # L'email qui reçoit les alertes de réservation
        )
        msg_salon.body = f"""
        NOUVELLE RÉSERVATION EN LIGNE - HORCO BEAUTÉ

        Client : {new_booking.fullname}
        Téléphone : {new_booking.phone}
        Email : {new_booking.email}
        Prestation : {new_booking.service}
        Date : {new_booking.date} à {new_booking.time}
        
        Adresse du salon : 7 cours Gambetta, 34000 Montpellier
        """
        mail.send(msg_salon)

        # 3. Envoi du mail de confirmation au client
        msg_client = Message(
            subject="Votre réservation chez Horco Beauté Montpellier",
            recipients=[new_booking.email]
        )
        msg_client.body = f"""
        Bonjour {new_booking.fullname},

        Nous avons le plaisir de vous confirmer la prise en compte de votre demande de réservation chez Horco Beauté.

        Détails du rendez-vous :
        • Prestation : {new_booking.service}
        • Date : {new_booking.date} à {new_booking.time}
        • Lieu : 7 cours Gambetta, 34000 Montpellier

        Pour toute modification ou annulation, veuillez nous contacter au 09 83 80 90 08.

        Au plaisir de vous accueillir,
        L'équipe Horco Beauté
        """
        mail.send(msg_client)

        return jsonify({'success': True, 'message': 'Réservation enregistrée ! Un email de confirmation vous a été envoyé.'})

    except Exception as e:
        db.session.rollback()
        print("Erreur :", e)
        return jsonify({'success': False, 'message': 'Erreur lors de l\'enregistrement ou de l\'envoi de l\'email.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)