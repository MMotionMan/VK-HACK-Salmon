import vk_api
from googletrans import Translator
import re
def trans(en_word):
    translator = Translator()
    word = (translator.translate(en_word, dest='ru')).text
    return word


def normal(gr_for_an):
    for i in range(len(gr_for_an)):
        gr_for_an[i] = gr_for_an[i].lower()
        gr_for_an[i] = re.sub('[^а-я0-9 ]', '', gr_for_an[i])
    return (gr_for_an)


def user_anal(user_id):
    t = open("logpass.txt","r",encoding = "UTF-8").readlines()
    login, password = t[0], t[1]


    vk = vk_api.VkApi(login, password, token='')
    vk.auth()
    vk = vk.get_api()
    user_ids = user_id
    user_info = vk.users.get(user_ids = user_ids , extended = 1,fields = ['bdate','interests'])
    user_info = user_info[0]

    try:
        user_bdate = user_info['bdate']
        if len(user_bdate.split('.')) <3: user_bdate = 0
    except: user_bdate = 0

    try:
        user_interests = user_info['interests']
        user_interests = normal(user_interests)
    except: user_interests = 0

    user_groups = vk.groups.get(user_id=user_ids,extended = 1, fields = 'description' )

    groups_bufer = user_groups['items']
    x=0
    groups_name = []
    try:
        for i in groups_bufer:
            word = str(i['name'])
            if word[0]<='z' and word[0]>='A':
                word = trans(word)
            groups_name.append(word)
            if x<25:
                x+=1
            else:
                break
    except: groups_name = 0

    #x = 0
    #groups_description = []
    #try:
    #   for i in groups_bufer:
    #       groups_description.append(i['description'])
    #       if x<25:
    #           x+=1
    #       else:
    #           break
    #except: groups_description = 0

    print("Не нормализованные данные: ",groups_name)
    groups_name = normal(groups_name)
    print("Нормализованный данные: ", groups_name)



    return user_bdate,groups_name,user_interests