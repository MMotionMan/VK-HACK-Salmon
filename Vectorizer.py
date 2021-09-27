from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import numpy as np
import scipy
import pymysql
import pickle

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

sql = "SELECT content from name"
cursor.execute(sql)

line = []
for row in cursor:
    line.append(row['content'])

d = {'text':line}
texts = pd.DataFrame(d)
texts.text = texts.text.replace('[^а-яА-Я0-9]', ' ', regex = True).str.lower()

for i in range(0, len(texts.text)):

    t_str = ""
    for word in texts.text[i].split(' '):

        if len(word) != 1:

            t_str += word + " "

    texts.text[i] = t_str

vectorizer = TfidfVectorizer()
words_train = vectorizer.fit_transform(texts.text) #тупая матрица с циферками
words = vectorizer.get_feature_names()
words_train_densed = words_train.todense() # матрица
pickle.dump(vectorizer, open('vectorizer.pickle', 'wb'))
n = 10

for i in range(0,len(words_train_densed)):

    row = words_train_densed[i]

    row = np.array(row)
    indices = (-row).argsort()[:n]
    indices = indices[0][:n]

    most_values_words = [words[i] for i in indices]
    sql = "UPDATE name set tags = %s where content = %s"
    s = ""
    for word in most_values_words:

        s += word + ','

    cursor.execute(sql, (s, line[i]))

cursor.close()