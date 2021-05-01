import time
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
def vertex_search(nest, parts_of_speech):
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
def diff_search_allmrphs(word1, word2):
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
def derivate_search(parrent_words, nest, reflexives, privatives,
                    gerunds, participles, diffs, pos_tags):
    #множество уже обработанных слов
    proc_words = set()
    for key in parrent_words:
        for word in nest:
            if (word not in proc_words and word not in reflexives and
                word not in privatives and word not in gerunds and
                word not in participles):
                if (diff_search_allmrphs(morph_selection(key),
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

#функция определения частей речи группы слов
def identify_POS(nest):
    res = {}
    for elem in nest:
        word = modify_word(elem)
        res[elem] = search_POS(word)
    return res
        
#функция приведения слова к обычному виду (без разделения на морфемы)
def modify_word(word):
    word = word.replace("+", "")
    word = word.replace("-", "")
    word = word.replace("*", "")
    return word.lower()

#функция поиска производящих слов для возвратных слов
def producing_search_for_reflexives(nest, reflexives, diffs):
    proc_words = set()
    for key in nest:
        if not is_reflexive(key):
            for word in reflexives:
                if (word not in proc_words and
                    diff_search_allmrphs(morph_selection(key),
                                         morph_selection(word)) == diffs):
                    nest[key].append(word)
                    proc_words.add(word)
        #возвратное слово может быть производящим только для
        #других возвратных слов, причем с разницей = 1
        else:
            for word in reflexives:
                if (word not in proc_words and
                    diff_search_allmrphs(morph_selection(key),
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
                producing_search_for_reflexives(nest, reflexives, k)
                #если текущие цепочки больше не продолжить, заканчиваем цикл
                if old_len - len(nest) == 0:
                    break
        diffs += 1

#функция поиска производящих слов с наложенными на них условиями
def producing_search(nest, derived_words, cond, arg, diffs):
    proc_words = set()
    for word in derived_words:
        for key in nest:
            if (word not in proc_words and
                diff_search_allmrphs(morph_selection(key),
                                     morph_selection(word)) == diffs):
                if cond != True:
                    if arg != True:
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
    return (not is_privative(word))

#функция поверки наличия префиксов у слова
def has_not_prefix(word):
    if word.startswith("+"):
        return True
    return False

#функция обработки слов с отрицательным значением
def privatives_processing(privatives, nest):
    #первый проход - слова с отрицательными префиксами должны быть образованы
    #только от максимально похожих слов БЕЗ префиксов 
    producing_search(nest, privatives, has_not_prefix, True, 1)
    #второй проход - слова с отрицательными префиксами должны быть образованы
    #только от максимально похожих слов БЕЗ ОТРИЦАТЕЛЬНЫХ префиксов
    producing_search(nest, privatives, is_not_privative, True, 1)
    #третий и далее проход - слова с отрицательными префиксами могут быть 
    #образованы от любых максимально похожих на них слов
    diffs = 1
    while len(privatives) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                producing_search(nest, privatives, True, True, k)
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
def gerunds_participles_start(derived_words, nest, pos_tags):
    #определяем, есть ли в гнезде глаголы (полная или неполная группа)
    flag = False
    for word in nest:
        if is_verb(word, pos_tags):
            flag = True
            break
    if flag == False:
        #ищем самое короткое по числу морфем слово
        shortest = search_shortest(derived_words)
        #ищем для него производящее слово из гнезда
        diffs = 1
        while shortest in derived_words:
            for key in nest:
                if (diff_search_allmrphs(morph_selection(key),
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
    gerunds_participles_start(gerunds, nest, pos_tags)
    diffs = 1
    while len(gerunds) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                producing_search(nest, gerunds, is_gerund_or_verb, pos_tags, k)
                if old_len - len(nest) == 0:
                    break
        #увеличиваем допустимое число отличий
        diffs += 1

#функция поиска максимально соответствующего производящего
#глагола для причастия
def search_the_best_verb(nest, asp, trans, word, diffs, pos_tags):        
    for key in nest:
        if is_verb(key, pos_tags):
            modif_key = modify_word(key)
            p = morph.parse(modif_key)[0]
            #определяем вид
            aspect = p.tag.aspect
            #определяем переходность
            transitivity = p.tag.transitivity
            if trans == True and asp == True:
                if diff_search_allmrphs(morph_selection(key),
                                        morph_selection(word)) == diffs:
                    nest[key].append(word)
                    return key
            else:
                if asp == True:
                    if (transitivity == trans and
                        diff_search_allmrphs(morph_selection(key),
                                             morph_selection(word)) == diffs):
                        nest[key].append(word)
                        return key
                else:
                    if trans == True:
                        if (aspect == asp and
                            diff_search_allmrphs(morph_selection(key),
                                                 morph_selection(word)) == diffs):
                            nest[key].append(word)
                            return key

#функция поиска производящих слов для причастий
def producing_search_for_participles(participles, nest, diffs, pos_tags):
    proc_words = set()
    for word in participles:
        modif_word = modify_word(word)
        p = morph.parse(modif_word)[0]
        #определяем залог причастия
        voice = p.tag.voice
        #определяем время причастия
        tense = p.tag.tense
        #страдательное причастие настоящего времени
        if voice == "pssv" and tense == "pres":
            #ищем переходный глагол несовершенного вида
            key = search_the_best_verb(nest, "impf", "tran",
                                       word, diffs, pos_tags)
            if key != None:
                proc_words.add(word)
        else:
            #страдательное причастие прошедшего времени
            if voice == "pssv" and tense == "past":
                #ищем переходный глагол совершенного вида
                key = search_the_best_verb(nest, "perf", "tran",
                                           word, diffs, pos_tags)
                if key != None:
                    proc_words.add(word)
            else:
                #действительное причастие настоящего времени
                if voice == "actv" and tense == "pres":
                    #ищем переходный или непереходный глагол несовершенного вида
                    key = search_the_best_verb(nest, "impf", True,
                                               word, diffs, pos_tags)
                    if key != None:
                        proc_words.add(word)
                else:
                    #действительное причастие прошедшего времени
                    #ищем глагол любого вида и любой переходности
                    key = search_the_best_verb(nest, True, True,
                                               word, diffs, pos_tags)
                    if key != None:
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
def participles_processing(participles, nest, pos_tags):
    gerunds_participles_start(participles, nest, pos_tags)
    #допустимое число отличий
    diffs = 1
    while len(participles) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                #ищем максимально соответствующие производящие глаголы
                producing_search_for_participles(participles, nest, k, pos_tags)
                #ищем любые производящие глаголы
                producing_search(nest, participles, is_verb, pos_tags, k)
                #ищем любые производящие причастия
                producing_search(nest, participles, is_participle, pos_tags, k)
                if old_len - len(nest) == 0:
                    break
        diffs += 1

#функция обработки словообразовательного гнезда (СГ)
def nest_processing(vertices, nest):
    res = {}
    #проставляем словам части речи,
    #получаем словарь, где ключ - слово из nest, а значение - его часть речи
    pos_tags = identify_POS(nest)
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
    vertex = vertex_search(nest, pos_tags)
    res.update({vertex : []})
    vertices.append(vertex)
    nest.remove(vertex)
    #выполняем, пока все слова не будут распределены по словообразоват. цепочкам
    while len(nest) != 0:
        for k in range(0, diffs + 1):
            while 1:
                old_len = len(nest)
                derivate_search(res, nest, reflexives, privatives,
                                gerunds, participles, k, pos_tags)
                if old_len - len(nest) == 0:
                    break
        diffs += 1
        #добавляем новые дериваты только для вершины СГ
        for word in nest:
            if diff_search_allmrphs(morph_selection(vertex),
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
        participles_processing(participles, res, pos_tags)
    #обработка слов с префиксами НЕ и АНТИ
    privatives_processing(privatives, res)
    #обработка слов, оканчивающихся на СЯ и СЬ
    reflexives_processing(reflexives, res)
    return res

#основная функция обработки всех групп однокоренных слов 
def main_processing(data):
    #словообразовательные гнёзда - массив словарей, где в каждом словаре ключ - это
    #слово, а значение - массив производных от него слов
    #кроме того, есть отдельный элемент с ключом "vertex", хранящий вершину СГ
    word_formation_nests = []
    #массив вершин СГ
    vertices = []
    #множество обрабатываемой в текущий момент группы слов
    curr_words = set()
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
                word_formation_nests.append(nest_processing(vertices,
                                                            curr_words))
                #формируем новое множество корней
                curr_roots = form_roots(root)
                #очищаем текущую групу слов 
                curr_words = set()
        #добавляем слово в текущую группу слов для обработки
        curr_words.add(word)
    #обработка самой последней группы слов
    word_formation_nests.append(nest_processing(vertices, curr_words))
    print_nests_in_file(word_formation_nests, vertices)

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
def print_nests_in_file(word_formation_nests, vertices):
    #печать СГ в файл
    string = ""
    #отступ для отдельного уровня
    tab = "   "
    for i in range(0, len(vertices)):
        #вершину СГ печатаем без отступа
        string += vertices[i] + "\n"
        string += print_nest(word_formation_nests[i], vertices[i], 1)
    out_file.write(string)

#функция поиска группы родственных слов для заданного слова
def search_related_words(word):
    for dic in word_formation_nests:
        for key in dic:
            if modify_word(key) == word:
                return dic, key

#функция продолжения цепочки, начиная с заданного слова
def continue_chain(word):
    #поиск родственной группы слов для заданного слова
    nest, word = search_related_words(word)
    string = word + "\n"
    string += print_nest(nest, word, 1)
    print(string)

#функция печати цепочки
def print_chain(chain, word, k):
    res = ""
    if word not in chain:
        res += word + "\n"
    else:
        res += word + " --> " + print_chain(chain, chain[word], k + 1)
    return res 
    
#функция печати всех цепочек   
def print_all_chains(word, nest, chain):
    if word in vertices:
        string = print_chain(chain, word, 0)
        print(string)
        return
    for key in nest:
        if word in nest[key]:
            chain[key] = word
            print_all_chains(key, nest, chain)

#функция восстановления цепочки по конечному слову
def restore_chains(word):
    nest, word = search_related_words(word)
    print_all_chains(word, nest, {})

#консольный пользовательский интерфейс
def user_interface():
    while 1:
        print("Выберите действие:")
        print("1 - Восстановление цепочки по начальному слову")
        print("2 - Восстановление цепочки по конечному слову")
        print("3 - Выход")
        enter = int(input())
        if enter == 1:
            print("Введите слово:")
            word = input()
            continue_chain(word)
        if enter == 2:
            print("Введите слово:")
            word = input()
            restore_chains(word)
        if enter == 3:
            break


start_time = time.time()
morph = pymorphy2.MorphAnalyzer()
in_file = open("PARONYM_TEST_WITHOUT_PLURALS.txt", "r")
out_file = open("Word_Formation_Nests.txt", "w")
data = in_file.readlines()
main_processing(data)
out_file.close()
in_file.close()
print("--- %s seconds ---\n" % (time.time() - start_time))
user_interface()
