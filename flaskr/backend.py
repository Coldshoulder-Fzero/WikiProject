# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

class Backend:

    def init(self):

        self.storage_client = storage.Client()

        self.user_bucket_name = "bucket-users-password"
        self.content_bucket_name = "bucket-contents"

        self.user_bucket = self.storage_client.bucket(self.user_bucket_name)
        self.content_bucket = self.storage_client.bucket(self.content_bucket_name)
        
    def get_wiki_page(self, name):
        blob = self.content_bucket.get_blob(name)
        if blob is None:
            raise ValueError("Page not found")
        return blob.download_as_bytes()

    def get_all_page_names(self):
        blobs = self.content_bucket.list_blobs()
        return [blob.name for blob in blobs]

    def upload(self, name, data):
        blob = self.content_bucket.blob(name)
        blob.upload_from_string(data)

    def sign_up(self, username, password):
        blob = self.user_bucket.blob(username)
        if not blob.exists():
            from hashlib import sha256

            hashed_password = sha256(password.encode("utf-8")).hexdigest()
            data = f"password={hashed_password}".encode("utf-8")
            blob.upload_from_string(data)

    def sign_in(self, username, password):
        blob = self.user_bucket.get_blob(username)
        if blob is None:
            return False

        from hashlib import sha256

        hashed_password = sha256(password.encode("utf-8")).hexdigest()
        return hashed_password == blob.download_as_text().split("=")[1]

    def get_image(self, name):
        blob = self.content_bucket.get_blob(name)
        if blob is None:
            raise ValueError("Image not found")
        return blob.download_as_bytes()

