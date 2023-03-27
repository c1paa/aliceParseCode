# aliceParseCode

Код навыка Алисы в привотном доступе
Здесь только основная механика, парсинг, подбор слов...
Нужно скачать все 3 файла, запустить main.py, также должны быть установлены все библиотеки:

import random
from bs4 import BeautifulSoup
import requests
import urllib.parse
import io
from fuzzywuzzy import fuzz

Данный код генерирует случайное слово из 1001 и подбирает сочетания в которых оно может использоваться, выводит список в консоль
