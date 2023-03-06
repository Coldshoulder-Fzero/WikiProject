# TODO(Project 1): Implement Backend according to the requirements.
from flask import request
from google.cloud import storage
import hashlib

class Backend:

    def __init__(self):
        pass
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self, name, password):

        # Encripting passwords
        with_salt = f"{name}{password}"
        hash = hashlib.blake2b(with_salt.encode()).hexdigest()
        
        return 

    def sign_in(self):

        pass

    def get_image(self):
        pass

