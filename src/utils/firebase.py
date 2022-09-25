from firebase_admin import credentials, initialize_app

""" Initializes firebase file storage app """   
def initialise_file_storage():
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred, {'storageBucket': 'cs2admin.appspot.com'})
