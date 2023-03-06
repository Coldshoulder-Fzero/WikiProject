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
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass