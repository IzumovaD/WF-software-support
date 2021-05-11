import time
import re
import pymorphy2

#функция, оставляющая только слова минимальной длины
def discard_applicants(words):
    min_len = 1
    #множество со словами минимальной длины
    res = set()
    while 1:
        for word in words:
            #приводим слово к обычному виду
            modif_word = modify_word(word)
            #не учитываем мягкий и твёрдый знаки
            modif_word = modif_word.replace("ь", "")
            modif_word = modif_word.replace("ъ", "")
            if len(modif_word) == min_len:
                res.add(word)
        if len(res) != 0:
            break
        min_len += 1
    return res

#функция отбора вершины СГ
def search_vertex(nest, parts_of_speech):
    #максимальное число морфем (корень и окончание не считаем)
    max_morphs = 0
    #текущие претенденты на вершину СГ
    applicants = set()
    while 1:
        for word in nest:
            #если число морфем в слове минимально для данной группы
            if word.count('-') == max_morphs:
                applicants.add(word)     
        if len(applicants) != 0:
            break
        max_morphs += 1
    #если нашёлся только один кандидат
    if len(applicants) == 1:
        return applicants.pop()
    #оставляем только кандидатов с наименьшим количеством букв
    applicants = discard_applicants(applicants)
    if len(applicants) == 1:
        return applicants.pop()
    #1-й приоритет - глаголы
    for word in applicants:
        #берём случайный
        if parts_of_speech[word] == "VERB":
            return word
    #2-й приоритет - существительные
    for word in applicants:
        if parts_of_speech[word] == "NOUN":
            return word
    #3-й приоритет - прилагательные/причастия
    for word in applicants:
        if (parts_of_speech[word] == "ADJ" or
            parts_of_speech[word] == "PARTICIPLE"):
            return word
    #4-й приоритет - наречия/деепричастия
    return applicants.pop()

#функция выделения морфем в слове
def morph_selection(word):
    #постфиксы тоже заносим в suff, окончания не важны
    res = {"pref": [], "root": [], "suff": []}
    temp = word.split("+")
    res["pref"].extend((temp[0].split("-"))[1:])
    #если слово имеет окончание
    if word.count("*") == 1:
        temp = temp[1].split("*")
        tmp = temp[0].split("-")
        res["root"].extend([tmp[0]])
        res["suff"].extend(tmp[1:])
        tmp = temp[1].split("-")
        res["suff"].extend(tmp[1:])
    #наречия, деепричастия, инфинитивы, нулевое окончание (окончания нет)
    else:
        temp = temp[1].split("-")
        res["root"].extend([temp[0]])
        res["suff"].extend(temp[1:])
    return res

#функция подсчёта количества отличий по одному виду морфем
#(без учёта алломорфизма)
def count_diffs(morph1, morph2):
    temp1 = list(morph1)
    temp2 = list(morph2)
    count = 0
    if len(temp1) <= len(temp2):
        count += len(temp2) - len(temp1)
        for elem in temp1:
            if elem in temp2:
                temp2.remove(elem)
            else:
                count += 1
    else:
        count = count_diffs(temp2, temp1)
    return count

#функция нахождения количества отличий в словах с учётом алломорфизма
def search_diff_allmrphs(word1, word2):
    diffs = 0
    for morph in word1:
        #учитываем только корневой алломорфизм
        if morph != "root":
            diffs += count_diffs(word1[morph], word2[morph])
    return diffs

#функция проверки наличия суффиксов СЯ и СЬ
def is_reflexive(word):
    morphs = morph_selection(word)
    if "СЯ" in morphs["suff"] or "СЬ" in morphs["suff"]:
        return True
    return False

#функция поверки наличия префиксов НЕ и АНТИ
def is_privative(word):
    morphs = morph_selection(word)
    if "НЕ" in morphs["pref"] or "АНТИ" in morphs["pref"]:
        return True
    return False

