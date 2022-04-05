from pars_site import Pars_site
from translate import Translator

if __name__ == '__main__':
    URL1 = 'https://docs.oracle.com/javase/tutorial/collections/interfaces/index.html'
    t = Pars_site(URL1)
    translator = Translator()

    for i in t[:10]:
        print(i + ' : ' + translator.translate(i))
