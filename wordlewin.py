# The MIT License (MIT)
#
# Copyright (c) 2022 Scott Means
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Thanks to:
#   * John Lawler for the word list (http://www-personal.umich.edu/~jlawler/wordlist.html)
#   * Wikipedia for the letter frequency table (https://en.wikipedia.org/wiki/Letter_frequency)

# calculate good word combos to start Wordle games with

import re
from collections import namedtuple

char_freq = {
    "a": 8.20,
    "b": 1.50,
    "c": 2.80,
    "d": 4.30,
    "e": 13.0,
    "f": 2.20,
    "g": 2.0,
    "h": 6.10,
    "i": 7.0,
    "j": 0.15,
    "k": 0.77,
    "l": 4.0,
    "m": 2.50,
    "n": 6.70,
    "o": 7.50,
    "p": 1.90,
    "q": 0.10,
    "r": 6.0,
    "s": 6.30,
    "t": 9.10,
    "u": 2.80,
    "v": 0.98,
    "w": 2.40,
    "x": 0.15,
    "y": 2.0,
    "z": 0.07
}

# first, find candidate words
word_test = re.compile(r'^[a-z]{5}$')

words = []
with open('wordlist.txt') as f:
    for row in f:
        row = row.strip()
        chars = set([*row])

        if word_test.match(row) and len(chars) == 5:
            words.append(row)

# next, sort them by letter frequency totals
def score_word(word):
    return sum([char_freq[ch] for ch in word])
words.sort(key=score_word)

# now find letter-unique combos
Combo = namedtuple('Combo', ['letters', 'words'])

combos = []
for word in words:
    letters = set([*word])

    for combo in combos:
        if len(combo.letters | letters) == ((len(combo.words)+1)*len(word)):
            combo.letters.update(letters)
            combo.words.append(word)

    combos.append(Combo(letters, [word]))

combos.sort(key=lambda combo: len(combo.words), reverse=True)
print('\n'.join([', '.join(combo.words) for combo in combos if len(combo.words) >= 3]))
