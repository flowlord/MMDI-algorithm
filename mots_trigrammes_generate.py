# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import choice
import codecs
from uuid import uuid4
from random import shuffle
import json
import os

if not os.path.exists("m_keys/"):
    os.makedirs("m_keys/")

with open("settings.json", 'r') as file:
    data = json.load(file)

MIN_LENGTH = data["MIN_LENGTH"]

MAX_LENGTH = data["MAX_LENGTH"]

filepath = data["word_lst_pth"]

def gen_words():

    outfile = f"m_keys/{str(uuid4())[0:4]}.txt"
    dico = set()
    with codecs.open(filepath, "r", "utf-8") as lines:
        for line in lines:
            dico.add(line.strip())

    count = np.fromfile("count.bin", dtype="int32").reshape((256, 256, 256))
    s = count.sum(axis=2)
    s[s == 0] = 1
    p = count / s[:, :, None]
    p[np.isnan(p)] = 0

    for i in range(256):
        for j in range(256):
            if not np.isclose(p[i, j, :].sum(), 1.0):
                p[i, j, :] = 1.0 / 256

    with open("total_word_count.txt", "r") as f:
        target_length = int(f.read().strip())

    with codecs.open(outfile, "w", "utf-8") as f:
        total_generated = 0
        TGT = MIN_LENGTH
        while total_generated < target_length:
            i, j = 0, 0
            word = ""
            while True:
                k = choice(range(256), p=p[i, j, :])
                if k == 10:
                    break
                word += chr(k)
                if len(word) == TGT:
                    break
                i, j = j, k
            if word and word not in dico:
                f.write(word + "\n")
                total_generated += 1
                print(f"Mot généré : {word}")
            if total_generated % 5000 == 0:
                TGT = min(TGT + 1, MAX_LENGTH)
    
    of = open(outfile, "r", encoding="utf-8").read().split("\n")

    shuffle(of)

    nf = open(outfile, "w", encoding="utf-8")

    for e in of:
        nf.write(e+"\n")
    
    nf.close()


def gen_many_x(n):
    for i in range(n):
        gen_words()
        print(i)


#gen_words()
