from flask import render_template
# from templates import login

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
         return render_template('main.html')

    # TODO(Project 1): Implement additional routes according to the project requirements.
    # @app.route("/login", methods=['GET'])
    # def login():
    #     if templates.login =='GET':
    #         return "Please log in"
    #     return render_template('login.html')