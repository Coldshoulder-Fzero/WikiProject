from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Add your logic to save the changes to the wiki
        return redirect(url_for('pages'))

    return render_template('pages.html')

if __name__ == '__main__':
    app.run(debug=True)
    