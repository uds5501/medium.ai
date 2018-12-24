from bs4 import BeautifulSoup as bsoup
from bs4 import SoupStrainer
import pandas as pd
# from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests as rq
import re
import warnings
warnings.simplefilter('ignore')

# base_url = 'https://entrepreneurshandbook.co/i-sat-down-with-a-millionaire-who-operates-10-businesses-while-sailing-around-the-world-with-his-338929c4e8c9'
base_url = "https://hackernoon.com/high-definition-data-eeab16b055a3"

r = rq.get(base_url)
soup = bsoup(r.text)
soup.prettify()

authors = []
for link in soup.findAll('a', {'data-action' : 'show-user-card'}):
    authors.append(str(link.text))
    # print link.text
print authors[1]

sections = soup.findAll('div', {'class':'section-inner sectionLayout--insetColumn'})
# print section_container
total_text = []
for section_container in sections:
    for ptag in section_container.find_all('p'):
        try:
            total_text.append(ptag.text)
        except UnicodeEncodeError:
            pass

    for h3 in section_container.find_all('h3'):
        try:
            total_text.append(h3.text)
        except UnicodeEncodeError:
            pass

    # for strong in section_container.find_all('strong'):
    #     try:
    #         total_text.append(h3.text)
    #     except UnicodeEncodeError:
    #         pass
Clength = len(total_text)
current_df = pd.DataFrame({'Site' : ['HackerNoon']*Clength, 'Author' : [authors[1]]*Clength, 'Text' : total_text})
print current_df