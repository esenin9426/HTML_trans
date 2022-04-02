from pars_site import Pars_site

if __name__ == '__main__':
    URL1 = 'https://docs.oracle.com/javase/tutorial/collections/interfaces/index.html'
    URL2 = 'https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/'
    t = Pars_site(URL1)
    t2 = Pars_site(URL2)
    print(t)
    print(t2)