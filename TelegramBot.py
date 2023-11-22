import os
import logging
from CreateQuestions import Interviewer
from SaveChatID import set_chat_id, set_url
import psycopg2
import redis

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from ParsSite import Parser
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="root")
# Создание курсора для работы с базой данных
cur = conn.cursor()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

storage = MemoryStorage()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def markup(answers):
    # Создание кнопок
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if answers:
        button1 = KeyboardButton(answers[0])
        button2 = KeyboardButton(answers[1])
        button3 = KeyboardButton(answers[2])
        button4 = KeyboardButton(answers[3])
        markup.row(button1, button2)
        markup.row(button3, button4)

    button5 = KeyboardButton('/start')
    button6 = KeyboardButton('/question')
    button7 = KeyboardButton('/data')
    button8 = KeyboardButton('/help')

    markup.row(button6, button7, button5, button8)
    return markup

# Создание клавиатуры с кнопками

load_dotenv()  # загрузить переменные из .env файла
TOKEN = os.getenv('TOKEN')  # получить значение переменной API_KEY

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
bot = Bot(token=TOKEN)

# Создаем объект диспетчера
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['help'])
async def process_question_command(message: types.Message):
    await set_chat_id(message, conn=conn, cur=cur)
    text = "Брат/Сеcтра меня создали для того чтобы я переводил тебе ссылки пендосовских сайтов, и потом мы с тобой учили слова, поэтому если ты тут первый раз, найди сайт который тебе нужен, копируй ссылку, жми /data отправь мне сайт, и дальше будет магия. " \
           "Если ты уже дедал это, то жми /question и наслаждайся"
    await message.answer(text)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    print(message)
    await set_chat_id(message, conn=conn, cur=cur)
    await message.reply("Привет! Я бот, который может задавать тебе вопросы, которые будут состоять из английских слов, из ссылок которые ты загрузишь нажав кнопку  /data")
    await bot.send_message(message.chat.id, "Выберите действия" ,reply_markup=markup(False))

async def do_question(message: types.Message):
    question = Interviewer().question(message)
    Interviewer().log_question(question)
    # Создаем сообщение с вопросом и вариантами ответов
    text = f"{question['question']}"
    await message.answer(text)
    await bot.send_message(message.chat.id, "Введите Ваш ответ:", reply_markup=markup(question['options']))
    question['options'] = str(question['options'])
    r.hset(message['from']['id'], mapping = question)

# Обработчик команды /question
@dp.message_handler(commands=['question'])
async def process_question_command(message: types.Message, state: FSMContext):
    await set_chat_id(message, conn=conn, cur=cur)
    await do_question(message)
    await state.finish()

@dp.message_handler(commands=['data'])
async def send_welcome(message: types.Message):
    await set_chat_id(message, conn=conn, cur=cur)
    await message.reply("Давайте загрузим текст, который нужно перевести(на данный момент я могу принимать только URL сайта, но скоро я стану лучше:))")
    await dp.current_state(chat=message.chat.id, user=message.from_user.id).set_state('waiting_data')
    await message.delete()

@dp.message_handler(state='waiting_data')
async def process_download(message: types.Message, state: FSMContext):
    await set_url(message, conn=conn, cur=cur)
    await state.finish()

@dp.message_handler()
async def echo(message: types.Message):
    await set_chat_id(message, conn=conn, cur=cur)
    print(message.text)
    answer = r.hgetall(message.chat.id)

    if message.text == answer['answer']:
        await message.answer("Правильно")

    elif message.text in answer['options']:
        await message.answer(f"Неправильно,  верный ответ - {answer['answer']}")
    else:
        await message.answer("""Брат/Сестра я хз чо ты напиcал/а. Этот дебил разработчик не научил меня обрабатывать это( мудак""")
        return
    await set_chat_id(message, conn=conn, cur=cur)
    await do_question(message)


def main():
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        cur.close()
        conn.close()
# Запускаем бота
if __name__ == '__main__':
    main()
