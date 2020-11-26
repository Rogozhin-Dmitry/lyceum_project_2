"""
класс обработки событий иреакции на них
last update: 26.11.2020 10:35
author: Рогожин Дмитрий
"""


class Check:
    def __init__(self, run, keys):
        self.keys = keys
        self.run = run

    def check_funk(self, events):
        for i in events:
            if i.type == 12:
                self.run[0] = False
            elif i.type == 2:
                self.keys[i.key] = True
            elif i.type == 3:
                self.keys[i.key] = False
