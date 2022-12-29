from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])


def get_password_hash(texto):
    return pwd_context.hash(texto)

def verify_password(texto, hash):
    return pwd_context.verify(texto, hash)
