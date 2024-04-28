from passlib.hash import bcrypt
import re
from typing import Tuple

from voluntary_work_calendar.config import Config


# Initialize CryptContext/bcrypt
pwd_context = bcrypt.using(rounds=Config.ROUNDS)

def check_rules_password(psw: str) -> Tuple[bool, str]:
    error_in_psw = False
    type_response = "passwordchanged"
    if len(psw) < 8:
        # "La password deve essere lunga almeno 8 caratteri"
        type_response = "La password deve essere lunga almeno 8 caratteri"
        error_in_psw = True
    if re.search("[0-9]", psw) is None:
        # "La password deve contenere almeno un numero"
        type_response = "La password deve contenere almeno un numero"
        error_in_psw = True
    if re.search("[A-Z]", psw) is None:
        # "La password deve contenere almeno una lettera maiuscola"
        type_response = "La password deve contenere almeno una lettera maiuscola"
        error_in_psw = True
    #TODO: aggiungere check che ci sia almeno un carattere speciale

    return error_in_psw, type_response


def get_hash(phrase):
    return pwd_context.hash(phrase)


def verify_hash(plain_phrase, hashed_phrase):
    return pwd_context.verify(plain_phrase, hashed_phrase)