#функция поиска производных слов
def search_derivate(parrent_words, nest, reflexives, privatives,
                    gerunds, participles, diffs, pos_tags):
    #множество уже обработанных слов
    proc_words = set()
    for key in parrent_words:
        for word in nest:
            if (word not in proc_words and word not in reflexives and
                word not in privatives and word not in gerunds and
                word not in participles):
                if (search_diff_allmrphs(morph_selection(key),
                                         morph_selection(word)) == diffs and
                    not is_reflexive(word) and not is_privative(word) and
                    pos_tags[word] != "ADV PARTICIPLE" and
                    pos_tags[word] != "PARTICIPLE"):
                    #добавляем дериват по соответствующему ключу
                    parrent_words[key].append(word)
                    proc_words.add(word)
                else:
                    if is_reflexive(word):
                        reflexives.add(word)
                    else:
                        if is_privative(word):
                            privatives.add(word)
                        else:
                            if pos_tags[word] == "ADV PARTICIPLE":
                                gerunds.add(word)
                            else:
                                if pos_tags[word] == "PARTICIPLE":
                                    participles.add(word)
    for word in proc_words:
        #обработанные слова удаляем
        nest.discard(word)
        #потенциально каждое слово может быть производящим
        parrent_words.update({word: []})
    for word in reflexives:
        nest.discard(word)
    for word in privatives:
        nest.discard(word)
    for word in gerunds:
        nest.discard(word)
    for word in participles:
        nest.discard(word)

#функция определения части речи слова
def search_pos(word, morph):
    pos = morph.parse(word)[0].tag.POS
    if pos == "NOUN":
        return "NOUN"
    if pos in ("INFN", "VERB"):
        return "VERB"
    if pos in ("ADJF", "ADJS"):
        return "ADJ"
    if pos in ("PRTF", "PRTS"):
        return "PARTICIPLE"
    if pos == "GRND":
        return "ADV PARTICIPLE"
    return "ADVERB"

#функция определения частей речи группы слов
def identify_pos(nest, morph):
    res = {}
    for elem in nest:
        word = modify_word(elem)
        res[elem] = search_pos(word, morph)
    return res

#функция приведения слова к обычному виду (без разделения на морфемы)
def modify_word(word):
    word = word.replace("+", "")
    word = word.replace("-", "")
    word = word.replace("*", "")
    return word.lower()

#функция поиска производящих слов для возвратных слов
def search_producing_for_reflexives(nest, reflexives, diffs):
    proc_words = set()
    for key in nest:
        if not is_reflexive(key):
            for word in reflexives:
                if (word not in proc_words and
                    search_diff_allmrphs(morph_selection(key),
                                         morph_selection(word)) == diffs):
                    nest[key].append(word)
                    proc_words.add(word)
        #возвратное слово может быть производящим только для
        #других возвратных слов, причем с разницей = 1
        else:
            for word in reflexives:
                if (word not in proc_words and
                    search_diff_allmrphs(morph_selection(key),
                                         morph_selection(word)) == 1 and
                    is_reflexive(word)):
                    nest[key].append(word)
                    proc_words.add(word)
    for word in proc_words:
        reflexives.discard(word)
        nest.update({word: []})

#функция обработки возвратных глаголов, причастий и деепричастий
def reflexives_processing(reflexives, nest):
    #допустимое число отличий
    diffs = 1
    while len(reflexives) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                search_producing_for_reflexives(nest, reflexives, k)
                #если текущие цепочки больше не продолжить, заканчиваем цикл
                if old_len - len(nest) == 0:
                    break
        diffs += 1

#функция поиска производящих слов с наложенными на них условиями
def search_producing(nest, derived_words, cond, arg, diffs):
    proc_words = set()
    for word in derived_words:
        for key in nest:
            if (word not in proc_words and
                search_diff_allmrphs(morph_selection(key),
                                     morph_selection(word)) == diffs):
                if cond is not True:
                    if arg is not True:
                        if cond(key, arg):
                            nest[key].append(word)
                            proc_words.add(word)
                    else:
                        if cond(key):
                            nest[key].append(word)
                            proc_words.add(word)
                else:
                    nest[key].append(word)
                    proc_words.add(word)
    for word in proc_words:
        derived_words.discard(word)
        nest.update({word: []})

#вспомогательная функция
def is_not_privative(word):
    return not is_privative(word)

#функция поверки наличия префиксов у слова
def has_not_prefix(word):
    if word.startswith("+"):
        return True
    return False

#функция обработки слов с отрицательным значением
def privatives_processing(privatives, nest):
    #первый проход - слова с отрицательными префиксами должны быть образованы
    #только от максимально похожих слов БЕЗ префиксов
    search_producing(nest, privatives, has_not_prefix, True, 1)
    #второй проход - слова с отрицательными префиксами должны быть образованы
    #только от максимально похожих слов БЕЗ ОТРИЦАТЕЛЬНЫХ префиксов
    search_producing(nest, privatives, is_not_privative, True, 1)
    #третий и далее проход - слова с отрицательными префиксами могут быть
    #образованы от любых максимально похожих на них слов
    diffs = 1
    while len(privatives) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                search_producing(nest, privatives, True, True, k)
                if old_len - len(nest) == 0:
                    break
        diffs += 1

