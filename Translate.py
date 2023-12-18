from time import sleep

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
        #print(world[0])
        return self.GoogleTranslator(source= sourse_language , target=target_language).translate(world[0])

    def translating(self):
        query = "select word from public.url_words where word not in (select word from words_trsl) limit 100"
        self.cur.execute(query)
        # Получение результатов запроса
        row = self.cur.fetchall()
        if len(row) == 0:
            return
        print('start translate')
        ins = []
        for i in row:
            word = self.translate(world=i)
            ins.append((i, word))
        insert = "INSERT INTO public.words_trsl (word, trsl) VALUES (%s, %s)"
        self.cur.executemany(insert, ins)
        self.conn.commit()
        print('end translate')


def main():
    print('start_t')
    t = Translator()
    while True:
        try:
            t.translating()
        except Exception as e:
            pass
            #print(e)

if __name__ == '__main__':
    main()