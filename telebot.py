import random
import requests
import socket
import pickle
import time

import telebot
from telebot.types import Message
from telebot import apihelper


TOKEN = "818761782:AAE0t0i8IDX_TLbl47KmTFJYPiAMFH4_jC8"
#THUMB_URL = f'https://api.telegram.org/file/bot{TOKEN}/photos/file_2.jpg'
STICKER_ID = "CAADAgADqggAAgi3GQIQO4YOkKiCCQI"

USER = set()
def get_txt(site):
    r = requests.get(site)
    return r.text

def get_txt_data(html):
    """
    фОРМАТИРУЕМ ТЕКСТ УДАЛЯЕМ
    :param html:
    :return: ВЕРНЕМ ТЕКСТ БЕЗ ПЕРВЫХ 4 СТРОК И ДВУХ ПОСЛЕДНИХ
    """
    return html.split("\n")[4:-2]

def get_txt_filter(arr, filter=None):
    """
        Функция поиска в массиве по залоному фильтру
        arr принимает лист ['101.109.116.104:8080 TH-N-S + ', '..']
        filter строка 'A-S + '
        :param arr:
        :param filter:
        :return:
    """

    for proxi in arr:
        if proxi:
            if filter:
                if proxi.endswith(filter):
                    host = get_proxie_test(proxi.split(" ")[0])
                    if host:
                        return host
            else:
                return get_proxie_test(proxi.split(" ")[0])
        else:
            print("Line 27. Ошибка чтения")
            return False

def get_proxie_test(host):
    """
    Функция проверяет доступность прокси
    принимает переменную хост "134.209.106.81:8080"
    :param host:
    :return:
    """
    ip = host.split(":")[0]
    port = host.split(":")[1]

    s = socket.socket()
    s.settimeout(4)  ### сколько ждать соеденения с портом прокси
    print('Line 59. Хост\033[93m', ip + ':' + port, '\033[00m')
    try:
        s.connect((ip, int(port)))
    except socket.error:
        s.close()
        print('Line 64. Порт закрыт! Хост \033[31m' + ip + ':' + port, '!UNAVAILABLE!\033[00m')
    else:
        s.close()
        #with open('proxy_list_checked0.txt', 'a') as fa:
        print('Line 68. Хост:\033[32m', ip + ':' + port, 'AVAILABLE\033[00m')
        #fa.write(ip + ':' + port + '\n')
        return (ip+':'+port)
    return False

filt = ' + '
#filt = 'TR-A-S + '
arr = get_txt_data(get_txt('http://spys.me/proxy.txt'))
print(arr)
PROXIE = {'https': f'https://{get_txt_filter(arr, filt)}'}

apihelper.proxy = PROXIE
#print("Line 78. apihelper.proxy {}".format(apihelper.proxy))
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def command_handler(message: Message):
    bot.reply_to(message, 'Вери из но ансвер')
"""
@bot.message_handler(content_types=['text'])
def send_message_link(message: Message):
    bot.reply_to(message, 'www.ya.ru')
"""

#Функция отреагирует на любое сообщение от пользователя
@bot.message_handler(content_types=['text'])
def echo_digits(message: Message):
    #print(message.from_user.id)
    if 'Bilet' in message.text:
        bot.reply_to(message, 'Сколько нужно?')
        return
    reply = str(random.random())
    if message.from_user.id in USER:
        reply += f' {message.from_user}, hello again'
    bot.reply_to(message, reply)
    USER.add(message.from_user.id)
    print(USER)

@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    #print(message)
    #print(message.chat.id)
    #with open("C:/CAADAgADqggAAgi3GQIQO4YOkKiCCQI.jpg") as f:
        #print(f)
    bot.send_sticker(message.chat.id, STICKER_ID)

"""
@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
    print(inline_query)
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
    r = InlineQueryResultArticle('1', 'Подтвердить', InputTextMessageContent('Подтверждаю'), thumb_url=THUMB_URL)
    bot.answer_inline_query(inline_query.id, results=[r])

#bot.send_message(845809327, 'gogo power ranger')
"""
bot.polling(timeout=60)


