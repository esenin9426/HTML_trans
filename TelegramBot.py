import os
import logging
from CreateQuestions import question as q, log_question

from SaveChatID import set_chat_id

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

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

    markup.row(button6, button7, button5)
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
    await message.reply("Привет! Я бот, который может задавать тебе вопросы.")
    await bot.send_message(message.chat.id, "Выберите действия" ,reply_markup=markup(False))
    set_chat_id(message.chat.id)
    await message.delete()


# Обработчик команды /question
@dp.message_handler(commands=['question'])
async def process_question_command(message: types.Message):
    # Выбираем случайный вопрос из списка
    question = q()
    log_question(question)
    # Создаем сообщение с вопросом и вариантами ответов
    text = f"{question['question']}"
    await message.answer(text)
    await bot.send_message(message.chat.id, "Введите Ваш ответ:", reply_markup=markup(question['options']))
    await dp.current_state(chat=message.chat.id, user=message.from_user.id).set_state('waiting_for_answer')
    await dp.current_state(chat=message.chat.id, user=message.from_user.id).update_data(question=question)

# Обработчик ответа на вопрос
@dp.message_handler(state='waiting_for_answer')
async def process_answer(message: types.Message, state: FSMContext):
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


def main():
    executor.start_polling(dp, skip_updates=True)
# Запускаем бота
if __name__ == '__main__':
    main()
