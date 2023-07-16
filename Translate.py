import psycopg2


class Translator:
    def __init__(self):
        from deep_translator import GoogleTranslator
        self.GoogleTranslator = GoogleTranslator
        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="translator",
            password="translator")

        # Создание курсора для работы с базой данных
        self.cur = self.conn.cursor()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()

    def translate(self, world = '', sourse_language = 'en', target_language = 'ru'):
        return self.GoogleTranslator(source= sourse_language , target=target_language).translate(world)

    def translating(self):
        query = "select word from public.url_words where word not in (select word from words_trsl) limit 10"
        self.cur.execute(query)
        # Получение результатов запроса
        row = self.cur.fetchall()
        for i in row:
            word = self.translate(world=i)
            insert = "INSERT INTO public.url_words (word, trsl) VALUES (%s, %s)"
            values = (i, word)
            self.cur.execute(insert, values)
        self.conn.commit()

if __name__ == '__main__':
    t = Translator()
    t.translating()