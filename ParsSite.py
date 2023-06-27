from pprint import pprint


class Parser:
    def __init__(self):
        import requests
        from bs4 import BeautifulSoup as bs
        self.requests = requests
        self.bs = bs

    def pars_site(self, URL):
        response = self.requests.get(URL)
        print('start')
        soup = self.bs(response.content, "html.parser")
        print(2)
        words = []
        for text in soup.stripped_strings:
            for word in text.split():
                if word.isalpha() and word.isascii():
                    words.append(word)
        print(3)
        english_words = set()
        for word in words:
            if word.encode('ascii', 'ignore').decode('ascii') == word:
                english_words.add(word.lower())

        return english_words

if __name__ == '__main__':
    URL = 'https://www.oracle.com/java/technologies/javase-subscription-overview.html'
    p = Parser()
    pprint(p.pars_site(URL))