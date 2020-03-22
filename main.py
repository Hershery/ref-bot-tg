from threading import Thread
from refbot import referal_bot_loop
from distbot import distribution_bot_loop
from pay_handler import payment_handler_loop
from timer import timer_loop
from models import *
from telebot import TeleBot

bot = TeleBot('1110077491:AAGB8R4CMkPDWIb5TtO3BmoCM3FqMAic1Tk')
ref_link = 'https://telegram.me/{}?start={}'


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    splited = message.text.split()
    if not Users.user_exists(user_id):
        Users.create_user(user_id)
        if len(splited) == 2:
            Users.increase_ref_count(splited[1])
    bot.reply_to(message, text='hello')


@bot.message_handler(commands=['ref'])
def get_my_ref(message):
    bot_name = bot.get_me().username
    bot.reply_to(message, text=ref_link.format(bot_name, message.chat.id))


@bot.message_handler(commands=['ref_count'])
def get_my_refs(message):
    count = Users.get_ref_count(message.chat.id)
    bot.reply_to(message, text=f'Count: {count}')


if __name__ == '__main__':
    bot.polling(none_stop=True)

class ReferalBotThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        referal_bot_loop()


class DistributionBotThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        distribution_bot_loop()


class PaymentHandlerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        payment_handler_loop()


class TimerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        timer_loop()


if __name__ == "__main__":
    ReferalBotThread().start()
    print('Referal bot started')
    DistributionBotThread().start()
    print('Distribution bot started')
    PaymentHandlerThread().start()
    print('Pay handler started')
    TimerThread().start()
    print('Timer started')
