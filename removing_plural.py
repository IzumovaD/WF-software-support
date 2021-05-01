import re
import pymorphy2 
from root_allomorphs import root_allomorphs as allomorphs

#функция создания множества корней
def form_roots(root): 
    res = set()
    #проверка, есть ли алломорфы у корня
    for group in allomorphs:
        if root in group:
            res.update(group)
            return res
    #у корня нет алломорфов, группа состоит из одного корня
    res.add(root)
    return res

#функция определения части речи слова
def search_POS(word):
    POS = morph.parse(word)[0].tag.POS
    if POS == "NOUN":
        return "NOUN"
    if POS == "INFN" or POS == "VERB":
        return "VERB"
    if POS == "ADJF" or POS == "ADJS":
        return "ADJ"
    if POS == "PRTF" or POS == "PRTS":
        return "PARTICIPLE"
    if POS == "GRND":
        return "ADV PARTICIPLE"
    else:
        return "ADVERB"

#функция определения частей речи
def identify_POS(nest):
    res = {}
    for elem in nest:
        #приводим слово к обычному виду
        word = modify_word(elem)
        res[elem] = search_POS(word)
    return res

#функция приведения слова к обычному виду (без разделения на морфемы)
def modify_word(word):
    word = word.replace("+", "")
    word = word.replace("-", "")
    word = word.replace("*", "")
    return word.lower()

#функция определения числа существительного
def identify_number(word):
    word = modify_word(word)
    case = morph.parse(word)[0].tag.case
    #если не именительный падеж
    if case != "nomn":
        return "PLURAL"
    number = morph.parse(word)[0].tag.number
    if number == "plur":
        return "PLURAL"
    else: return "SINGULAR"

#функция поиска слова в единственном числе
def search_singular(word, words):
    pattern = word.split("*")[0]
    pattern = pattern.replace("+", "\+")
    pattern += "\*\w*"
    for elem in words:
        #исходное слово пропускаем
        if elem != word:
            #если слово совпадает с исходным с точностью до окончания
            if re.fullmatch(pattern, elem):
                return 1
    return 0 

#функция удаления слов во множ. числе
def del_plurals(words, pos_tags):
    words_to_del = []
    for word in words:
        if pos_tags[word] == "NOUN":
            if identify_number(word) == "PLURAL":
                #если в группе есть это же слово в единств. числе
                if search_singular(word, words):
                    #добавляем слово в число удаляемых
                    words_to_del.append(word)
    #обработка исключений (слов, которых нет в файле с признаками слов)
    for word in words:
        if (word not in words_to_del and word.endswith("*Ы") and
            search_singular(word, words)):
            words_to_del.append(word)
    #удаляем слова из группы
    for word in words_to_del:
        words.discard(word)

def nest_processing(nest):
    #проставляем словам части речи,
    #получаем словарь, где ключ - слово из nest, а значение - его часть речи
    pos_tags = identify_POS(nest)
    #удаляем слова во множ. числе
    del_plurals(nest, pos_tags)

def main_processing(data):
    #множество обрабатываемой в текущий момент группы слов
    curr_words = set()
    #новые группы слов
    new_groups = []
    #множество обрабатываемой в текущий момент группы алломорфных корней
    curr_roots = set()
    for line in data:
        #выделяем корень в слове
        res = re.search("\+\w+", line)
        root = res.group(0)[1:]
        root = root.lower()
        #выделяем слово из строки
        word = (line.split())[0]
        #обработка самого первого слова 
        if len(curr_roots) == 0:
            #формируем множество корней
            curr_roots = form_roots(root)
        else:
            #начало новой группы слов
            if root not in curr_roots:
                #обработка текущей группы слов
                nest_processing(curr_words)
                new_groups.append(curr_words)
                #формируем новое множество корней
                curr_roots = form_roots(root)
                #очищаем текущую групу слов 
                curr_words = set()
        #добавляем слово в текущую группу слов для обработки
        curr_words.add(word)
    #обработка самой последней группы слов
    nest_processing(curr_words)
    new_groups.append(curr_words)
    print_groups(new_groups)

#ф-ция печати новых групп в файл
def print_groups(new_groups):
    string = ""
    for group in new_groups:
        for word in group:
            string += word + "\n"
    out_file.write(string)


morph = pymorphy2.MorphAnalyzer()
in_file = open("PARONYM_TEST.txt", "r")
out_file = open("PARONYM_TEST_WITHOUT_PLURALS.txt", "w")
data = in_file.readlines()
main_processing(data)
out_file.close()
in_file.close()

