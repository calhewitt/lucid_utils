import urllib
import json

# Functions for retrieving meta-analysis computed by Bernard (http://github.com/calhewitt/bernard)

BASE_PATH = "http://starserver.thelangton.org.uk/lucid-data-browser/api/"

def bernard_list():
    # Get a list of available tables to download
    stream = urllib.urlopen(BASE_PATH + "bernard_list")
    if not stream.getcode() == 200:
    	raise Exception("An error occurred whilst processing the request")
    tables = json.loads(stream.read())
    return tables

def bernard_dump(table_name):
    # Get a dump of a table from Bernard's output database
    # Format of [row1, row2...]
    # Column names not supplies
    pass

def bernard_schema(table_name):
    #TODO implement this!
    pass
