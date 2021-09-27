from spacy.lang.ru.lemmatizer import RussianLemmatizer
from spacy.lookups import Lookups
lookups = Lookups()
lookups.add_table("lemma_rules", {"noun": [["s", ""]]})
lemmatizer = RussianLemmatizer(lookups)

def cmp_tags(tag1, tag2):

    str1 = ""
    str2 = ""

    for word in tag1.split():
        str1 += lemmatizer((word),"NOUN")[0] + " "

    for word in tag2.split():

        str2 += lemmatizer((word),"NOUN")[0] + " "

    print(type(str1))
    print(str1)

    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)

    return float(len(c)) / (len(a) + len(b) - len(c))


