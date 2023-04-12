from flaskr.user import User
from google.cloud import storage
from io import BytesIO
from hashlib import sha256
from datetime import datetime
import re


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

    def save_wiki_page(self, page_name, content, username):
        # Save the current version to the history folder
        if self.content_bucket.blob(page_name).exists():
            current_content = self.get_wiki_page(page_name)
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            history_blob = self.content_bucket.blob(f'history/{page_name}-{timestamp}-{username}.txt')
            history_blob.upload_from_string(current_content)

        # Save the new version
        blob = self.content_bucket.blob(page_name)
        blob.upload_from_string(content)

    def get_previous_version(self, page_name):
        history_blobs = sorted(
            [blob for blob in self.content_bucket.list_blobs(prefix=f'history/{page_name}')],
            key=lambda x: x.name,
            reverse=True
        )

        if not history_blobs:
            return None, None, None

        latest_history_blob = history_blobs[0]

        split_list = re.split('/|-', latest_history_blob.name[:-4])

        if len(split_list) >= 4:
            _, _, timestamp, username = split_list
            timestamp = datetime.strptime(timestamp, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp, username = None, None

        return latest_history_blob.download_as_text(), timestamp, username



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

 