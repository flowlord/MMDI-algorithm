# -*- coding: utf-8 -*-

"""
MMDI
"""

import json

settings_pth = "settings.json"

with open(settings_pth, 'r') as file:
    data = json.load(file)

MIN_LENGTH = data["MIN_LENGTH"]

MAX_LENGTH = data["MAX_LENGTH"]

word_lst = open("word_lst.txt", "r", encoding="utf-8").read().split("\n")

mmdi_dickey = open("m_keys/ff2a.txt", "r", encoding="utf-8").read().split("\n")


def cipher(text, word_lst):
    text = text.lower()
    cipher_text = ""

    words = text.split(" ")

    dict_key = {word_lst[i]: mmdi_dickey[i] for i in range(len(word_lst))}

    for word in words:
        if word in dict_key:
            cipher_text += dict_key[word] + " "
        else:
            cipher_text += word + " "

    return cipher_text


def decipher(text, word_lst):
    cipher_text = ""

    words = text.split(" ")

    dict_key = {mmdi_dickey[i]: word_lst[i] for i in range(len(mmdi_dickey))}

    for word in words:
        if word in dict_key:
            cipher_text += dict_key[word] + " "
        else:
            cipher_text += word + " "

    return cipher_text


# test -------------------------------------------------

msg = "bonjour tous le monde je dit que je suis une phrase de test"
print(msg,"\n")

encrypted_text = cipher(msg, word_lst)

print(encrypted_text, "\n")

print(decipher(encrypted_text, word_lst))


# 12/12/24: Test passed. Encrypt and decrypt functions work correctly.

# ---------------------------------


