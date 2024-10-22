from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "4988c3777f32f05c47355f6ef4d247e25b899f15cfe70a02f3bdcf7eedee17b7"


# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMywiZXhwIjoxNzI3OTg4NzcxfQ.DnXlfhiLkjhSnPC8gZzaAqsUfHgXuzN4ypjdpkbT0ao"



ALGORITHM = "HS256"  # Fixed the typo here
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()  # Added parentheses to call the copy method
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Corrected the typo in "algorithm"
    return encoded_jwt
