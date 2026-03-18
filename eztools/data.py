from string import digits, ascii_lowercase, ascii_uppercase, ascii_letters
from secrets import randbelow
import random

SPEC_CHARS = ["@", "!", "#", "$", "%", "^", "&", "*", "_", "+", "=", "-", "?", "/", "~", ",", ".", ";", ":", "№"]
CHARS = digits+ascii_lowercase+ascii_uppercase+"".join(SPEC_CHARS)
LETTERS = ascii_letters
del ascii_letters, ascii_lowercase, ascii_uppercase, digits
VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
NUMERATE_LETTERS = {i+1: let for i, let in enumerate(LETTERS)}

def instr(*patterns: str, strings: list | tuple):
    return any(pat in strings for pat in patterns)

def confuse(text: str):
    lst = list(text)
    randomly = randbelow(10**18)
    random.seed(randomly)
    n = len(lst)
    for i in range(n):
        pos = random.randint(0, n - 1)
        lst[i], lst[pos] = lst[pos], lst[i]
    return "".join(lst), randomly

def deconfuse(text: str, key: int):
    lst = list(text)
    random.seed(key)
    n = len(lst)
    moves = []
    for i in range(n):
        moves.append((i, random.randint(0, n - 1)))
    for i, pos in reversed(moves):
        lst[i], lst[pos] = lst[pos], lst[i]
    return "".join(lst)

def reverse_dict(dictionary: dict):
    return {val: key for key, val in dictionary.items()}
