import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth, db

# Path to your service account key JSON file
cred = credentials.Certificate('path/to/serviceAccountKey.json')

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred)


def get_user_name(id_token):
    try:
        # Verify the ID token and get the user's UID
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Get a reference to the 'institutions' table
        ref = db.reference('institutions')

        # Get the user's data
        user_data = ref.child(uid).get()

        # Return the user's name
        return user_data['name']
    except ValueError:
        # The ID token was invalid
        return None