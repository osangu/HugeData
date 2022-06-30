import matplotlib.pyplot as plt
from requests import get

from emoji import emojize, demojize

from bs4 import BeautifulSoup as Bs

import re
from time import sleep

import numpy as np


class LanguageListEditor:

    def __init__(self):
        self.__basic = ['C/C++', 'C++', 'C#']
        self.__wanted = self.__basic + ['C', 'R', 'Swift', 'Objective-C', 'Kotlin']

        self.__basic_alternative = ['C%2B%2B', 'C%2B%2B', 'C%23']
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


class Scrawler:

    def __init__(self, lang_list_editor: LanguageListEditor):
        self._list_editor = lang_list_editor

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

    @property
    def job_amount_list(self):
        lang_list = self._list_editor.change_for_usage('encode', 'wanted', self.language_list)
        job_amount_list = []

        for language in lang_list:
            for cnt in range(20):
                request = get(
                    f'https://www.wanted.co.kr/api/v4/jobs?1655641140814&country=kr&job_sort=company.response_rate_order&locations=all&years=-1&query={language}&limit=100&offset={100 * cnt}'
                ).json()

                amount = len(request['data'])

                if 100 > amount != 0:
                    job_amount_list.append(100 * cnt + amount)
                    break

        return (
            self._list_editor.change_for_usage('decode', 'wanted', lang_list), job_amount_list
        )

    # ['Python', 'Java', 'JavaScript', 'PHP', 'TypeScript', 'Matlab', 'Go', 'Rust', 'Ruby', 'C/C++', 'C#', 'R', 'Swift', 'Kotlin']
    # [81, 267, 18, 72, 18, 1, 157, 2, 2, 58, 39, 108, 371, 236]

    @property
    def repository_amount_list(self):
        language_list = self._list_editor.change_for_usage('encode', 'github', self.language_list)
        repository_amount_list = []

        for language in language_list:
            request = get(f'https://github.com/search?l={language}&q={language}&type=Repositories').text

            soup = str(Bs(request, 'lxml').find('body').find_all('h3')[2])
            start = re.match('<h3>', soup).span()[1]
            finish = soup.find(' repository results')

            repository_amount_list.append(
                int(soup[start:finish].translate(
                    str.maketrans('<span class="v-align-middle"> Showing,available\n',
                                  ' ' * len('<span class="v-align-middle"> Showing,available\n'))
                ).replace(' ', ''))
            )
            sleep(8)

        return (
            self._list_editor.change_for_usage('decode', 'github', language_list), repository_amount_list
        )

    # ['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Objective-C', 'Swift', 'Matlab', 'Kotlin', 'Go', 'Rust', 'Ruby', 'C/C++', 'C#']
    # [5652840, 5387788, 1544826, 7680111, 48748297, 297175, 1338706, 1230230, 422068, 488155, 46970659, 1259213, 3764969, 87305050, 78692273]

    @property
    def issue_amount_list(self):
        language_list = self._list_editor.change_for_usage('encode', 'github', self.language_list)
        issue_amount_list = []

        for language in language_list:
            request = get(f'https://github.com/search?l={language}&q={language}&type=Issues').text

            soup = str(Bs(request, 'lxml').find('body').find_all('h3')[-1]).translate(
                str.maketrans('<h3></h3>,issues \n', ' ' * len('<h3></h3>,issues \n'))
            )

            issue_amount_list.append(int(soup.replace(' ', '')))
            sleep(8)

        return (
            self._list_editor.change_for_usage('decode', 'github', language_list), issue_amount_list
        )

    # ['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Objective-C', 'Swift', 'Matlab', 'Kotlin', 'Go', 'Rust', 'Ruby', 'C/C++', 'C#']
    # [52101, 47072, 1288478, 2688859, 25571, 262941, 1945, 2550, 27290, 198497, 251298, 576679, 2887775, 1190650, 5728]

    @property
    def commit_amount_list(self):
        language_list = self._list_editor.change_for_usage('encode', 'github', self.language_list)
        commit_amount_list = []
        for language in language_list:
            request = get(f'https://github.com/search?l={language}&q={language}&type=commits').text

            soup = str(Bs(request, 'lxml').find('body').find_all('h3')[-1])

            start = soup.find('Showing') + 8
            finish = soup.find(' available')

            commit_amount_list.append(
                int(soup[start:finish].replace(',', ''))
            )

            sleep(8)

        return (
            self._list_editor.change_for_usage('decode', 'github', language_list), commit_amount_list
        )
    # ['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Objective-C', 'Swift', 'Matlab', 'Kotlin', 'Go', 'Rust', 'Ruby', 'C/C++', 'C#']
    # [1663241, 1440823, 715852, 536107, 203691, 246494, 17831, 192095, 65333, 156212, 413159, 144984, 289751, 276793, 200423]


class GraphPrinter:

    @staticmethod
    def print_pie_graph(title, language_list, amount_list):
        fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))
        wedges, texts = ax.pie(amount_list, wedgeprops=dict(width=0.5), startangle=40,
                               counterclock=True, )
        bbox_props = dict(fc='w', ec='k', lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(language_list[i], xy=(x, y), xytext=(1.5 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment, **kw)
        ax.set_title(title)
        plt.show()

    @staticmethod
    def print_bar_graph(title, color, property_list, amount_list):
        x = np.arange(len(amount_list))
        print(x, title)
        plt.figure(figsize=(15, 10))
        plt.xticks(x, property_list, rotation=45)
        bar = plt.bar(x, amount_list, color=color)
        plt.title(title)
        for rect in bar:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0, height, height, ha='center', va='bottom', size=12)
        plt.show()
