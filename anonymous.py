from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

@app.before_request
def create_tables():
    db.create_all()

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Message content is required'}), 400

    message = Message(content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent anonymously'}), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return jsonify([msg.to_dict() for msg in messages])

if __name__ == '__main__':
    app.run(debug=True)
