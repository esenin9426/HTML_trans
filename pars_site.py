import requests
from bs4 import BeautifulSoup as bs
def Pars_site(URL):
    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')

    html_soup = soup.find_all('div', id = 'PageContent')
    html_str = html_soup[0].text
    html_str = ''.join([i.lower() for i in html_str if  i.isalpha() or i == ' ']).split(' ')
    html_str = list(set(html_str))

    return html_str
