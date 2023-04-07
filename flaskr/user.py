"""Default implementation of a User class for Flask Login.

The Flask Login library will load users with our implementation. By default, we will make sure that every user is authenticated and active. 

Reference documentation: https://flask-login.readthedocs.io/en/latest/#your-user-class
"""


class User:

    def __init__(self, username):
        """Constructs a default instance of the User class for login/logout."""

        self.username = username
        # by default, we return True to indicate that every User that we create will be authenticated
        self.is_authenticated = True
        # by default, we return True to indicate that every User is active
        self.is_active = True
        # every user we encounter should not be anonymous. They must all have a username and password
        self.is_anonymous = False

    def get_id(self):
        """Return the string that uniquely identifies the user."""
        return self.username


'''Creating admin class to implement different methods and access to data in the website when user is proved to be an Admin instead of regular user
    current class has basic user implementation since further functions need to be decided before implemented.

    Each admin will have a username, password and role describing the access needed (PoLP)
'''

class Admin:
    def __init__(self, username,role):
        self.username = username
        self.role = role
        # by default, we return True to indicate that every User that we create will be authenticated
        self.is_authenticated = True
        # by default, we return True to indicate that every User is active
        self.is_active = True
        # every user we encounter should not be anonymous. They must all have a username and password
        self.is_anonymous = False    
    
    def admin_id(self):
        return self.username, self.role
