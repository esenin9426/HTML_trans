import random

def question():
    questions = [
        {
            "question": "Какой язык программирования используется для разработки приложений на Android?",
            "options": ["Java", "Python", "C++", "JavaScript"],
            "answer": "Java"
        },
        {
            "question": "Какая операционная система является наиболее распространенной в мире?",
            "options": ["Windows", "Linux", "macOS", "Android"],
            "answer": "Windows"
        },
        {
            "question": "Какой язык программирования используется для создания веб-сайтов?",
            "options": ["F", "d", "HTML/CSS", "P"],
            "answer": "HTML/CSS"
        }
    ]

    return random.choice(questions)

def log_question(question: dict):
    print(question)