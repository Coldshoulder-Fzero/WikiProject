"""Creates all the endpoints related to retrieving content.
 
The following endpoints will be handled:

URI             | Method | Description
----------------|--------|-------------
/               | GET    | Returns the home page
/about          | GET    | Returns an about page
/images/<image> | GET    | Returns the image from backend.get_image
/pages          | GET    | Returns all of the pages in a list via backend.get_all_page_names
/pages/<page>   | GET    | Returns the page from backend.get_wiki_page
"""

from flask import render_template, send_file, request, redirect, url_for
from flask_login import  login_required, current_user


# Note: pages.py relies on the backend to fulfill some routes so we need to
# pass an instance of the backend (dependency injection)
def make_endpoints(app, backend):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template('main.html')

    @app.route('/pages')
    def pages():
        # Display a list of all the pages
        list_of_pages = backend.get_all_page_names()
        return render_template('pages.html', pages=list_of_pages)
    
    @app.route('/save_changes', methods=['POST'])
    def save_changes():
        page_name = request.form['page_name']
        content = request.form['content']


        # Check if the page_name value is not empty
        if not page_name.strip():
            return "Error: Page name cannot be empty", 400
        username = current_user.username
        backend.save_wiki_page(page_name, content, username)
        # Save content using the backend object
        # Redirect to the updated page after saving
        return redirect(url_for('show_page', page_name=page_name))

    @app.route('/pages/<page_name>/previous_version')
    @login_required
    def show_previous_version(page_name):
        content, timestamp, username = backend.get_previous_version(page_name)
        if content is None:
            return "No previous version found", 404

        return render_template('showing_previous_version.html', title=page_name, content=content, timestamp=timestamp, username=username, page=page_name)



    @app.route('/pages/<page_name>')
    def show_page(page_name):
        # get the content from the backend
        try:
            content = backend.get_wiki_page(page_name)
        except ValueError as ve:
            # return error to user if page is not found
            return render_template('main.html',
                                page_name=page_name,
                                content=str(ve))

        # render the show_page template with the title and content
        return render_template('show_page.html',
                            title=page_name,
                            content=content,
                            page_name=page_name
                            )


    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route('/images/<image>')
    def images(image):
        """Returns the image from the backend.

        This is a parameterized route where the identifier for the image we 
        want is passed in the route. We will call backend.get_image to get the 
        image contents.

        We use the send_file method provided by Flask to return the bytes of an
        image. Documentation can be found at 
        https://flask.palletsprojects.com/en/2.2.x/api/#flask.send_file

        Args:
            image: the name of the image that we want
        """
        return send_file(backend.get_image(image), mimetype='image/jpeg')
