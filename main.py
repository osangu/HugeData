import matplotlib.pyplot as plt
from requests import get

from emoji import emojize

from bs4 import BeautifulSoup as Bs

import re
from time import sleep


def print_encode_warning(original, revision):
    print(emojize(f':red_exclamation_mark: {original} to {revision} for better result '))



class Scrawler:

    @property
    def material_list(self):
        _list = []
        request = get('https://pypl.github.io/PYPL.html')
        soup = Bs(request.content, 'lxml')
        data = str(soup.find('head').find('script')).split('<td>')

        for i in range(16):
            if i > 0:
                data[i] = str(data[i]).replace('</td>', ' ')
                _list.append(data[i].split()[0])

        return _list

    @staticmethod
    def get_job_amount_list(material_list: list):
        job_amount_list = []

        for material in material_list:
            for cnt in range(20):
                request = get(
                    f'https://www.wanted.co.kr/api/v4/jobs?1655641140814&country=kr&job_sort=company.response_rate_order&locations=all&years=-1&query={material}&limit=100&offset={100 * cnt}'
                ).json()

                amount = len(request['data'])

                if 100 > amount != 0:
                    job_amount_list.append(100 * cnt + amount)
                    break
        return job_amount_list

    @staticmethod
    def get_repository_amount_list(language_list):
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

    @staticmethod
    def get_issue_amount_list(language_list):
        issue_amount_list = []
        for language in language_list:
            request = get(f'https://github.com/search?l={language}&q={language}&type=Issues').text

            soup = str(Bs(request, 'lxml').find('body').find_all('h3')[-1]).translate(
                str.maketrans('<h3></h3>,issues \n', ' ' * len('<h3></h3>,issues \n')))

            issue_amount_list.append(int(soup.replace(' ', '')))
            sleep(8)

        return issue_amount_list

    @staticmethod
    def get_commits_amount_list(language):  # language_list):
        # for language in language_list:
        request = get(f'https://github.com/search?l={language}&q={language}&type=commits').text
        print(request)
        soup = str(Bs(request, 'lxml').find('body').find_all('h3'))
        print(soup)

        sleep(8)


class MaterialEditor:

    def __init__(self):
        self.__github_black = {
            'C#': 'C%23',
            'C/C++': 'C%2B%2B',
            'Objective-C': 'Swift'
        }
        self.__wanted_black = {
            'C#': 'C%23',
            'C/C++': 'C%2B%2B',
            'Kotlin': 'Android',
            'Swift': 'IOS',
            'Objective-C': 'IOS',
            'R': '데이터 분석'
        }
        self.__decode = {
            'C%23': 'C#',
            'C%2B%2B': 'C/C++',
            'Android': 'Kotlin',
            'IOS': 'Swift',
            '데이터 분석': 'Data Analysis'
        }
        self.__list_type = {
            'github': self.__github_black,
            'wanted': self.__wanted_black,
            'decode': self.__decode
        }

    def change_material_list(self, material_list: list, _type: str):
        change_instances = self.__list_type[_type]
        for i in change_instances:
            if i in material_list:
                material_list.remove(i)
                if change_instances[i] in material_list: continue
                material_list.append(change_instances[i])
                print_encode_warning(i, change_instances[i])
        return material_list


class GraphPrinter:

    @staticmethod
    def print_two_bar_graph(x_list, y_list, title):
        plt.title(title)
        plt.xticks(rotation=45, size=7)
        plt.bar(x_list, y_list)
        for i in range(1, len(x_list) + 1):
            plt.text(i - 1, y_list[i - 1], y_list[i - 1], ha="center")
        plt.show()

    @staticmethod
    def print_three_bar_graph(github_list, title):
        plt.title(title)
        plt.xticks(size=10)
        plt.bar(['repository', 'issue', 'commits'], github_list, width=0.5)
        for i in range(1, 4):
            plt.text(i - 1, github_list[i - 1], github_list[i - 1], ha="center")
        plt.show()

    @staticmethod
    def print_pie_graph(name_list, amount_list, title):
        plt.title(title)
        plt.pie(amount_list, labels=name_list,counterclock=False)
        plt.show()

