from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet
import os

engine = create_engine(os.getenv("HOST"), echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    api_key = Column(String(255))
    encryption_key = Column(String(255))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Function to encrypt data
def encrypt_data(data: bytes) -> bytes:
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)
    cipher_text = cipher_suite.encrypt(data)
    return cipher_text, encryption_key

# Function to decrypt data
def decrypt_data(cipher_text: bytes, encryption_key: bytes) -> bytes:
    cipher_suite = Fernet(encryption_key)
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text
