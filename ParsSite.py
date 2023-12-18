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

    def all_close(self):
        self.cur.close()
        self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()




    def pars_site(self, URL):
        response = self.requests.get(URL)
        soup = self.bs(response.content, "html.parser")
        words = []
        prepositions = ['about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'at', 'before',
                        'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning',
                        'considering', 'despite', 'down', 'during', 'except', 'for', 'from', 'in', 'inside', 'into',
                        'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'regarding',
                        'round', 'since', 'through', 'throughout', 'till', 'to', 'toward', 'under', 'underneath',
                        'until', 'up', 'upon', 'with', 'within', 'without']
        for text in soup.stripped_strings:
            for word in text.split():
                if word.isalpha() and word.isascii():
                    words.append(word)
        english_words = set()
        for word in words:
            if word.encode('ascii', 'ignore').decode('ascii') == word \
                    and word.encode('ascii', 'ignore').decode('ascii') not in prepositions:
                english_words.add(word.lower())

        return list(english_words)

    def parsing(self):
        query = "select user_id, url from public.user_url where parsed = false order by date"
        self.cur.execute(query)
        # Получение результатов запроса
        row = self.cur.fetchall()
        for i in row:
            print('start pars')
            try:
                word_list = self.pars_site(i[1])
            except Exception as e:
                print("we here")
                query = f"delete from public.user_url where user_id = {i[0]} and url = '{i[1]}'"
                self.cur.execute(query)
                self.conn.commit()
                #print(e)
            for j in word_list:
                query = "INSERT INTO public.url_words (user_id, url, word) VALUES (%s, %s, %s)"
                values = (i[0], i[1], j)
                self.cur.execute(query, values)
            query = f"update public.user_url set parsed = true where user_id = {i[0]} and url = '{i[1]}'"
            self.cur.execute(query)
            # Сохранение изменений в базе данных
            self.conn.commit()
            print('end pars')

def main():
    try:
        p = Parser()
        print('start_p')
        while True:
            try:
                p.parsing()
            except Exception as e:
                pass
                #print(e)
    finally:
        p.all_close()

if __name__ == '__main__':
    main()