if __name__ == '__main__':
    a = MaterialEditor().change_material_list(['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Swift', 'Matlab', 'Kotlin', 'Go',
                     'Rust', 'Ruby', 'C%23', 'C%2B%2B'],'decode')
    commit_amt = [12607777, 9216606, 2150033, 12680602, 64773189, 612512, 2016807, 339736, 394051, 40797277, 977496,
                  3763702, 111008993, 116905408]
    issue_amt = [520006, 4719901, 128798, 26861, 255168, 2622579, 2514, 27246, 19720, 227800, 57454, 2884441, 572560, 11881]
    repo_amt =[1595300, 1424433, 712372, 534982, 195602, 244981, 191716, 65242, 155649, 411925, 144407, 289514, 199930, 276201]
    import matplotlib.pyplot as plt
    from requests import get

    from emoji import emojize

    from bs4 import BeautifulSoup as Bs

    import re
    from time import sleep


    def print_encode_warning(original, revision):
        print(emojize(f':red_exclamation_mark: {original} to {revision} for better result '))


    class Scrawler:

        @property
        def material_list(self):
            _list = []
            request = get('https://pypl.github.io/PYPL.html')
            soup = Bs(request.content, 'lxml')
            data = str(soup.find('head').find('script')).split('<td>')

            for i in range(16):
                if i > 0:
                    data[i] = str(data[i]).replace('</td>', ' ')
                    _list.append(data[i].split()[0])

            return _list

        @staticmethod
        def get_job_amount_list(material_list: list):
            job_amount_list = []

            for material in material_list:
                for cnt in range(20):
                    request = get(
                        f'https://www.wanted.co.kr/api/v4/jobs?1655641140814&country=kr&job_sort=company.response_rate_order&locations=all&years=-1&query={material}&limit=100&offset={100 * cnt}'
                    ).json()

                    amount = len(request['data'])

                    if 100 > amount != 0:
                        job_amount_list.append(100 * cnt + amount)
                        break
            return job_amount_list

        @staticmethod
        def get_repository_amount_list(language_list):
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

        @staticmethod
        def get_issue_amount_list(language_list):
            issue_amount_list = []
            for language in language_list:
                request = get(f'https://github.com/search?l={language}&q={language}&type=Issues').text

                soup = str(Bs(request, 'lxml').find('body').find_all('h3')[-1]).translate(
                    str.maketrans('<h3></h3>,issues \n', ' ' * len('<h3></h3>,issues \n')))

                issue_amount_list.append(int(soup.replace(' ', '')))
                sleep(8)

            return issue_amount_list

        @staticmethod
        def get_commits_amount_list(language):  # language_list):
            # for language in language_list:
            request = get(f'https://github.com/search?l={language}&q={language}&type=commits').text
            print(request)
            soup = str(Bs(request, 'lxml').find('body').find_all('h3'))
            print(soup)

            sleep(8)


    class MaterialEditor:

        def __init__(self):
            self.__github_black = {
                'C#': 'C%23',
                'C/C++': 'C%2B%2B',
                'Objective-C': 'Swift'
            }
            self.__wanted_black = {
                'C#': 'C%23',
                'C/C++': 'C%2B%2B',
                'Kotlin': 'Android',
                'Swift': 'IOS',
                'Objective-C': 'IOS',
                'R': '데이터 분석'
            }
            self.__decode = {
                'C%23': 'C#',
                'C%2B%2B': 'C/C++',
                'Android': 'Kotlin',
                'IOS': 'Swift',
                '데이터 분석': 'Data Analysis'
            }
            self.__list_type = {
                'github': self.__github_black,
                'wanted': self.__wanted_black,
                'decode': self.__decode
            }

        def change_material_list(self, material_list: list, _type: str):
            change_instances = self.__list_type[_type]
            for i in change_instances:
                if i in material_list:
                    material_list.remove(i)
                    if change_instances[i] in material_list: continue
                    material_list.append(change_instances[i])
                    print_encode_warning(i, change_instances[i])
            return material_list


    class GraphPrinter:

        @staticmethod
        def print_two_bar_graph(x_list, y_list, title):
            plt.title(title)
            plt.xticks(rotation=45, size=7)
            plt.bar(x_list, y_list)
            for i in range(1, len(x_list) + 1):
                plt.text(i - 1, y_list[i - 1], y_list[i - 1], ha="center")
            plt.show()

        @staticmethod
        def print_three_bar_graph(github_list, title):
            plt.title(title)
            plt.xticks(size=10)
            plt.bar(['repository', 'issue', 'commits'], github_list, width=0.5)
            for i in range(1, 4):
                plt.text(i - 1, github_list[i - 1], github_list[i - 1], ha="center")
            plt.show()

        @staticmethod
        def print_pie_graph(name_list, amount_list, title):
            plt.title(title)
            plt.pie(amount_list, labels=name_list, counterclock=False)
            plt.show()


    if __name__ == '__main__':
        a = MaterialEditor().change_material_list(
            ['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Swift', 'Matlab', 'Kotlin', 'Go',
             'Rust', 'Ruby', 'C%23', 'C%2B%2B'], 'decode')
        commit_amt = [12607777, 9216606, 2150033, 12680602, 64773189, 612512, 2016807, 339736, 394051, 40797277, 977496,
                      3763702, 111008993, 116905408]
        issue_amt = [520006, 4719901, 128798, 26861, 255168, 2622579, 2514, 27246, 19720, 227800, 57454, 2884441,
                     572560, 11881]
        repo_amt = [1595300, 1424433, 712372, 534982, 195602, 244981, 191716, 65242, 155649, 411925, 144407, 289514,
                    199930, 276201]

        print(repo_amt)
    print(repo_amt)