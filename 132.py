import json
import re
from datetime import datetime
import pymysql
path = 'events.txt'
data = open(path,'r', encoding="UTF-8")

s = 0
# connect to db
def get_connection():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='qy.pr.wppw',
                                 db='vk_hack',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection
connection = get_connection()
cursor = connection.cursor()

for i in data:
    tags = []
    s+=1
    data_json = json.loads(i)

    name = data_json.get('name')
    age_restriction = data_json.get('ageRestriction')
    category = data_json.get('category').get('name')
    description = data_json.get('description')
    text = re.sub('[^а-яА-Я0-9 ]','',(data_json.get('content')[0]).get('text'))
    for j in data_json.get('tags'):
        tags.append(j.get('name'))
    is_free = data_json.get('isFree')
    if is_free == 'false':
        is_free = 0
    else:
        is_free = 1

    if data_json.get('schedules') != []:

        if data_json.get('schedules')[0].get('venue').get('place') != None:
            place = data_json.get('schedules')[0].get('venue').get('place').get('name')
        else:
            place = data_json.get('schedules')[0].get('venue').get('location').get('name')
        start_time = datetime.fromtimestamp((data_json.get("schedules")[0]).get('start')/1000)
        end_time = datetime.fromtimestamp((data_json.get("schedules")[0]).get('end')/1000)
        min_price = (data_json.get("schedules")[0]).get('ticketsInfo').get('minPrice')
        max_price = (data_json.get("schedules")[0]).get('ticketsInfo').get('maxPrice')
        print(place)
        sql = "INSERT INTO name(name,Agerestr,category,description,content,is_free,place,start_time," \
                      "end_time,mean_price,max_price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(name, age_restriction, category, description, text, is_free, place, start_time, end_time,min_price, max_price))
        connection.commit()


connection.close()

