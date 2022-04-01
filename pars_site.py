import requests
from bs4 import BeautifulSoup as bs
def Pars_site(URL):
    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')

    html_soup = soup.find_all('div')

    html_str = ''

    for i in html_soup:
        html_str += i.text
    html_str = ''.join([i.lower() for i in html_str if i.isalpha() or i == ' ']).split(' ')
    html_str = list(set(html_str))
    html_str.remove('')

    return html_str


if __name__ == '__main__':
    URL = 'https://docs.oracle.com/javase/tutorial/collections/interfaces/index.html'

    print(Pars_site(URL))