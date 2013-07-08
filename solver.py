#!/usr/bin/python3
import re
from constants import *
from operator import attrgetter

class Word:
    def __init__(self, word, score, path):
        self.word = word
        self.score = score
        self.path = path

    def __str__(self):
        return '{0}: {1}'.format(self.word, self.score)

def valid(line):
    board_patt = '([a-z][/?]{0,2}){' + str(BOARD_SIZE) + '}$'
    if not re.match(board_patt, line):
        return False
    else:
        return True

# expects a valid, stripped board
def solve(line):
    letter_patt = r'([a-z])([/?]{0,2})'
    split = re.findall(letter_patt, line)
    # compute multipliers
    # clever scheme:
    # 0 = nothing
    # 1 = double word
    # 2 = triple word
    # 3 = double letter
    # 6 = triple letter
    mults = [ { '/': 3,
                '//': 6,
                '?': 1,
                '??': 2,
                '': 0,
                }[x[1]] for x in split ]
    board = [ x[0] for x in split ]
    # with q expanded to qu
    board_ = [ x[0] if x[0] is not 'q' else 'qu' for x in split]
    
    def get_word(path):
        word = []
        for pos in path:
            word.append(board_[pos])
        return ''.join(word)
    def get_score(path):
        score = 0
        dw, tw = False, False
        for i in path:
            score += LETTER_VALS[ord(board[i]) - 97] * (mults[i] // 3 + 1)
            if mults[i] == 1:
                dw = True
            elif mults[i] == 2:
                tw = True

        # 2 letter words have score 1
        if len(path) == 2:
            score = 1

        # word multipliers
        if tw:
            score *= 3
        elif dw:
            score *= 2

        # length bonus
        score += LENGTH_BONUS[len(path)]

        return score

    # recursive function
    def find_paths(word, visited, can_go, path, level):
        if len(word) == level:
            return [Word(get_word(path), get_score(path), path)]

        words = []
        for i in range(BOARD_SIZE):
            if board[i] == word[level] and can_go[i] and not visited[i]:
                visited_ = list(visited)
                visited_[i] = True
                path[level] = i
                can_go_ = [False] * BOARD_SIZE
                irow = i//BOARD_DIMENSION
                icol = i%BOARD_DIMENSION
                for j in range(BOARD_SIZE):
                    if -1 <= j//BOARD_DIMENSION - irow <= 1 and -1 <= j%BOARD_DIMENSION - icol <= 1:
                        can_go_[j] = True
                words.extend(find_paths(word, visited_, can_go_, path, level + 1))

        return words

    found = []
    for word in WORDS:
        words = find_paths(word, [False] * BOARD_SIZE, [True] * BOARD_SIZE, [''] * len(word), 0)
        if len(words) != 0:
            found.append(max(words, key=attrgetter('score')))

    found.sort(key=attrgetter('word'))
    found.sort(key=attrgetter('score'), reverse=True)

    return found
