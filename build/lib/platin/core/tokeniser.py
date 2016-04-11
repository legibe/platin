#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import os
from config import Config


class Tokeniser(object):
    escape = {
        '\\"': '"',
        #'\\,':  ',',
        '\\:': ':',
        '\\\\': '\\',
        '\\n': '\n',
        '\\r': '\r',
        '\\t': 't',
    }

    def __init__(self, which='classic'):
        config = Config.read(os.path.join(os.path.dirname(__file__), 'tokenizer_config_%s.json' % which))
        self._keep = set(config['keep'])
        self._separators = set(config['drop']).union(self._keep)

    def tokenise_split(self, buffer, split):
        return self._tokenise(self.unescape(buffer), split, self._keep, True)

    def tokenise(self, buffer):
        return self._tokenise(self.unescape(buffer), self._separators, self._keep, False)

    def _tokenise(self, buffer, separators, keep, split):
        tokens = []
        maxIndex = len(buffer) - 1
        index = 0
        start = 0
        word = False
        while index <= maxIndex:
            currentChar = buffer[index]
            if currentChar == "\\":
                current = index + 1
                while current <= maxIndex and buffer[current - 1] == "\\":
                    current += 1
                if not split:
                    word = False
                    tokens.append(buffer[start:index])
                    if buffer[current - 1] in keep:
                        tokens.append(buffer[current - 1])
                        start = current
                        index = current
                    else:
                        tokens.append('\\')
                        start = current - 1
                        index = current + 1
                else:
                    word = True
                    index = current
            elif currentChar in separators:
                if word:
                    tokens.append(buffer[start:index])
                if currentChar in keep and not split:
                    tokens.append(currentChar)
                start = index + 1
                index += 1
                word = False
            else:
                word = True
                index += 1
        if index > start:
            tokens.append(buffer[start:index])
        return tokens

    @classmethod
    def unescape(self, argument):
        for sequence, replacement in self.escape.items():
            argument = argument.replace(sequence, replacement)
        return argument

