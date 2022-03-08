# -*- encoding:utf-8 -*-

import re
import ast

class Persian():
    def __init__(self):
        pass

    def _multiple_replace(self, mapping, text):
        pattern = "|".join(map(re.escape, mapping.keys()))
        return re.sub(pattern, lambda m: mapping[m.group()], str(text))
    
    def convert(self, text):
        mapping = {
            '۰': '0',
            '۱': '1',
            '۲': '2',
            '۳': '3',
            '۴': '4',
            '۵': '5',
            '۶': '6',
            '۷': '7',
            '۸': '8',
            '۹': '9',
            '.': '.',
        }

        return self._multiple_replace(mapping, text)