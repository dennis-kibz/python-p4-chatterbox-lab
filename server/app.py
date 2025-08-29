# server/app.py

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route('/')
def index():
    return '<h1>Chatterbox API</h1>'

@app.route('/messages', methods=['GET'])
def get_messages():
    """Get all messages ordered by created_at ascending"""
    try:
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_data = []
        
        for message in messages:
            messages_data.append({
                'id': message.id,
                'body': message.body,
                'username': message.username,
                'created_at': message.created_at.isoformat(),
                'updated_at': message.updated_at.isoformat()
            })
        
        return make_response(jsonify(messages_data), 200)
    
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/messages', methods=['POST'])
def create_message():
    """Create a new message"""
    try:
        data = request.get_json()
        
        if not data:
            return make_response(jsonify({'error': 'No JSON data provided'}), 400)
        
        body = data.get('body')
        username = data.get('username')
        
        if not body or not username:
            return make_response(jsonify({'error': 'Both body and username are required'}), 400)
        
        new_message = Message(
            body=body,
            username=username
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        response_data = {
            'id': new_message.id,
            'body': new_message.body,
            'username': new_message.username,
            'created_at': new_message.created_at.isoformat(),
            'updated_at': new_message.updated_at.isoformat()
        }
        
        return make_response(jsonify(response_data), 201)
    
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """Update a message's body"""
    try:
        message = Message.query.filter(Message.id == id).first()
        
        if not message:
            return make_response(jsonify({'error': 'Message not found'}), 404)
        
        data = request.get_json()
        
        if not data:
            return make_response(jsonify({'error': 'No JSON data provided'}), 400)
        
        body = data.get('body')
        
        if not body:
            return make_response(jsonify({'error': 'Body is required'}), 400)
        
        message.body = body
        db.session.commit()
        
        response_data = {
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at.isoformat(),
            'updated_at': message.updated_at.isoformat()
        }
        
        return make_response(jsonify(response_data), 200)
    
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """Delete a message"""
    try:
        message = Message.query.filter(Message.id == id).first()
        
        if not message:
            return make_response(jsonify({'error': 'Message not found'}), 404)
        
        db.session.delete(message)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Message deleted successfully'}), 200)
    
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(port=5000, debug=True)