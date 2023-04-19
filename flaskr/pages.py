"""Creates all the endpoints related to retrieving content.

The following endpoints will be handled:

URI                                      | Method   | Description
-----------------------------------------|----------|-----------------------------------
/                                        | GET      | Returns the home page
/about                                   | GET      | Returns an about page
/images/<image>                          | GET      | Returns the image from backend.get_image
/pages                                   | GET      | Returns all of the pages in a list via backend.get_all_page_names
/pages/<page>                            | GET      | Returns the page from backend.get_wiki_page
/page/<page_name>/previous               | GET,POST | Handles showing and reverting to the previous version of a wiki page
/pages/<page_name>/showing_previous_version | GET   | Displays the previous version of a wiki page
/pages/<page_name>/previous_versions     | GET      | Lists all previous versions of a wiki page
"""
"""
added login_required to make sure that only autherized users can edit
"""
from flask import render_template, send_file, request, redirect, url_for, flash
from flask_login import login_required, current_user


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
    @login_required
    def save_changes():
        page_name = request.form['page_name']
        content = request.form['content']


        # Check if the page_name value is not empty
        if not page_name:
            error_message = "Error: Page name cannot be empty."
            return render_template('error.html', error_message=error_message), 400

        # Save content using the backend object
        backend.save_wiki_page(page_name, content, current_user.username)
        
        # Redirect to the updated page after saving
        return redirect(url_for('show_page', page_name=page_name))

        
    @app.route('/pages/<page_name>')
    def show_page(page_name):
        # get the content from the backend
        try:
            content = backend.get_wiki_page(page_name)
        except ValueError as ve:
            # return error page to user if page is not found
            return render_template('error.html',
                                page_name=page_name,
                                error_message=str(ve)), 404

        # render the show_page template with the title and content
        return render_template('show_page.html',
                                content=content,
                                page_name=page_name)


    @app.route('/pages/<page_name>/showing_previous_version', methods=['GET'])
    @login_required
    def showing_previous_version(page_name):
        content, timestamp, username = backend.get_previous_version(page_name)
            
        if content is None or timestamp is None or username is None:
            return "No previous version found", 404

        return render_template('showing_previous_version.html', page_name=page_name, content=content, timestamp=timestamp, username=username)
    """
    The flash() method in Flask is used to display temporary messages to the user.
    These messages are called "flash messages." When you call flash() with a message,
    the message is stored temporarily and can be rendered in the HTML templates 
    using the get_flashed_messages() function.
    """        
    @app.route("/page/<page_name>/previous", methods=["GET", "POST"], endpoint='show_previous_version')
    @login_required
    def replace_with_previous_version(page_name):
        if backend.revert_to_previous(page_name, current_user.username):
            flash('Page reverted to the previous version.')
        else:
            flash('No previous version available to revert to.')
        return redirect(url_for('show_page', page_name=page_name))

            
    @app.route('/pages/<page_name>/previous_versions')
    def previous_versions(page_name):
        previous_versions = backend.get_all_previous_versions(page_name)
        return render_template('previous_versions.html', page_name=page_name, previous_versions=previous_versions)
    
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
