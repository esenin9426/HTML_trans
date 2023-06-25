from time import sleep

from ParsSite import Parser
from translate import Translator
import TelegramBot
import os


if __name__ == '__main__':
        os.system('docker-compose up --build -d')
        URL = 'https://www.oracle.com/java/technologies/javase-subscription-overview.html'
        t1 = Parser()
        t1 = t1.pars_site(URL)
        translator = Translator()
        dictionary = {}
        for i in t1[:10]:
            dictionary[i] = translator.translate(i)
        print(dictionary)

        TelegramBot.main()