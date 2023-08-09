import os
import logging

from CreateQuestions import Interviewer
from SaveChatID import set_chat_id, set_url
import psycopg2

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

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    set_chat_id(message, conn=conn, cur=cur)
    await message.reply("Привет! Я бот, который может задавать тебе вопросы.")
    await bot.send_message(message.chat.id, "Выберите действия" ,reply_markup=markup(False))
    await message.delete()


# Обработчик команды /question
@dp.message_handler(commands=['question'])
async def process_question_command(message: types.Message):
    set_chat_id(message, conn=conn, cur=cur)
    # Выбираем случайный вопрос из списка
    question = Interviewer().question(message)
    Interviewer().log_question(question)
    # Создаем сообщение с вопросом и вариантами ответов
    text = f"{question['question']}"
    await message.answer(text)
    await bot.send_message(message.chat.id, "Введите Ваш ответ:", reply_markup=markup(question['options']))
    await dp.current_state(chat=message.chat.id, user=message.from_user.id).set_state('waiting_for_answer')
    await dp.current_state(chat=message.chat.id, user=message.from_user.id).update_data(question=question)

# Обработчик ответа на вопрос
@dp.message_handler(state='waiting_for_answer')
async def process_answer(message: types.Message, state: FSMContext):
    set_chat_id(message, conn=conn, cur=cur)
    # Получаем контекст пользователя
    data = await state.get_data()
    question = data['question']
    # Проверяем ответ пользователя
    if message.text == question['answer']:
        await message.answer("Правильно!")
    else:
        await message.answer("Неправильно!")
    # Сбрасываем состояние пользователя
    await state.finish()

@dp.message_handler(commands=['data'])
async def send_welcome(message: types.Message):
    set_chat_id(message, conn=conn, cur=cur)
    await message.reply("Давайте загрузим текст, который нужно перевести(на данный момент я могу принимать только URL сайта, но скоро я стану лучше:))")
    await dp.current_state(chat=message.chat.id, user=message.from_user.id).set_state('waiting_data')

    await message.delete()

@dp.message_handler(state='waiting_data')
async def process_download(message: types.Message, state: FSMContext):
    p = Parser()
#    t = Translator()
    set_url(message, conn=conn, cur=cur)
    """data = message.text
    for i in p.pars_site(URL=data):
        print(t.translate(i))"""

    await state.finish()

def main():
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        cur.close()
        conn.close()
# Запускаем бота
if __name__ == '__main__':
    main()
