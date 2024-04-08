from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth, db

# Path to your service account key JSON file
#cred = credentials.Certificate(os.getenv('FIREBASE_FILE_PATH'))
cred = credentials.Certificate('/home/aj/Documents/GitHub/GradeAI/C/backend/FirebaseCreds.json')

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://auto-mark-grader-default-rtdb.firebaseio.com/'
})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # login is the URL that Postman/frontend would use to get the token.

# gets the token from the Authorization header of the HTTP request with Depends(oauth2_scheme)
# used in routers to identify the user making the request
def get_current_user(idToken: str):# = Depends(oauth2_scheme)):
    try:
        # Verify the ID token and get the user's UID
        decoded_token = auth.verify_id_token(idToken)
        uid = decoded_token['uid']

        # Get a reference to the 'institutions' table
        ref = db.reference('institutions')

        # Get the user's data
        user_data = ref.child(uid).get()
        return user_data['name']
    
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Couldnt validate credentials", headers={"WWW-Authenticate": "Bearer"})
        return None

print(get_current_user('eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwNzhkMGViNzdhMjdlNGUxMGMzMTFmZTcxZDgwM2I5MmY3NjYwZGYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vYXV0by1tYXJrLWdyYWRlciIsImF1ZCI6ImF1dG8tbWFyay1ncmFkZXIiLCJhdXRoX3RpbWUiOjE3MTI1MTAxNDksInVzZXJfaWQiOiJIZjhLUk9JUEZuVmNnbjdtNEhmMHdDRVRESWUyIiwic3ViIjoiSGY4S1JPSVBGblZjZ243bTRIZjB3Q0VUREllMiIsImlhdCI6MTcxMjUxMDE0OSwiZXhwIjoxNzEyNTEzNzQ5LCJlbWFpbCI6InUyMTAzMDU3QHJhamFnaXJpLmVkdS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInUyMTAzMDU3QHJhamFnaXJpLmVkdS5pbiJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.eS0ovoYSqw8g_N4CnE2mMDxDgswx618ueJwnrHsAjvSi2b_QkHU0Iu-cU1CJNSIiPD8KxKasWGs4mb_NnJ0Napq-OIXELuJMkVvr68iIFwzvwmS6GX-7bqmNb1TKvHtipcZbxprk1BF4cIXG_1GO6QrO3rtqdt0Aiwadhskftk8Yo_BjGyCEysspibdL65eniX-r2zdqQAdMl2CSvCsE1c5mLPWMCtOG78ZkgBrQ6oIBsPqsNWywWhA_JgbU-gXWzUOKYPqMoamKY_AsVWP-_wK1WV9xcsPfGWYyDrTDjPj5Q5C4fbRVK1Fse2mrSqhRlKacDCoMY0AoHnPcHcoLhg'))
