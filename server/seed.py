#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

# server/seed.py

from app import app
from models import db, Message

def seed_data():
    with app.app_context():
        # Clear existing data
        Message.query.delete()
        
        # Create sample messages
        messages = [
            Message(
                body="Hello everyone! Welcome to Chatterbox!",
                username="admin"
            ),
            Message(
                body="This is my first message in the chat!",
                username="alice"
            ),
            Message(
                body="Great to see everyone here. How's everyone doing?",
                username="bob"
            ),
            Message(
                body="I love this new chat app! Very clean interface.",
                username="charlie"
            ),
            Message(
                body="Anyone want to grab coffee later?",
                username="dana"
            ),
            Message(
                body="The weather is beautiful today!",
                username="eve"
            ),
            Message(
                body="Just finished a great workout. Feeling energized!",
                username="frank"
            ),
            Message(
                body="Working on some exciting new projects. Can't wait to share!",
                username="grace"
            ),
            Message(
                body="Thanks for all the warm welcomes everyone!",
                username="alice"
            ),
            Message(
                body="Looking forward to chatting with you all!",
                username="admin"
            )
        ]
        
        # Add messages to session
        for message in messages:
            db.session.add(message)
        
        # Commit the changes
        db.session.commit()
        print("✅ Database seeded successfully!")
        print(f"✅ Added {len(messages)} messages to the database")

if __name__ == '__main__':
    seed_data()