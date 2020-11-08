import difflib
import requests

from libgen_api import LibgenSearch
from bs4 import BeautifulSoup

from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# For each book in the response, calculate the confidence score relative to the user search query and append it to object
def calculateConfidence( query, response ):
    
    for book in response:
        seq = difflib.SequenceMatcher(None, book['Title'] + " " + book['Author'] + str(book['Year']), query )
        lvl = seq.ratio()

        seq = difflib.SequenceMatcher(None, book['Title'] + " " + book['Author'], query)
        lvlTemp = seq.ratio()
        if lvlTemp > lvl: lvl = lvlTemp

        seq = difflib.SequenceMatcher(None, book['Title'], query)
        lvlTemp = seq.ratio()
        if lvlTemp > lvl: lvl = lvlTemp

        seq = difflib.SequenceMatcher(None, book['Author'], query)
        lvlTemp = seq.ratio()
        if lvlTemp > lvl: lvl = lvlTemp    

        book['confidence'] = lvl
    
    return response

def filterBooks( response ):

    output = []

    for book in response:
        if book['Extension'] == 'pdf' or book['Extension'] == 'epub': output.append( book )
    
    return output

def Cover_URL(array_books):
  for dicts in array_books:

    word = dicts["Title"]
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')
    dicts['Cover_url'] = images[1].get('src')

  return array_books

@app.route( '/' )
def index():
    return '<div style="font-size: 24px; font-weight: 600;">Hello, world!</div>'

@app.route('/ping')
def ping():
    return jsonify( { 'response': 'Pong!' } )

@app.route('/textbook-search', methods=['POST'])
def getTextbookSearchResults():
    if not request.json or not 'message' in request.json: abort(400)

    query = request.json['message']

    s = LibgenSearch()
    response = s.search_title( query )
    response = calculateConfidence( query, response )
    response = filterBooks( response )
    response = Cover_URL( response )
    response = sorted( response, key = lambda i: i['confidence'], reverse=True )

    return jsonify( response )