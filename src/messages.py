import random

START_MESSAGE = '''Отправь стикер - а я тебе в ответ отправлю его как черно-белую картинку!'''

CANT_PROCESS_ANIMATED = '''Ойойой! 
Похоже это анимированный стикер! С такими работать не умею 😢 '''

CANT_PROCESS_VIDEO = '''Ойойой! 
Похоже это видео-стикер! С такими работать еще не умею 😢 
Но скоро научусь!'''

READY_MESSAGES = ["Готово!", "Готовченко!", "Опа!", "Лови!", "Это лучший стикер в мире", "Так только я умею!",
                  "Держи!", "Фигакс!", "БУМ!", "С вас 100 рублей!", "Во какой!", "Красотища!", "Круто! Ну круто же!!!"]


def get_random_ready_msg():
    return random.sample(READY_MESSAGES, 1)[0]
