from ParsSite import Parser
from Translate import Translator
import TelegramBot
import os

if __name__ == '__main__':
        os.system('docker-compose up --build -d')
        TelegramBot.main()