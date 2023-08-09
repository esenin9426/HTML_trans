import ParsSite
import Translate
import TelegramBot
import threading


if __name__ == '__main__':
        t3 = threading.Thread(target=TelegramBot.main())
        t1 = threading.Thread(target=Translate.main())
        t2 = threading.Thread(target=ParsSite.main())
        print('start')
        t3.start()
        t1.start()
        t2.start()

