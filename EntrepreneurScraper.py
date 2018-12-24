from bs4 import BeautifulSoup as bsoup
from bs4 import SoupStrainer
import pandas as pd
# from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests as rq
import re
import warnings
warnings.simplefilter('ignore')



class GetPageParagraphs():
    # Input URL list, Base Url
    # Output List of paragraphs and texts
    def __init__(self, urlList, base_url):
        self.urls = urlList
        self.df = pd.DataFrame(columns = ['Site', 'Author', 'Text'])
        self.base = base_url

    def saveText(self):
        for page in self.urls:
            r = rq.get(page)
            soup = bsoup(r.text)

            authors = []
            for link in soup.findAll('a', {'data-action' : 'show-user-card'}):
                
                authors.append(link.text)
                # print link.text
            self.author = authors[1]

            sections = soup.findAll('section', {'class':'section section--body'})
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
            finals = []
            for para in total_text:
                for sentences in para.split('.'):
                    
                    finals.append(sentences)
            # print finals
            # total_text = [j for j in i.split('.') for i in total_text]
            Clength = len(finals)
            current_df = pd.DataFrame({'Site' : [self.base]*Clength, 'Author' : [self.author]*Clength, 'Text' : finals})
            self.df = pd.concat([self.df, current_df])
            # print "After Processing ", page
            # print self.df
        
    def getData(self):
        if len(self.df) > 0:
            return self.df
        else:
            self.saveText()
            return self.df


def main():

    # START HERE
    main_df = pd.DataFrame(columns = ['Site', 'Author', 'Text'])

    # BaseURLS = ['https://medium.freecodecamp.org/','https://medium.com/the-mission', 'https://hackernoon.com/', 'https://entrepreneurshandbook.co/', 'https://medium.com/personal-growth' ]
    BaseURLS = ['https://entrepreneurshandbook.co/']
    for base_url in BaseURLS:
            
        r = rq.get(base_url)

        soup = bsoup(r.text)
        # soup.prettify()

        URLlist = []
        for link in soup.find_all('a', href = True):
            currently_processing = link['href']
            if re.search(base_url, currently_processing):
                if '@' in  currently_processing or 'latest' in  currently_processing or 'about' in  currently_processing or 'archive' in  currently_processing or 'looking-for' in  currently_processing or 'write-for' in  currently_processing:
                    pass
                else:
                    URLlist.append(currently_processing)

        URLlist = list(set(URLlist))
        # for testing purpose
        # print URLlist
        # for _url in URLlist:
        #     req = rq.get(_url)
        #     print req.status_code, _url[:50]

        # for deployment
        CurrentCategory = GetPageParagraphs(URLlist, base_url)
        CurrentCategory.saveText()
        main_df = pd.concat([main_df,CurrentCategory.getData()])

    main_df.reset_index()
    main_df.to_csv('output.csv', encoding = 'utf-8' , index = False)
    print 'done'
if __name__ == '__main__':
    main()

                
