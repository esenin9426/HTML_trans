import psycopg2

class Parser:
    def __init__(self):
        import requests
        from bs4 import BeautifulSoup as bs
        self.requests = requests
        self.bs = bs

        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="parser_user",
            password="parser_user")

        # Создание курсора для работы с базой данных
        self.cur = self.conn.cursor()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()


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

    def parsing(self):
        query = "select user_id, url from public.user_url where parsed = false order by date"
        self.cur.execute(query)
        # Получение результатов запроса
        row = self.cur.fetchall()
        for i in row:
            word_list = self.pars_site(i[1])
            for j in word_list:
                query = "INSERT INTO public.url_words (user_id, url, word) VALUES (%s, %s, %s)"
                values = (i[0], i[1], j)
                self.cur.execute(query, values)
            query = f"update public.user_url set parsed = true where user_id = {i[0]} and url = '{i[1]}'"
            self.cur.execute(query)
            # Сохранение изменений в базе данных
            self.conn.commit()
            print(word_list)

if __name__ == '__main__':
    p = Parser()
    while True:
        try:
            p.parsing()
        except Exception as e:
            print(e)


