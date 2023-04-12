from flaskr.user import User
from google.cloud import storage
from io import BytesIO
from hashlib import sha256


class Backend:

    def __init__(self, storage_client=storage.Client()):
        self.user_bucket_name = 'theuserspasswords'
        self.content_bucket_name = 'thewikicontent'
        self.user_bucket = storage_client.bucket(self.user_bucket_name)
        self.content_bucket = storage_client.bucket(self.content_bucket_name)

    def get_wiki_page(self, name):
        blob = self.content_bucket.get_blob(name)
        if blob is None:
            raise ValueError(f'No page exists with the given name: {name}')
        else:
            # default mode for blob open() is read-only mode
            with blob.open() as b:
                return b.read()

    def get_all_page_names(self):
        blobs = self.content_bucket.list_blobs()
        # we should ignore any blobs that are images
        return [
            blob.name
            for blob in blobs
            if not blob.name.endswith(('png', 'jpg', 'jpeg'))
        ]

    def upload(self, name, blob_data):
        blob = self.content_bucket.get_blob(name)
        if blob is not None:
            raise ValueError(f'{name} already exists in the content bucket!')
        blob = self.content_bucket.blob(name)
        # write the byte data to the bucket
        with blob.open('wb') as b:
            b.write(blob_data)

    def sign_up(self, username, password):
        blob = self.user_bucket.get_blob(username)
        if blob is not None:
            raise ValueError(f'Username {username} already exists!')
        blob = self.user_bucket.blob(username)
        # hash the username/password together and store in bucket
        hashed_string = sha256(f'{username}:{password}'.encode()).hexdigest()
        with blob.open('w') as b:
            b.write(hashed_string)
        # return a default user object with the given username
        return User(username)

    def sign_in(self, username, password):
        blob = self.user_bucket.get_blob(username)
        if blob is None:
            raise ValueError(f'Username {username} does not exist!')

        # create hashed string to compare with bucket contents
        expected_hashed_string = sha256(
            f'{username}:{password}'.encode()).hexdigest()
        with blob.open() as b:
            if expected_hashed_string == b.read():
                # successful login, return a User object
                return User(username)
            else:
                # failed login, throw error
                raise ValueError(f'Invalid password for username {username}!')

    def get_image(self, name):
        blob = self.content_bucket.get_blob(name)
        if blob is None:
            # return empty bytes stream if image does not exist
            return BytesIO()
        else:
            with blob.open('rb') as b:
                return BytesIO(b.read())

    def search(self, query):
        """
        Searches for pages in the Google Cloud Storage bucket that contain the given query string.
        Returns a list of matching page titles.
        """
        query = query.lower()  # convert query to lowercase for case-insensitive search
        pages = []
        
        # Loop through all blobs in the content bucket
        for blob in self.content_bucket.list_blobs():
            # Read the content of the blob
            content = blob.download_as_bytes()
            # Compute the SHA-256 hash of the content
            hash = sha256(content).hexdigest()
            
            # Check if the hash matches the blob's name (which is the page title)
            if hash == blob.name:
                # Decode the content from bytes to string
                text = content.decode('utf-8')
                # Check if the query appears in the text
                if query in text.lower():
                    # Add the page title to the list of matching pages
                    pages.append(blob.name)
        
        return pages
