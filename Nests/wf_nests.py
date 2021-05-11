import re
from collections import OrderedDict
from root_allomorphs import root_allomorphs as allomorphs

class Nest:
    def __init__(self, vert):
        vert = vert.replace("\n", "")
        self.nest = OrderedDict([((vert, 0), [])])
        self.vertex = vert
        root = self.__form_root()
        self.roots = self.__form_roots(root)

    #функция выделения корня в слове
    def __form_root(self):
        pattern = re.compile(r"\+\w+")
        res = pattern.search(self.vertex)
        root = res.group(0)[1:]
        root = root.lower()
        return root

    #функция формирования группы алломорфных корней
    def __form_roots(self, root):
        res = set()
        #проверка, есть ли алломорфы у корня
        for group in allomorphs:
            if root in group:
                res.update(group)
                return res
        #у корня нет алломорфов, группа состоит из одного корня
        res.add(root)
        return res

    #функция добавления слова в дерево
    def add_word(self, word, tabs):
        word = word.replace(" ", "")
        word = word.replace("\n", "")
        temp = [x for x in self.nest.keys() if x[1] == tabs - 3]
        parent = temp[-1]
        self.nest[parent].append(word)
        self.nest[(word, tabs)] = []

    #функция поиска слова в дереве
    def find_word(self, word):
        for key in self.nest:
            if self.modify_word(key[0]) == word:
                return key[0]
        return False

    #функция поиска корня в дереве
    def find_root(self, root):
        root = self.modify_word(root)
        for elem in self.roots:
            if elem == root:
                return True
        return False

    def __iter__(self):
        self.iterator = iter(self.nest)
        return self

    def __next__(self):
        try:
            key = next(self.iterator)
        except StopIteration:
            raise StopIteration
        else:
            return (key[0], key[1], self.nest[key])

    #функция извлечения поддерева по заданной вершине
    def restore_subtree(self, word, nest):
        word = word.lower()
        iterator = iter(nest)
        key, tabs, value = next(iterator)
        while self.modify_word(key) != word:
            key, tabs, value = next(iterator)
        subtree = Nest(key)
        vertex_tab = tabs
        key, tabs, value = next(iterator)
        while tabs != vertex_tab:
            subtree.nest[(key, tabs-vertex_tab)] = self.nest[(key, tabs)]
            key, tabs, value = next(iterator)
        return subtree

    def __str__(self):
        res = ""
        tab = " "
        for key in self.nest:
            for i in range(0, key[1]):
                res += tab
            res += key[0] + "\n"
        return res

    def modify_word(self, word):
        word = word.replace("+", "")
        word = word.replace("-", "")
        word = word.replace("*", "")
        return word.lower()

    #функция перевода цепочки в строку
    def chain_to_str(self, chain, word):
        string = ""
        if word not in chain:
            string += word + "\n"
        else:
            string += word + " --> " + self.chain_to_str(chain, chain[word])
        return string    

    #функция формирования и печати цепочки по конечному слову
    def restore_chain(self, word, chain, nest):
        if word == self.vertex:
            print(self.chain_to_str(chain, word))
            return
        for key, tabs, value in nest:
            if word in value:
                chain[key] = word
                self.restore_chain(key, chain, nest)


class Nests:
    def __init__(self, data):
        self.nests = []
        self.collect_nests(data)

    #функция сбора деревьев из файла
    def collect_nests(self, data):
        nest = Nest(data[0])
        data = data[1:]
        for line in data:
            tabs = line.count(" ")
            if tabs == 0:
                self.nests.append(nest)
                nest = Nest(line)
            else:
                nest.add_word(line, tabs)
        self.nests.append(nest)

    #функция поиска слова во всех деревьях 
    def find_word_nest(self, word):
        word = word.lower()
        for nest in self.nests:
            if nest.find_word(word) is not False:
                return nest
        raise Exception("Такого слова нет ни в одном дереве.")

    #функция поиска корня во всех деревьях
    def find_root_nest(self, root):
        root = root.lower()
        for nest in self.nests:
            if nest.find_root(root):
                return nest
        raise Exception("Такого корня нет ни в одном дереве.")
    

def user_interface(all_nests):
    while 1:
        print("Выберите действие:")
        print("1 - Найти дерево по слову")
        print("2 - Найти дерево по корню")
        print("3 - Восстановление поддерева по начальному слову")
        print("4 - Восстановление цепочки по конечному слову")
        print("5 - Выход")
        enter = int(input())
        if enter == 5:
            break
        if enter == 1:
            print("Введите слово:")
            word = input()
            try:
                nest = all_nests.find_word_nest(word)
            except Exception as e:
                print(e)
            else:
                print(nest)
        if enter == 2:
            print("Введите корень:")
            root = input()
            try:
                nest = all_nests.find_root_nest(root)
            except Exception as e:
                print(e)
            else:
                print(nest)
        if enter == 3:
            print("Введите слово:")
            word = input()
            try:
                nest = all_nests.find_word_nest(word)
            except Exception as e:
                print(e)
            else:
                subtree = nest.restore_subtree(word, nest)
                print(subtree)
        if enter == 4:
            print("Введите слово:")
            word = input()
            try:
                nest = all_nests.find_word_nest(word)
            except Exception as e:
                print(e)
            else:
                word = nest.find_word(word.lower())
                nest.restore_chain(word, {}, nest)
                
