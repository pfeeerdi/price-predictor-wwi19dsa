def createHashAndSalt(password):
    import os
    import hashlib
    #Generation of Salt and Hash-Key
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    # Store them as:
    StorageKey = salt + key
    return StorageKey
    # Getting the values back out
    #salt_from_storage = StorageKey[:32] # 32 is the length of the salt
    #key_from_storage = StorageKey[32:]

def matchingPassword(StorageKey, password):
    import hashlib

    salt = (StorageKey[:32]) # Get the salt you stored for *this* user
    key = StorageKey[32:] # Get this users key calculated

    password_to_check = password # The password provided by the user to check

    # Use the exact same setup you used to generate the key, but this time put in the password to check
    new_key = hashlib.pbkdf2_hmac('sha256', password_to_check.encode('utf-8'), salt, 100000)

    if new_key == key:
        return True
    else:
        return False

def secretKey():
    f = open("secret_key.bin", 'rb')
    secret = f.read()
    f.close()
    return secret

def createToken(email):
    import jwt
    import datetime
    #Reading Secret Key
    secret = secretKey()
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': email
        }
        return str(jwt.encode(payload, secret, algorithm='HS256'), 'utf-8')
    except Exception as e:
        return e

def verifyToken(auth_token):
    import jwt
    from flask_restful import abort
    #Reading Secret Key
    secret = secretKey()
    #decoding Token
    try:
        payload = jwt.decode(auth_token, secret)
        print(payload['sub'])
        return True
    except jwt.ExpiredSignatureError:
        abort(404, message="Token expired")
        return False

    except jwt.InvalidTokenError:
        abort(404, message="Token invalid")
        return False


    

