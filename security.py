from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("secret_key")

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")