#функция поиска самого короткого по числу морфем слова
def search_shortest(words):
    #максимальное число морфем (корень и окончание не считаем)
    max_morphs = 0
    while 1:
        for word in words:
            if word.count('-') == max_morphs:
                return word
        max_morphs += 1

#функция обработки неполной группы
def incomplete_group(derived_words, nest, pos_tags):
    #определяем, есть ли в гнезде глаголы (полная или неполная группа)
    flag = False
    for word in nest:
        if is_verb(word, pos_tags):
            flag = True
            break
    if flag is False:
        #ищем самое короткое по числу морфем слово
        shortest = search_shortest(derived_words)
        #ищем для него производящее слово из гнезда
        diffs = 1
        while shortest in derived_words:
            for key in nest:
                if (search_diff_allmrphs(morph_selection(key),
                                         morph_selection(shortest)) ==
                    diffs):
                    nest[key].append(shortest)
                    derived_words.discard(shortest)
                    nest.update({shortest: []})
                    break
            diffs += 1

#функция определения, является ли слово глаголом или деепричастем
def is_gerund_or_verb(word, pos_tags):
    if pos_tags[word] == "VERB" or pos_tags[word] == "ADV PARTICIPLE":
        return True
    return False

#функция обработки невозвратных деепричастий
def gerunds_processing(gerunds, nest, pos_tags):
    incomplete_group(gerunds, nest, pos_tags)
    diffs = 1
    while len(gerunds) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                search_producing(nest, gerunds, is_gerund_or_verb, pos_tags, k)
                if old_len - len(nest) == 0:
                    break
        #увеличиваем допустимое число отличий
        diffs += 1

#функция поиска максимально соответствующего производящего
#глагола для причастия
def search_the_best_verb(morph, nest, asp, trans, word, diffs, pos_tags): 
    for key in nest:
        if is_verb(key, pos_tags):
            modif_key = modify_word(key)
            tags = morph.parse(modif_key)[0]
            #определяем вид
            aspect = tags.tag.aspect
            #определяем переходность
            transitivity = tags.tag.transitivity
            if trans is True and asp is True:
                if search_diff_allmrphs(morph_selection(key),
                                        morph_selection(word)) == diffs:
                    nest[key].append(word)
                    return key
            else:
                if asp is True:
                    if (transitivity == trans and
                        search_diff_allmrphs(morph_selection(key),
                                             morph_selection(word)) == diffs):
                        nest[key].append(word)
                        return key
                else:
                    if trans is True:
                        if (aspect == asp and
                            search_diff_allmrphs(morph_selection(key),
                                                 morph_selection(word)) == diffs):
                            nest[key].append(word)
                            return key

#функция поиска производящих слов для причастий
def search_producing_for_participles(morph, participles, nest, diffs, pos_tags):
    proc_words = set()
    for word in participles:
        modif_word = modify_word(word)
        tags = morph.parse(modif_word)[0]
        #определяем залог причастия
        voice = tags.tag.voice
        #определяем время причастия
        tense = tags.tag.tense
        #страдательное причастие настоящего времени
        if voice == "pssv" and tense == "pres":
            #ищем переходный глагол несовершенного вида
            key = search_the_best_verb(morph, nest, "impf", "tran",
                                       word, diffs, pos_tags)
            if key is not None:
                proc_words.add(word)
        else:
            #страдательное причастие прошедшего времени
            if voice == "pssv" and tense == "past":
                #ищем переходный глагол совершенного вида
                key = search_the_best_verb(morph, nest, "perf", "tran",
                                           word, diffs, pos_tags)
                if key is not None:
                    proc_words.add(word)
            else:
                #действительное причастие настоящего времени
                if voice == "actv" and tense == "pres":
                    #ищем переходный или непереходный глагол несовершенного вида
                    key = search_the_best_verb(morph, nest, "impf", True,
                                               word, diffs, pos_tags)
                    if key is not None:
                        proc_words.add(word)
                else:
                    #действительное причастие прошедшего времени
                    #ищем глагол любого вида и любой переходности
                    key = search_the_best_verb(morph, nest, True, True,
                                               word, diffs, pos_tags)
                    if key is not None:
                        proc_words.add(word)
    for word in proc_words:
        participles.discard(word)
        nest.update({word: []})

def is_verb(word, pos_tags):
    if pos_tags[word] == "VERB":
        return True
    return False

