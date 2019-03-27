from model.project import Project
import string
import random
import os.path
import jsonpickle
#библиотека для чтения опций командной строки
import getopt
#библиотека для использования опций командной строки
import sys


try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of groups", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

#указывыем значения параметров: количество генерируемых циклов,путь к файлу, в который будут записаны данные
n = 5
f = "data/project.json"

#  кортеж из названий переменных и значения, для вврдимых опций проверяются n и f для использования нижепо коду
for o, a in opts:
    if a == "-n":
        n = int(a)
    elif o == "-f":
        f = a



def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + ""*10 + string.punctuation
    return prefix+"".join(random.choice(symbols) for i in range(random.randrange(maxlen)))

def random_state():
    list = [10, 30, 50, 70]
    return random.choice(list)

def random_visible():
    list = '["10", "50"]'
    return random.choice(list)


testdata = [Project(name=random_string("name", 60), state=random_state(), enabled=random.choice([True, False]), visibility=random_visible(), description = random_string("desc", 128))
    for i in range(n)]


#склейка родительской директории текущего файла и названия файла, в который будут записаны тестовые данные, вложенная функция определяет абсолютный путь к текущему файлу
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

#открываем файл для записи по пути path для записи в него сгенерированных данных
with open(path, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
# параметр indent для переноса объектов списка в отдельные строки
    out.write(jsonpickle.encode(testdata))
