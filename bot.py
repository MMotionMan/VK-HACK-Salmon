import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
import pymysql
import dateparser
import pars
import vk_anal
import lemmatizer
import numpy as np

token_id = open("token_id.txt",'r',encoding='UTF-8').readlines()
token = token_id[0]
group_id = token_id[1]
vk_session = vk_api.VkApi(token=token[:len(token) - 1])
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=group_id)
letter = open('config/letter.txt','r',encoding='UTF-8')
help = open('config/help.txt', 'r', encoding='UTF-8')
db = open("db.txt",'r', encoding='UTF-8').readlines()

def get_connection():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=db[0],
                                 db='vk_hack',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection
connection = get_connection()


def get_button(mode):

    if mode == 0:

        return 'keyboard/button_assist.json'

    if mode == 1:

        return 'keyboard/answer'

    else:

        return 'keyboard/default.json'


def get_date(msg):

    date = dateparser.parse(msg)
    if (date != None):

        diff = str(date-datetime.datetime.now())
        #t = int(diff.split()[0])
        #if t < 0:
            #date = date + datetime.timedelta(days = abs(t))
        return date

    else :

        return None


# send message to user_id in vk with button mode
def vk_send(user_id, message, mode):

   # keyboard = get_button(mode)

    if message == ' ':

        vk.messages.send(peer_id=user_id,
                         random_id=get_random_id())#keyboard=keyboard)

    else:

        vk.messages.send(peer_id=user_id,
                         message=message,
                         random_id=get_random_id())#,keyboard=keyboard)

while True:

    was_sended = []

    for event in longpoll.listen():

        if event.type == VkBotEventType.GROUP_JOIN:

            user_id = event.obj.user_id
            vk_send(user_id, letter.read(), 0)

        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.from_user:

                user_id = event.object.message['peer_id']
                message = event.message['text']

                if message.lower() == 'помощь':

                    vk_send(user_id, help.read(), 0)

                else:

                    if message.lower() == 'поменять':

                        for i in was_sended:

                            if i[0] == user_id:

                                date = i[2]

                    date = get_date(message)

                    if (date == None):

                        vk_send(user_id,"Я получил не корректную дату! "
                                        "Если возникли вопросы с форматом, напиши 'помощь'",0)
                        continue

                    bdate, groups_name, interesting = pars.user_anal(user_id)

                    if (bdate) :

                        year = bdate.split('.')[2]
                        age = datetime.datetime.now().year - int(year)

                    else:
                        age = 100

                    cursor = connection.cursor()
                    sql = "SELECT name, description, content, tags,mean_price,start_time, place from name where Agerestr" \
                          " <= %s and start_time BETWEEN %s and %s" # добавить текущую дату
                    cursor.execute(sql, (age, date, date + datetime.timedelta(days=1)))

                    most_words = vk_anal.analyse_vk_profile(user_id)

                    arr = []
                    cursor_t = []
                    for row in cursor:

                        cursor_t.append(row)
                        if (row['tags'] is not None):
                            arr.append(lemmatizer.cmp_tags(" ".join(most_words), row['tags']))
                        else:
                            arr.append(0.05)


                    n = 30
                    if (n > len(arr)):

                        n = len(arr) - 1

                    arr = np.array(arr)
                    indices = (-arr).argsort()[:9]
                    indices = indices[:n]

                    best = arr[indices]
                    f = False
                    t = 0
                    for i in range(0, len(was_sended)):

                        if was_sended[i][0] == user_id:

                            t = was_sended[i][1]
                            was_sended[i][1] += 3

                            f = True

                    if not f:

                        t = 0
                        was_sended.append([user_id, 0, date])

                    start = t
                    i = 0
                    for row in cursor_t:

                        if ((t < len(indices)) and (i == indices[t])) and (t < start + i + 1):

                            i += 1
                            t += 1
                            vk_send(user_id, 'Название мероприятия: ' + row['name'] +
                                    '\n\n' + 'Описание мероприятия: ' + row['description'] +
                                    '\n\n' +  row['content'] +
                                    '\n\n' + 'Минимальная стоимость билета: ' + str(row['mean_price']) + " руб." +
                                    '\n\n' + 'Время начала мероприятия: ' + str(row['start_time']) +
                                    '\n\n' + 'Место проведения: ' + row['place'] +
                                    '\n_________________________________________\n', 0)

                        else:

                            break

                    cursor.close()