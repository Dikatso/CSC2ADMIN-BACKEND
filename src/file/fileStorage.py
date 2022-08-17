
from firebase_admin import storage

def upload_file(fileName: str) -> str:
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # Opt : if you want to make public access from the URL
    blob.make_public()
    return blob.public_url