import os
import webbrowser
from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    url = f'http://openlibrary.org/search.json?q={query}'
    response = requests.get(url, verify=False)
    data = response.json()

    results = []
    for book_data in data['docs'][:10]:
        book = {
            'title': book_data.get('title', 'Unknown'),
            'author': ', '.join(book_data.get('author_name', ['Unknown'])),
            'url': f'https://openlibrary.org/search?q={query}'
        }
        results.append(book)

    return render_template('results.html', results=results)


if __name__ == '__main__':
    # Open the web page automatically in the default browser
    webbrowser.open('http://localhost:5000')

    # Start the Flask app with debug mode and reloader disabled
    app.run(debug=False, use_reloader=False)