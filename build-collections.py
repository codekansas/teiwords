from eulexistdb import db
from localsettings import *

from xml.etree import ElementTree as ET

from collections import Counter

import nltk
import os
import sys

'''
    This is a quick project to get some interesting data about these
    documents and try out the nltk package. You need to download nltk
    before using it.
'''

class TestExist:
    ''' Class used for connecting to Exist server '''
    def __init__(self):
        # Configure DJANGO_SETTINGS_MODULE for ExistDB
        os.environ['DJANGO_SETTINGS_MODULE'] = 'localsettings.py'
        self.db = db.ExistDB(server_url=EXISTDB_SERVER_URL)
        
    def get_data(self, query):
        result = list()
        qresult = self.db.executeQuery(query)
        hits = self.db.getHits(qresult)
        for i in range(hits):
            result.append(str(self.db.retrieve(qresult,i)))
        return result
    
def main():
    ''' Main method, runs when you run the script '''
    if '-help' in sys.argv or 'help' in sys.argv or '-h' in sys.argv or 'h' in sys.argv:
        # Print help text
        
        print 'HELP:'
        print '-t or -test: Run on external server'
        print '-l or -testlocatl: Run using local document'
        return
    elif '-testlocal' in sys.argv or '-l' in sys.argv:
        # Test on local document
        
        f = open('test.xml','r')
        txt = f.read()
        f.close()
        res = [txt]
    else:
        if '-test' in sys.argv or '-t' in sys.argv:
            # Test single document on exist server
            xquery = '''declare namespace tei='http://www.tei-c.org/ns/1.0';
                let $x := doc('/db/ewwrp/Arrow.xml')
                return $x/tei:TEI/tei:text'''
        else:
            # Test all documents on exist server
            xquery = '''declare namespace tei='http://www.tei-c.org/ns/1.0';
                let $x := xmldb:xcollection("/db/ewwrp/")
                return $x/tei:TEI/tei:text'''
        a = TestExist()
        res = a.get_data(xquery)
        data = []
    
    data = []
    
    for r in res:
        data = data + analyze(r)
    print data
    
def analyze(data):
    ''' Main method for analyzing a document '''
    root = ET.fromstring(data)
    
    # Read in text
    text = ''
    for i in root.itertext():
        text = text + i.strip() + ' '
    
    # Actual text analysis
    tokens = nltk.word_tokenize(text)
    pt = nltk.pos_tag(tokens)
    pt = [word for (word, tag) in pt if tag == 'NNP']
    c = Counter(pt)
    return c.most_common(25)
    
if __name__ == "__main__":
    ''' Boilerplate for running the script '''
    main()