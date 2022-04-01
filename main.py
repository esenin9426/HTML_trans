from pars_site import Pars_site

if __name__ == '__main__':
    URL = 'https://docs.oracle.com/javase/tutorial/collections/interfaces/index.html'
    #URL = 'https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/'
    t = Pars_site(URL)
    print(Pars_site(URL))
    print(len(t))