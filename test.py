from libgen_api import LibgenSearch # https://pypi.org/project/libgen-api/
import json
import difflib
import requests
from bs4 import BeautifulSoup

# print( json.dumps( response, indent=2 ) )

# {
# 		'ID'		: 'ID',
# 		'Author'	: 'Author',
# 		'Title'		: 'Title',
# 		'Publisher'	: 'Name',
# 		'Year'		: 'Year',
# 		'Pages'		: 'Pages',
# 		'Language'	: 'Lang',
# 		'Size'		: 'X',
# 		'Extension'	: 'Extension',
# 		'Mirror_1'	: 'URL1',
# 		'Mirror_2'	: 'URL2',
# 		'Mirror_3'	: 'URL3',
# 		'Mirror_4'	: 'URL4',
# 		'Mirror_5'	: 'URL5',
# 		'Edit'		: 'edit_URL'
# }

# calculate confidence - DONE
# how close is the query to the meta data of the reponse
# clean search
# remove results with less than a threshold of pages
# similarly remove results with tiny file sizes
# remove non-pdf values

# return list of good values sorted by best -> worst

# plan a UI

# calculateConfidenceLevels
# input: user query string, list of all books
# output: list of all books with confidence level added to their key

# Correct: book info from the website
# User: what the user has input as their search
# both are DICT variables
# Can add more seq to compare more values


def confidence_lvl(correct, user):
  lvl = 0.00
  for dicts in correct:
    seq = difflib.SequenceMatcher(None, dicts['Title'] + " " + dicts['Author'] + str(dicts['Year']), user )
    lvl = seq.ratio() * 100

    seq = difflib.SequenceMatcher(None, dicts['Title'] + " " + dicts['Author'], user)
    lvlTemp = seq.ratio() * 100
    if lvlTemp > lvl: lvl = lvlTemp

    seq = difflib.SequenceMatcher(None, dicts['Title'], user)
    lvlTemp = seq.ratio() * 100
    if lvlTemp > lvl: lvl = lvlTemp

    seq = difflib.SequenceMatcher(None, dicts['Author'], user)
    lvlTemp = seq.ratio() * 100
    if lvlTemp > lvl: lvl = lvlTemp    

    dicts['Confidence_lvl'] = lvl
  return correct

# input: array of books
# output: array of books cleaned of bad values
def FilterBooks(array_books):

  remove_list = []
  for book in array_books:
    if book['Extension'] != 'pdf':
      remove_list.append( book )
      continue

  for book in remove_list: array_books.remove( book )

  return array_books
  

def Cover_URL(array_books):
  for dicts in array_books:

    word = dicts["Title"]
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')
    dicts['Cover_url'] = images[1].get('src')

  return array_books

# Entry Point ---------------------------------------------------------------------------------------

s = LibgenSearch()

user_test_queries = [ "analysis of biological data", "mathematics", "statistics" ]
for query in user_test_queries:
  print( "\n=============\nUSER QUERY :: ", query )

  response = s.search_title(query)
  response = confidence_lvl( response, query )

  print( '# QUERIES :: ', len(response) )
  
  # filter books
  response = FilterBooks(response)

  response = Cover_URL(response)
  
  print( '# GOOD QUERIES :: ', len(response), '\n' )

  response = sorted( response, key = lambda i: i['Confidence_lvl'], reverse=True )

  count = 0
  for book in response:
    output = {
      "Author": book['Author'],
      "Title": book['Title'],
      "Confidence_lvl": book['Confidence_lvl'],
      "Extension": book['Extension'],
      "Cover_url": book['Cover_url']
    }

    print( json.dumps( output, indent=2 ) )
    count += 1
    if count == 5: break


#response = sorted(response, key = lambda i: i['Confidence_lvl'], reverse=True)
#print(json.dumps( response, indent=2 ))
