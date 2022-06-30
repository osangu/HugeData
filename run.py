from main import LanguageListEditor, Scrawler, GraphPrinter


class CommandCenter:

    def __init__(self):
        self._scr = Scrawler(
            LanguageListEditor()
        )
        self._graph_printer = GraphPrinter()

    def show_language_vs_job_amount_list_as_pie(self):
        language_list, job_amount_list = self._scr.job_amount_list

        title = f'Job amount for each language - TOTAL AMT :: {sum(job_amount_list)}'
        language_list = [str(job_amount_list[ind]) + ' ' + val for ind, val in enumerate(language_list)]

        self._graph_printer.print_pie_graph(title, language_list, job_amount_list)

    def show_language_vs_job_amount_list_as_bar(self):

        language_list, job_amount_list = self._scr.job_amount_list

        print(language_list, '\n', job_amount_list)

        title = f'Job amount for each language - TOTAL AMT :: {sum(job_amount_list)}'

        self._graph_printer.print_bar_graph(title,'pink', language_list, job_amount_list)

    def show_repository_issue_commit_as_bar(self):
        self._github_language_list = ['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Objective-C', 'Swift', 'Matlab', 'Kotlin', 'Go', 'Rust', 'Ruby', 'C/C++', 'C#']
        self._issue_amt_list = [52101, 47072, 1288478, 2688859, 25571, 262941, 1945, 2550, 27290, 198497, 251298, 576679, 2887775, 1190650, 5728]
        self._commit_amt_list = [1663241, 1440823, 715852, 536107, 203691, 246494, 17831, 192095, 65333, 156212, 413159, 144984, 289751, 276793, 200423]
        self._repo_amt_list = [5652840, 5387788, 1544826, 7680111, 48748297, 297175, 1338706, 1230230, 422068, 488155, 46970659, 1259213, 3764969, 87305050, 78692273]

        for ind, val in enumerate(self._github_language_list):
            self._graph_printer.print_bar_graph(
                val,
                'springgreen',
                [
                    'issue',
                    'commit',
                    'repository'
                ],
                [
                    self._issue_amt_list[ind],
                    self._commit_amt_list[ind],
                    self._repo_amt_list[ind]
                ]
            )

    def show_repository_total_as_bar(self):
        self._repo_amt_list = [5652840, 5387788, 1544826, 7680111, 48748297, 297175, 1338706, 1230230, 422068, 488155, 46970659, 1259213, 3764969, 87305050, 78692273]
        self._github_language_list = ['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Objective-C', 'Swift', 'Matlab', 'Kotlin', 'Go', 'Rust', 'Ruby', 'C/C++', 'C#']

        self._graph_printer.print_bar_graph('REPOSITORY','skyblue',self._github_language_list,self._repo_amt_list)

    def show_issue_total_as_bar(self):
        self._issue_amt_list = [52101, 47072, 1288478, 2688859, 25571, 262941, 1945, 2550, 27290, 198497, 251298, 576679, 2887775, 1190650, 5728]
        self._github_language_list = ['Python', 'Java', 'JavaScript', 'PHP', 'R', 'TypeScript', 'Objective-C', 'Swift', 'Matlab', 'Kotlin', 'Go', 'Rust', 'Ruby', 'C/C++', 'C#']

        self._graph_printer.print_bar_graph('a','skyblue',self._github_language_list, self._issue_amt_list)

if __name__ == '__main__':
    cc = CommandCenter()
#    cc.show_language_vs_job_amount_list_as_pie()
#    cc.show_language_vs_job_amount_list_as_bar()
#    cc.show_repository_issue_commit_as_bar()
    cc.show_repository_total_as_bar()