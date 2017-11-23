from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password): # it compare the login data with stored user data
    user = UserModel.find_by_username(username) # username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload): # payload is the content of the JWT token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
