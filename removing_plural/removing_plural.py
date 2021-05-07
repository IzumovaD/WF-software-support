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

#функция определения частей речи
def identify_pos(nest, morph):
    res = {}
    for elem in nest:
        #приводим слово к обычному виду
        word = modify_word(elem)
        res[elem] = search_pos(word, morph)
    return res

#функция приведения слова к обычному виду (без разделения на морфемы)
def modify_word(word):
    word = word.replace("+", "")
    word = word.replace("-", "")
    word = word.replace("*", "")
    return word.lower()

#функция определения числа существительного
def identify_number(word, morph):
    if (word.endswith("Ы") or word.endswith("И") or word.endswith("А") or
        word.endswith("Я") or word.endswith("Е")):
        word = modify_word(word)
        case = morph.parse(word)[0].tag.case
        #если не именительный падеж
        if case != "nomn":
            return "PLURAL"
        number = morph.parse(word)[0].tag.number
        if number == "plur":
            return "PLURAL"
    return "SINGULAR"

#функция поиска слова в единственном числе
def search_singular(word, words):
    pattern = word.split("*")[0]
    pattern = pattern.replace("+", r"\+")
    pattern += r"\*\w*"
    for elem in words:
        #исходное слово пропускаем
        if elem != word:
            #если слово совпадает с исходным с точностью до окончания
            if re.fullmatch(pattern, elem):
                return 1
    return 0

#функция удаления слов во множ. числе
def del_plurals(words, pos_tags, morph):
    words_to_del = []
    for word in words:
        if pos_tags[word] == "NOUN":
            if identify_number(word, morph) == "PLURAL":
                #если в группе есть это же слово в единств. числе
                if search_singular(word, words):
                    #добавляем слово в число удаляемых
                    words_to_del.append(word)
    #удаляем слова из группы
    for word in words_to_del:
        words.discard(word)

def nest_processing(nest, morph):
    #проставляем словам части речи,
    #получаем словарь, где ключ - слово из nest, а значение - его часть речи
    pos_tags = identify_pos(nest, morph)
    #удаляем слова во множ. числе
    del_plurals(nest, pos_tags, morph)

def main_processing(data, out_file):
    morph = pymorphy2.MorphAnalyzer()
    #множество обрабатываемой в текущий момент группы слов
    curr_words = set()
    #новые группы слов
    new_groups = []
    #множество обрабатываемой в текущий момент группы алломорфных корней
    curr_roots = set()
    pattern = re.compile(r"\+\w+")
    for line in data:
        #выделяем корень в слове
        res = pattern.search(line)
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
                nest_processing(curr_words, morph)
                new_groups.append(curr_words)
                #формируем новое множество корней
                curr_roots = form_roots(root)
                #очищаем текущую групу слов
                curr_words = set()
        #добавляем слово в текущую группу слов для обработки
        curr_words.add(word)
    #обработка самой последней группы слов
    nest_processing(curr_words, morph)
    new_groups.append(curr_words)
    print_groups(new_groups, out_file)

#ф-ция печати новых групп в файл
def print_groups(new_groups, out_file):
    string = ""
    for group in new_groups:
        for word in group:
            string += word + "\n"
    out_file.write(string)