def is_participle(word, pos_tags):
    if pos_tags[word] == "PARTICIPLE":
        return True
    return False

#функция обработки невозвратных причастий без отрицательных префиксов
def participles_processing(morph, participles, nest, pos_tags):
    incomplete_group(participles, nest, pos_tags)
    #допустимое число отличий
    diffs = 1
    while len(participles) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                #ищем максимально соответствующие производящие глаголы
                search_producing_for_participles(morph, participles,
                                                 nest, k, pos_tags)
                #ищем любые производящие глаголы
                search_producing(nest, participles, is_verb, pos_tags, k)
                #ищем любые производящие причастия
                search_producing(nest, participles, is_participle, pos_tags, k)
                if old_len - len(nest) == 0:
                    break
        diffs += 1

#функция обработки словообразовательного гнезда (СГ)
def nest_processing(vertices, nest, morph):
    res = {}
    #проставляем словам части речи,
    #получаем словарь, где ключ - слово из nest, а значение - его часть речи
    pos_tags = identify_pos(nest, morph)
    #допустимое число отличий между словами в цепочке
    diffs = 0
    #слова, оканчивающиеся на СЯ и СЬ
    reflexives = set()
    #слова, начинающиеся с префиксов НЕ и АНТИ
    privatives = set()
    #невозвратные деепричастия
    gerunds = set()
    #невозвратные причастия без отрицательных префиксов
    participles = set()
    #поиск вершины СГ
    vertex = search_vertex(nest, pos_tags)
    res.update({vertex : []})
    vertices.append(vertex)
    nest.remove(vertex)
    #выполняем, пока все слова не будут распределены по словообразоват. цепочкам
    while len(nest) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                search_derivate(res, nest, reflexives, privatives,
                                gerunds, participles, k, pos_tags)
                if old_len - len(nest) == 0:
                    break
        diffs += 1
        #добавляем новые дериваты только для вершины СГ
        for word in nest:
            if search_diff_allmrphs(morph_selection(vertex),
                                    morph_selection(word)) == diffs:
                res[vertex].append(word)
                res.update({word: []})
        for word in res[vertex]:
            nest.discard(word)
    #обработка невозвратных деепричастий
    if len(gerunds) != 0:
        gerunds_processing(gerunds, res, pos_tags)
    #обработка невозвратных причастий
    if len(participles) != 0:
        participles_processing(morph, participles, res, pos_tags)
    #обработка слов с префиксами НЕ и АНТИ
    privatives_processing(privatives, res)
    #обработка слов, оканчивающихся на СЯ и СЬ
    reflexives_processing(reflexives, res)
    return res

#основная функция обработки всех групп однокоренных слов
def main_processing(data, out_file):
    count = 0
    start_time = time.time()
    morph = pymorphy2.MorphAnalyzer()
    #словообразовательные гнёзда - массив словарей, где в каждом словаре ключ - это
    #слово, а значение - массив производных от него слов
    #кроме того, есть отдельный элемент с ключом "vertex", хранящий вершину СГ
    word_formation_nests = []
    #массив вершин СГ
    vertices = []
    #множество обрабатываемой в текущий момент группы слов
    curr_words = set()
    for line in data:
        #начало новой группы слов
        if "------" in line:
            if len(curr_words) != 0:
                #обработка текущей группы слов
                count += 1
                word_formation_nests.append(nest_processing(vertices,
                                                            curr_words, morph))
                #очищаем текущую групу слов
                curr_words = set()
        else:
            #выделяем слово из строки
            word = (line.split())[0]
            #добавляем слово в текущую группу слов для обработки
            curr_words.add(word)
    print_nests_in_file(word_formation_nests, vertices, out_file)
    print("--- %s seconds ---\n" % (time.time() - start_time))
    print(count)
    user_interface(word_formation_nests, vertices)

#функция печати одного гнезда
def print_nest(nest, key, k):
    res = ""
    #отступ для отдельного уровня
    tab = "   "
    for word in nest[key]:
        #печать отступа
        for i in range(0, k):
            res += tab
        res += word + "\n" + print_nest(nest, word, k + 1)
    return res

#функция печати всех построенных гнёзд в файл
def print_nests_in_file(word_formation_nests, vertices,out_file):
    #печать СГ в файл
    string = ""
    for i, vertex in enumerate(vertices):
        #вершину СГ печатаем без отступа
        string += vertex + "\n"
        string += print_nest(word_formation_nests[i], vertex, 1)
    out_file.write(string)
