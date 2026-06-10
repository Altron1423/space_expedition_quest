import hashlib
from backend.src.config.base import Settings

settings = Settings()

hash_models = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    "blake2b": hashlib.blake2b,
    "blake2s": hashlib.blake2s,
    "sha3_224": hashlib.sha3_224,
    "sha3_256": hashlib.sha3_256,
    "sha3_384": hashlib.sha3_384,
    "sha3_512": hashlib.sha3_512,
    "shake_128": hashlib.shake_128,
    "shake_256": hashlib.shake_256,
}

hash_model =hash_models[settings.hash_algorithm]

def hashing(password: str) -> str:
    """
    Преобразует пароль в хеш.
    :param password: Пароль, который требуется преобразовать.
    :return: Пароль в виде хеша
    """
    return hash_model(password.encode()).hexdigest()

def is_correct(password:str, hashed_password:str)->bool:
    """
    Проверяет, совпадает ли хеш введённого пароля и уже хешированный пароль.
    :param password: Пароль для проверки.
    :param hashed_password: Хешированный пароль.
    :return:
    """
    return hashing(password) == hashed_password


