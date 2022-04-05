class Translator:
    def __init__(self):
        from deep_translator import GoogleTranslator
        self.GoogleTranslator = GoogleTranslator

    def translate(self, world = '', sourse_language = 'en', target_language = 'ru'):
        return self.GoogleTranslator(source= sourse_language , target=target_language).translate(world)
