import psycopg2
from aiogram import types

async def insert_date_user_info(data: dict, cur, conn):
    # Запрос на вставку данных в таблицу
    query = "INSERT INTO public.user_info (date, user_id, username, last_name, first_name, message) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data["date"], data["id"], data["username"], data["last_name"],data["first_name"], data["message"])
    #Выполнение запроса на вставку данных
    cur.execute(query, values)
    # Сохранение изменений в базе данных
    conn.commit()

async def insert_user_answer(id_user, answer, right, conn, cur): #доделать
    # Запрос на вставку данных в таблицу
    query = "INSERT INTO public.user_answer (user_id, answer, right_a) VALUES (%s, %s, %s)"
    values = (id_user, answer, right)
    #Выполнение запроса на вставку данных
    cur.execute(query, values)
    # Сохранение изменений в базе данных
    conn.commit()

async def insert_url(data: dict, cur, conn):
    # Запрос на вставку данных в таблицу
    query = "INSERT INTO public.user_url (date, user_id, url, parsed) VALUES (%s, %s, %s, %s)"
    print(query)
    values = (data["date"], data["id"], data["url"], False)
    #Выполнение запроса на вставку данных
    cur.execute(query, values)
    # Сохранение изменений в базе данных
    conn.commit()

async def check_data(message: types.Message, conn, cur):
    query = f"select  count(1) from public.user_url where user_id = {message.chat.id}"
    cur.execute(query)
    # Получение результатов запроса
    cou = cur.fetchall()
    if cou[0] == 0:
        return True
    return False

async def set_chat_id(message: types.Message, conn, cur):
    res = {'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
     'id': message.chat.id,
     'username': message.chat.username,
     'last_name': message.chat.last_name,
     'first_name': message.chat.first_name,
     'message': message.text}
    await insert_date_user_info(res,cur, conn )
    print(res)

async def set_inspect_answer(id_user, answer, right, conn, cur):#доделать
    # Запрос на вставку данных в таблицу
    query = "INSERT INTO public.user_answer (user_id, answer, right_a) VALUES (%s, %s, %s)"
    values = (id_user, answer, right)
    #Выполнение запроса на вставку данных
    cur.execute(query, values)
    # Сохранение изменений в базе данных
    conn.commit()
async def set_url(message: types.Message, conn, cur):
    res = {'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
     'id': message.chat.id,
     'url': message.text}
    await insert_url(res,cur, conn )
    print(res)

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="0.0.0.0",
        port="5432",
        database="postgres",
        user="postgres",
        password="root")

    # Создание курсора для работы с базой данных
    cur = conn.cursor()
    conn.close()
    cur.close()
    # Закрытие соединения с базой данных
