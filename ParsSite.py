class Parser:
    def __init__(self):
        import requests
        from bs4 import BeautifulSoup as bs
        self.requests = requests
        self.bs = bs

    def pars_site(self, URL):
        response = self.requests.get(URL)
        soup = self.bs(response.content, "html.parser")
        words = []
        for text in soup.stripped_strings:
            for word in text.split():
                if word.isalpha() and word.isascii():
                    words.append(word)
        english_words = set()
        for word in words:
            if word.encode('ascii', 'ignore').decode('ascii') == word:
                english_words.add(word.lower())

        return list(english_words)[:2]

    def parsing(self, conn, cur):
        query = "select user_id, url public.user_url where parsed = false LIMIT 1"

        cur.execute(query)

        # Получение результатов запроса
        row = cur.fetchone()
        print(row)


