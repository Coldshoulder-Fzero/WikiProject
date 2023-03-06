from flask import render_template, request, redirect, abort, url_for
from google.cloud import storage
from flask import * # to avoid writing flask.function  everytime
# from flask_Login import LoginManager

# login_manager = LoginManager()

bucket = storage.Client().bucket("thewikicontent")
ryan = bucket.get_blob("Ryan.jpg")
james = bucket.get_blob("James.png")
cami = bucket.get_blob("cami.jpg")

bucket_name = "thewikicontent"
client = storage.Client()


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

def make_endpoints(app):

    @app.route("/")
    def home():
        return render_template('main.html')

    @app.route('/pages', methods=['GET', 'POST'])
    def pages():
        if request.method == 'POST':
            # Get the page name and text from the form data
            page_name = request.form['page_name']
            text = request.form['text']

            # Create a new blob with the page text
            blob = bucket.blob(f"{page_name}.txt")
            blob.upload_from_string(text)

            # Redirect the user to the new page
            return redirect(url_for('show_page', page_name=page_name))
        else:
            # Display a list of all the pages
            blobs = bucket.list_blobs()
            text_blobs = [blob for blob in blobs if blob.name.endswith('.txt')]
            pages = [blob.name[:-4] for blob in text_blobs]
            return render_template('pages.html', pages=pages)

    @app.route('/pages/<page_name>')
    def show_page(page_name):
        # get the content from the GCS bucket
        blob = bucket.get_blob(f"{page_name}.txt")

        if blob is None:
            # if the page doesn't exist, return a 404 error
            abort(404)

        # read the content from the blob and convert it to a string
        content = blob.download_as_string().decode('utf-8')

        # render the show_page template with the title and content
        return render_template('show_page.html', title=page_name, content=content)


    @app.route("/about")
    def about():
        ryan_url = ryan.public_url
        james_url = james.public_url
        cami_url = cami.public_url
        return render_template('about.html', ryan_url=ryan_url, james_url=james_url, cami_url=cami_url)


    @app.route('/sega')
    def sega():
        return render_template('sega.html')

    @app.route('/Atari')
    def Atari():
        return render_template('Atari.html')

    @app.route('/DS')
    def DS():
        return render_template('DS.html')
    @app.route('/MobileGaming')
    def MobileGaming():
        return render_template('MobileGaming.html')

    @app.route('/Nintendo')
    def Nintendo():
        return render_template('Nintendo.html')

    @app.route('/Playstation')
    def Playstation():
        return render_template('Playstation.html')    
    @app.route('/Steam')
    def Steam():
        return render_template('Steam.html')

    @app.route('/Tetris')
    def Tetris():
        return render_template('Tetris.html')

    @app.route('/Wii')
    def Wii():
        return render_template('Wii.html')    
    @app.route('/xbox')
    def xbox():
        return render_template('xbox.html')

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
