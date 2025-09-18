from passlib.context import CryptContext



pw_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



def hash_pw(plain_pw) -> str:
    return pw_context.hash(plain_pw)

def verify_pw(plain_pw, hashed_pw) -> bool:
    return pw_context.verify(plain_pw, hashed_pw)
    