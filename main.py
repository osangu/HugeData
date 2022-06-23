import matplotlib.pyplot as plt
from requests import get

from emoji import emojize, demojize

from bs4 import BeautifulSoup as Bs

import re
from time import sleep


def print_encode_warning(original, revision):
    print(emojize(f':red_exclamation_mark: {original} to {revision} for better result '))


class Scrawler:

    @property
    def language_list(self):
        _list = []
        request = get('https://pypl.github.io/PYPL.html')
        data = str(Bs(request.content, 'lxml').find('head').find('script')).split('<td>')

        for i in range(16):
            if i > 0:
                data[i] = str(data[i].replace('</td>', ' '))
                _list.append(data[i].split()[0])

        return _list


class LanguageListEditor:

    def __init__(self):
        self.__basic = ['C/C++', 'C++', 'C#']
        self.__wanted = self.__basic + ['C', 'R', 'Swift', 'Objective-C', 'Android']

        self.__basic_alternative = ['C%2D%2D', 'C%2D%2D', 'C%23']
        self.__wanted_alternative = self.__basic_alternative + ['C%2D%2D', '데이터 분석', 'IOS', 'IOS', 'Android']

    def change_for_usage(self, type: str, site: str, language_list: list):
        filter_list = self.__basic if site == 'github' else self.__wanted
        alternative_list = self.__basic_alternative if site == 'github' else self.__wanted_alternative

        if type == 'encode':
            answer = self.__change_list_instance(language_list, filter_list, alternative_list)
        elif type == 'decode':
            answer = self.__change_list_instance(language_list, alternative_list, filter_list)
        else:
            print(emojize(':face_with_monocle: 올바르지 않은 type으로 인해 원본 리스트를 반환합니다'))
            answer = language_list

        return answer

    @staticmethod
    def __change_list_instance(language_list: list, filter_list: list, alternative_list: list):
        for ind, val in enumerate(filter_list):
            if val in language_list:
                language_list.remove(val)
                if alternative_list[ind] in language_list: continue
                language_list.append(alternative_list[ind])
        return language_list