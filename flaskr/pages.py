from flask import request, render_template
from flask import * # to avoid writing flask.function  everytime
# from flask_Login import LoginManager

# login_manager = LoginManager()

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        
         return render_template('main.html')

    @app.route("/index")
    def index():
        return render_template('index.html')

    @app.route('/page1')
    def page1():
        return render_template('page1.html')

    @app.route('/page2')
    def page2():
        return render_template('page2.html')

    @app.route('/page3')
    def page3():
        return render_template('page3.html')
    @app.route('/page4')
    def page4():
        return render_template('page4.html')

    @app.route('/page5')
    def page5():
        return render_template('page5.html')

    @app.route('/page6')
    def page6():
        return render_template('page6.html')    
    @app.route('/page7')
    def page7():
        return render_template('page7.html')

    @app.route('/page8')
    def page8():
        return render_template('page8.html')

    @app.route('/page9')
    def page9():
        return render_template('page9.html')    
    @app.route('/page10')
    def page10():
        return render_template('page10.html')

    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route("/about")
    def about():
        return render_template('about.html') 

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        user = User(request.form.get('name'), request.form.get('password'))
        # form = LoginForm()
        # if form.validate_on_submit():
        #     login_user(user)
        #     flash('Logged in!')
        #     next = request.args.get('next')
        #     if not is_safe_url(next):
        #         return abort(400)
        #     return redirect(next or url_for('index'))
        return render_template('login.html')

    @app.route('/signup', methods=['GET'])
    def signup():
        return render_template('signup.html')

    # @app.route('/logout') @login_required
    # def logout():
    #     user = User(request.form.get('name'), request.form.get('password'))
    #     return render_template('logout.html')
