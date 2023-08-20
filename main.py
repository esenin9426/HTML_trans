import ParsSite
import Translate
import TelegramBot

import multiprocessing

def Pars():
    ParsSite.main()

def Trans():
    Translate.main()
def TBot():
    TelegramBot.main()

if __name__ == '__main__':

    p1 = multiprocessing.Process(target=Pars)
    p2 = multiprocessing.Process(target=Trans)
    p3 = multiprocessing.Process(target=TBot)


    p1.start()
    p2.start()
    p3.start()