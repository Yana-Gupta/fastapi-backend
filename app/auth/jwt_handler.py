from fastapi import FastAPI, status, HTTPException
from datetime import datetime, timedelta
from jose import jwt

JWT_SECRET = "TVlfSldUX1NFQ0VUCg"
JWT_ALGORITHM = "HS256"

# Creates the token 
def sign_JWT(email: str, role: str):
    try:
        # Create payload
        payload = {
            'email': email,  # User identifier -> Email
            'role': role,  # User role -> Admin, User, etc.
            'exp': datetime.utcnow() + timedelta(minutes=30)  # Expiration time
        }
        
        # Encode the token
        encoded_token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        
        return {"token": encoded_token}
    except Exception as e:
        return {"error": str(e)}


# Decodes the token
def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return {"decoded_token": decoded_token}
    except jwt.exceptions.DecodeError:
        return False
   