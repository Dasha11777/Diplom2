
import uuid

def generate_unique_user():
    unique = str(uuid.uuid4())
    return {
        "email": f"user{unique[:8]}@mail.com",
        "password": "password123",
        "name": f"User{unique[:8]}"
    }
