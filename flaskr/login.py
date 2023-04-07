"""Creates all the endpoints related to login, logout, and sign up.

The following endpoints will be created:

URI     | Method | Description
--------|--------|-------------
/login  | GET    | Returns the login page
/login  | POST   | Extracts login info from login page and calls backend.sign_in
/logout | GET    | Logs out the current user
/signup | GET    | Gets the signup page
/signup | POST   | Extracts signup info from signup page and calls backend.sign_up
"""

from flaskr.user import User  # default User class that we implemented
from flask import render_template, request
from flask_login import login_user, login_required, logout_user


# Note: we pass in all of the dependencies to the function (dependency injection)
def make_endpoints(app, login_manager, backend):
    """Constructs the login, logout, and sign up endpoints for the wiki.

    Args:
        app: instance of our Flask app
        login_manager: instance of flask_login.LoginManager
        backend: object that allows our wiki to interact with our database
    """

    @login_manager.user_loader
    def load_user(user_id):
        """Returns a user with the unique identifier.

        For now, we just create an instance of our User class and return that 
        object. Documentation for this method can be found at 
        https://flask-login.readthedocs.io/en/latest/#how-it-works

        Args:
            user_id: unique id of a user
        """
        return User(user_id)

    @app.route('/login')
    def login():
        """Returns the login page.

        This should handle the GET request for /login.
        """
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        """Extracts the login info and attempts to login the user.

        When the login button is pressed on the Wiki, the POST request is sent 
        with the login info (username + password) attached to the request. We 
        should extract the username and password and call backend.sign_in. If 
        we encounter a failure, redirect the user to the appropriate error page.
        """

        # extract username/password
        username = request.form.get('username')
        password = request.form.get('password')

        # check if both username/password were provided
        if not (username and password):
            # return appropriate error page
            return render_template(
                'main.html',
                page_name='Login Failed',
                page_content='Need a username and password to login!')
        # call backend method to sign in
        try:
            user = backend.sign_in(username, password)
        except ValueError as ve:
            # error with sign in, return appropriate error page
            return render_template('main.html',
                                   page_name='Login Failed',
                                   page_content=str(ve))
        # no errors, call login_user method required by flask_login
        login_user(user)
        # return appropriate page letting the user know that sign in worked
        return render_template('main.html',
                               page_name='Login Successful',
                               page_content=f'Welcome {username} to my wiki!')

    @app.route('/logout')
    @login_required
    def logout():
        """Logs out the current user.

        We need the @login_required because the user must be logged in before 
        we are able to call this endpoint. If logout is successful, return a 
        page to let the user know that they were logged out.
        """

        # call the logout_user() method from flask_login
        logout_user()
        # return appropriate page letting the user know that logout worked
        return render_template('main.html',
                               page_name='Logout Successful',
                               page_content='Logged out!')

    @app.route('/signup')
    def signup():
        """Returns the sign up page.

        This method should handle the GET request for /signup. For now, we just 
        render the appropriate template with a form for the user to fill in the 
        username and password.
        """

        return render_template('signup.html')

    @app.route('/signup', methods=['POST'])
    def signup_post():
        """Extracts the sign up info and attempts to signup the user.

        When the signup button is pressed on the Wiki, the POST request is sent 
        with the signup info (username + password) attached to the request. We 
        should extract the username and password and call backend.sign_up. If 
        we encounter a failure, redirect the user to the appropriate error page.
        """

        # extract the username and password
        username = request.form.get('username')
        password = request.form.get('password')
        # check if username and password were provided
        if not (username and password):
            # return appropriate error page
            return render_template(
                'main.html',
                page_name='Signup Failed',
                page_content='Need a username and password to sign up')
        # try to sign up the user with the backend
        try:
            user = backend.sign_up(username, password)
        except ValueError as ve:
            # return the appropriate error page
            return render_template('main.html',
                                   page_name='Signup Failed',
                                   page_content=str(ve))
        # no errors, call login_user method required by flask_login
        login_user(user)
        # return appropriate page letting the user know that sign up worked
        return render_template('main.html',
                               page_name='Signup Successful',
                               page_content='Successfully signed up!')
