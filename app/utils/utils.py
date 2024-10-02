import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def authenticate_profile(password, profile_details):
    hashed_password = profile_details['HashedPswd']
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
