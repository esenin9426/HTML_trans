from pars_site import Parser
from translate import Translator

if __name__ == '__main__':
    URL = 'https://docs.oracle.com/javase/tutorial/collections/interfaces/index.html'
    t = Pars_site(URL)
    t2 = Parser()
    t2 = t2.pars_site(URL)
    translator = Translator()

    for i in t2[:10]:
        print(i + ' : ' + translator.translate(i))
