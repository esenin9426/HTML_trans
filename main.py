import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL = "https://docs.oracle.com/javase/tutorial/collections/interfaces/index.html"
r = requests.get(URL)
#print(r.status_code)
#print(r.text)

soup = bs(r.text, 'html.parser')
#print(soup)
html_soup = soup.find_all('div', id = 'PageContent')

#print(html_soup[0].text)
str_soup = list(set([str.lower(i) for i in html_soup[0].text.split(' ') if i.isalpha(): i = ' ']))

print(len(html_soup[0].text))
#str_soup = filter(str.isalpha, html_soup[0].text)
#str_soup = ' '.join(str_soup)
#for i in str_soup:
#    print(i, end = '\n')
print(len(str_soup))


