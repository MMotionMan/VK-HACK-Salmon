import vk_api
from pars import user_anal
from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import numpy as np
import scipy
import re
import pickle

def analyse_vk_profile(user_id):

    itog_info = []
    all_info = user_anal(user_id)
    if all_info[2] == 0:
        itog_info.append(' '.join(all_info[1]))
        itog_info.append('')
    else:
        itog_info.append(' '.join(all_info[1]))
        itog_info.append(' '.join(all_info[2].split(',')))
    g =[]
    g.append(itog_info[0] +' '+ itog_info[1])


    d = {'text':g}
    texts = pd.DataFrame(d,index = [1])
    vect = pickle.load(open('vectorizer.pickle', 'rb'))
    text = vect.transform(itog_info)

    words = vect.get_feature_names()
    words_train_densed = text.todense() # матрица
    n = 10

    row = words_train_densed[0]

    row = np.array(row)
    indices = (-row).argsort()[:n]
    indices = indices[0][:n]

    most_values_words = [words[j] for j in indices]
    s = ""
    for word in most_values_words:

        s += word + ','

    return most_values_words



