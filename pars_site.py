class Parser:
    def __init__(self):
        import requests
        from bs4 import BeautifulSoup as bs
        self.requests = requests
        self.bs = bs

    def pars_site(self, URL):
        r = self.requests.get(URL)
        soup = self.bs(r.text, 'html.parser')

        html_soup = soup.find_all('div')

        self.html_str = ''

        for i in html_soup:
            self.html_str += i.text
        self.html_str = ''.join([i.lower() for i in self.html_str if i.isalpha() or i == ' ']).split(' ')
        self.html_str = list(set(self.html_str))
        self.html_str.remove('')

        return self.html_str


if __name__ == '__main__':
    URL = 'https://docs.oracle.com/'
    p = Parser()
    print(p.pars_site(URL))