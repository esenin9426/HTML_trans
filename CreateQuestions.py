import random
from aiogram import types
import psycopg2

class Interviewer:
    def __init__(self):
        conn = psycopg2.connect(
            host="0.0.0.0",
            port="5432",
            database="postgres",
            user="parser_user",
            password="parser_user")

        # Создание курсора для работы с базой данных
        self.cur = conn.cursor()
        self.users_words = {}



    def question(self, message: types.Message):
        id_user = message.chat.id
        sql = f"""SELECT distinct uw.user_id, uw.word, wt.trsl 
                FROM public.url_words uw 
        		    inner join public.words_trsl wt on uw.word = wt.word
        		    where uw.user_id = {id_user}
        		    and wt.trsl not in (select  answer from user_answer
                                                        where user_id = {id_user}
                                                        group by answer
                                                        having count(right_a) >= 5)
        		    order by uw.word desc
        		    """

        self.cur.execute(sql)
        row = self.cur.fetchall()
        if len(row) == 0:
            sql = f"""SELECT distinct {id_user}, uw.word, wt.trsl 
                            FROM public.url_words uw 
                    		    inner join public.words_trsl wt on uw.word = wt.word
                    		    where uw.user_id = 0
                    		    and wt.trsl not in (select  answer from user_answer
                                                                    where user_id = {id_user}
                                                                    group by answer
                                                                    having count(right_a) >= 1)
                    		    order by uw.word desc
                    		    """
        self.cur.execute(sql)
        row = self.cur.fetchall()

        if len(row) == 0:
            questions = {
                "question": 0
            }
            return questions
        for i in row:
            i = list(i)
            self.users_words[i[0]] = self.users_words.get(i[0], []) + [[i[1], i[2]]]

        l = len(self.users_words[id_user])
        p = random.randint(0, l)

        min = p - 5
        max = p + 5
        if min < 0:
            min = 0
            max = min + 11
        if max > len(self.users_words[id_user]):
            max = len(self.users_words[id_user])
            min = max - 11

        words = []
        for i in range(min, p):
            words.append(self.users_words[id_user][i][1])
        for i in range(p + 1, max):
            words.append(self.users_words[id_user][i][1])
        r = words
        random.shuffle(r)
        v = r[:3] + [self.users_words[id_user][p][1]]
        random.shuffle(v)

        questions = {
                "question": self.users_words[id_user][p][0],
                "options": v,
                "answer": self.users_words[id_user][p][1]
            }

        return questions

    def log_question(self, question: dict):
        print(question)
