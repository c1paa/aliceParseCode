import random
from bs4 import BeautifulSoup
import requests
import urllib.parse
import io
from fuzzywuzzy import fuzz

req_words = requests.get(url="http://dict.ruslang.ru/freq.php?act=show&dic=freq_s&title")

alfabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

bad_words = ['частность', 'водка', 'увеличение', '', 'пиво', 'сигарета']

open_words = []




# ФУНКЦИИ ДЛЯ СЕБЯ
def clear_string(num):
    for i in num:
        if alfabet.find(i) == -1:
            k = num.find(i)
            num = num[:k] + num[k + 1:]
        else:
            pass
    return num
def have_list(main_list, have_list):
    for i in main_list:
        for k in have_list:
            if (i == k):
                return True
    return False
def is_str_in_list(s, l):
    s = s.replace(" ", "")
    for i in l:
        if (s == i):
            return True
    return False



# ФУНКЦИИ ДЛЯ РАБОТЫ СО СЛОВАМИ
def find_word(words, index):
    index += 3
    word = words[index].text
    try:
        return clear_string(word.lower())
    except:
        pass

def get_simular_words(user_word_):
    user_word = user_word_
    search_word = urllib.parse.quote(str(user_word))
    u = "https://kartaslov.ru/%D1%81%D0%BE%D1%87%D0%B5%D1%82%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0/" + search_word
    # print(u)
    word_map = requests.get(url=u)
    with io.open("index_map.html", "w", encoding="utf-8") as file:
        try:
            file.write(word_map.text)
        except:
            file.close()

    with io.open("index_map.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup_map = BeautifulSoup(src, 'lxml')
    words = soup_map.find_all("td", class_="v2-contextual-td-left")
    ans = []
    for word in words:
        try:
            if (fuzz.ratio(word.find("a").text, user_word) > 50):
                continue
            if (len(word.find("a").text.lower().split()) > 1):
                try:
                    nice_words = []
                    exit_form_for = False
                    for i in range(len(word.find("a").text.lower().split())):
                        if (len(word.find("a").text.lower().split()[i]) > 4):
                            nice_words.append(False)
                        else:
                            nice_words.append(True)
                    for i in nice_words:
                        if (i == False):
                            exit_form_for = True
                    if (exit_form_for):
                        continue
                except:
                    pass

            ans.append(word.find("a").text)
        except:
            pass
    return ans

def add_to_file(path, text):
    with open(path, "a", encoding="utf-8") as file:
        try:
            file.write(text + "\n")
            file.close()
        except:
            file.close()

def generate_main_word():
    with open("index_words.html", "w") as file:
        try:
            file.write(req_words.text)
        except:
            file.close()
    with io.open("index_words.html", "r") as file:
        req_words_src = file.read()
    soup_words = BeautifulSoup(req_words_src, 'lxml')
    all_words_tds = soup_words.find_all("tr")

    word_index = random.randint(0, 1001)
    ans = find_word(all_words_tds, word_index)
    print(ans)
    while (is_str_in_list(ans, bad_words)):
        word_index = random.randint(0, 1001)
        ans = find_word(all_words_tds, word_index)
        print("bad!", ans)
    return ans

def generate_simular_words(num, word):
    sim_words = get_simular_words(word)
    ans = []
    for i in range(num):
        word_index = random.randint(0, len(sim_words) // 3)
        while (not is_str_in_list(sim_words[word_index], ans)):
            word_index = random.randint(0, len(sim_words) // 3)
        ans.append(sim_words[word_index])
        open_words.append(ans)
    return ans

'''
for k in range(1001):
    user_word = find_word(trs, k)
    #add_to_file("all_words.txt", user_word)
    search_word = urllib.parse.quote(str(user_word))
    u = "https://kartaslov.ru/%D1%81%D0%BE%D1%87%D0%B5%D1%82%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0/"+search_word
    #print(u)
    word_map = requests.get(url=u)
    #print(word_map.text)
    with io.open("index_map.html", "w", encoding="utf-8") as file:
        try:
            file.write(word_map.text)
        except:
            file.close()

    with io.open("index_map.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup_map = BeautifulSoup(src, 'lxml')
    words = soup_map.find_all("td", class_="v2-contextual-td-left")
    ans = []
    for word in words:
        try:
            if (fuzz.ratio(word.find("a").text, user_word) > 60):
                continue
            #print(word.find("a").text)
            ans.append(word.find("a").text)
        except:
            pass

    print(k, " - ",find_word(trs, k), " - главное слово", " - ", len(ans))
    if (len(ans) < 20):
        bad_words.append(find_word(trs, k))
    # for i in range(len(ans)):
    #     if (len(ans[i].lower().split()) > 1):
    #         print(ans[i])
    #         bad_words.append(ans[i])
    #print(ans)
'''

# print(len(bad_words))
# delete_bad_words()
w = generate_main_word()
print(get_simular_words(w))
# print(generate_simular_words(11, w))
