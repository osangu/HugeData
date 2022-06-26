import matplotlib.pyplot as plt
from requests import get

from emoji import emojize, demojize

from bs4 import BeautifulSoup as Bs

import re
from time import sleep


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

        return job_amount_list

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

        return repository_amount_list

    @property
    def issue_amount_list(self):
        language_list = self._list_editor.change_for_usage('encode', 'github', self.language_list)
        print(len(language_list), language_list)
        issue_amount_list = []
        for language in language_list:
            request = get(f'https://github.com/search?l={language}&q={language}&type=Issues').text

            soup = str(Bs(request, 'lxml').find('body').find_all('h3')[-1]).translate(
                str.maketrans('<h3></h3>,issues \n', ' ' * len('<h3></h3>,issues \n')))

            issue_amount_list.append(int(soup.replace(' ', '')))
            sleep(8)

        return issue_amount_list

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
                int(soup[start:finish].replace(',',''))
            )

            sleep(8)

        return commit_amount_list
