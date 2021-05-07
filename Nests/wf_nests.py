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

    def __form_root(self):
        pattern = re.compile(r"\+\w+")
        res = pattern.search(self.vertex)
        root = res.group(0)[1:]
        root = root.lower()
        return root

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

    def add_word(self, word, tabs):
        word = word.replace(" ", "")
        word = word.replace("\n", "")
        temp = [x for x in self.nest.keys() if x[1] == tabs - 3]
        parent = temp[-1]
        self.nest[parent].append(word)
        self.nest[(word, tabs)] = []

    def find_word(self, word):
        for key in self.nest:
            key = modify_word(key[0])
            if key == word:
                return True
        return False

    def find_root(self, root):
        root = modify_word(root)
        for elem in self.roots:
            if elem == root:
                return True
        return False

    def print_nest(self):
        res = ""
        tab = " "
        for key in self.nest:
            for i in range(0, key[1]):
                res += tab
            res += key[0] + "\n"
        print(res)


class Nests:
    def __init__(self):
        self.nests = []

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

    def find_nest_word(self, word):
        for nest in self.nests:
            if nest.find_word(word):
                return nest

    def find_nest_root(self, root):
        for nest in self.nests:
            if nest.find_root(root):
                return nest


def modify_word(word):
    word = word.replace("+", "")
    word = word.replace("-", "")
    word = word.replace("*", "")
    return word.lower()

def user_interface(all_nests):
    while 1:
        print("Выберите действие:")
        print("1 - Найти дерево по слову")
        print("2 - Найти дерево по корню")
        print("3 - Выход")
        enter = int(input())
        if enter == 3:
            break
        if enter == 1:
            print("Введите слово:")
            word = input()
            nest = all_nests.find_nest_word(word)
        if enter == 2:
            print("Введите корень:")
            root = input()
            nest = all_nests.find_nest_root(root)
        if nest is not None:
            nest.print_nest()
        else:
            print("Такого слова/корня нет ни в одном дереве")

def main_processing(data):
    all_nests = Nests()
    all_nests.collect_nests(data)
    user_interface(all_nests)
    
