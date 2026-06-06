import jwt
from datetime import datetime, timedelta
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
def create_access_token(data: dict):
    payload = data.copy()

    payload["exp"] = (
        datetime.now() + timedelta(hours=36)
    )

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None