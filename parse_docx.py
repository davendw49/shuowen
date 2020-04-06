import pydocx
from bs4 import BeautifulSoup
import re
import codecs
import pymysql

import sys

chinese_set = []
book_set = []

def parse_middle_html(file):
    soup = BeautifulSoup(open(file))
    print(soup.prettify())
    
if __name__ == '__main__':
    # Pass in a path
    html = pydocx.PyDocX.to_html('data/sample.docx')
    parse_middle_html(html)