from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .database import firebase_admin
from firebase_admin import auth, db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # login is the URL that Postman/frontend would use to get the token.

# gets the token from the Authorization header of the HTTP request with Depends(oauth2_scheme)
# used in routers to identify the user making the request

#input=JWT  output=Name of current user  eg RSET
def get_current_user(idToken: str = Depends(oauth2_scheme)) -> str:
    try:
        # Verify the ID token and get the user's UID
        decoded_token = auth.verify_id_token(idToken)
        uid = decoded_token['uid']

        # Get a reference to the 'users' object
        ref = db.reference('users')

        # Get the user's name
        user_data = ref.child(uid).get()
        return user_data['name']
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Couldnt validate credentials", headers={"WWW-Authenticate": "Bearer"})
