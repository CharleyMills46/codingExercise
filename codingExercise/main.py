import os
import webbrowser
from flask import Flask, render_template, request
import requests
import re
import sys
from urllib.parse import quote

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    url = f'http://openlibrary.org/search.json?q={query}'
    results = []
    response = requests.get(url, verify=False)
    data = response.json()
    print(f"\nQuery: '{query}'", file=sys.stderr)
    print(f"Response size: {len(response.content)} bytes", file=sys.stderr)
    print(f"JSON data size: {len(str(data))} bytes\n", file=sys.stderr)
    for book_data in data['docs'][:10]:
        book = {
            'title': book_data.get('title', 'Unknown'),
            'author': ', '.join(book_data.get('author_name', ['Unknown'])),
            'url': f'https://openlibrary.org/search?q={query}'
        }
        results.append(book)

    return render_template('results.html', results=results)


def fixedsearch():
    query = request.args.get('q', '')
    url = f'http://openlibrary.org/search.json?'
    params = {
        'q': query,
        'limit': 10,
    }
    pattern = re.compile(r'^[a-zA-Z\s]+$')
    if re.match(pattern, query):
        response = requests.get(url, params=params, verify=False)
        results = []
        data = response.json()

        print(f"\nQuery: '{query}'", file=sys.stderr)
        print(f"Response size: {len(response.content)} bytes", file=sys.stderr)
        print(f"JSON data size: {len(str(data))} bytes\n", file=sys.stderr)

        for book_data in data['docs']:
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
    app.run(debug=True, use_reloader=False)