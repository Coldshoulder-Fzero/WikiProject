""" All endpoints related to uploads are created here.
 
Endpoints:
URI     | Method | Description
--------|--------|-------------
/upload | GET    | Returns the upload page
/upload | POST   | Extracts the name/data and calls backend.upload
"""

from flask import render_template, request, url_for, redirect
from flask_login import login_required

# Note: upload relies on the backend to fulfill some routes so we need to
# pass an instance of the backend (i.e. dependency injection)
def make_endpoints(app, backend):
    """Constructs the endpoints so we can upload to the wiki.

        Args:
            app: an instance of the Flask app
            backend: an object that allows our wiki to interact with the backend
    """

    @app.route('/upload')
    @login_required
    def upload():
        """Returns the upload page.

        This method should handle the GET request for /upload. We only want 
        users to upload when they are logged in so we add the @login_required 
        decorator.
        """

        return render_template('upload.html')
    
    @app.route('/upload', methods=['POST'])
    @login_required
    def upload_page():
        """Extracts the name and data to upload.

        This method should handle the POST request for /upload. We only want 
        users to upload when they are logged in so we add the @login_required 
        decorator. This method will call backend.upload to upload the contents 
        to the content bucket. If the name or data is missing or an error 
        occurs during upload, an appropriate error page is returned.
        """

        wiki_name = request.form.get('wikiname')
        wiki_content = request.files.get('wikicontent')
        # if we are missing the name for the page or the file to upload, return
        # an error page to the user.
        if not (wiki_content and wiki_content.filename and wiki_name):
            return render_template(
                'main.html',
                page_name='Unable to Upload',
                page_content='Need a file and name for the wiki page'
            )
        try:
            # for now, we assume that we are uploading text files so we need to
            # take the string contents of the file and upload it to the bucket
            backend.upload(wiki_name, wiki_content.stream.read())
        except ValueError as ve:
            # upload failed in the backend, return an error page to the user
            return render_template(
                'main.html',
                page_name='Upload Failed!',
                page_content=str(ve)
            )
        # redirect the user to the new wiki page that they uploaded
        return redirect(url_for('show_page', page_name=wiki_name))
