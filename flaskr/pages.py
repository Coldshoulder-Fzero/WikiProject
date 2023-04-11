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
"""
added login_required to make sure that only autherized users can edit
"""
from flask import render_template, send_file, request, redirect, url_for
from flask_login import login_required


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
        print("Page Name:", page_name)
        print("Content:", content)

        # Check if the page_name value is not empty
       

        # Save content using the backend object
        backend.save_wiki_page(page_name, content)
        # Redirect to the updated page after saving
        return redirect(url_for('show_page', page_name=page_name))
        
    @app.route('/pages/<page_name>')
    def show_page(page_name):
        # get the content from the backend
        try:
            content = backend.get_wiki_page(page_name)
        except ValueError as ve:
            # return error to user if page is not foudn
            return render_template('main.html',
                                   page_name=page_name,
                                   page_content=str(ve))

        # render the show_page template with the title and content
        return render_template('show_page.html',
                               title=page_name,
                               content=content)

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
