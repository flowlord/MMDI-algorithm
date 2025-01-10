# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import choice as num_choice
import codecs
from random import randint, choice
import json
import os
from uuid import uuid4

# Ensure output directory exists
OUTPUT_DIR = "m_keys"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Load settings
SETTINGS_PATH = "settings.json"
with open(SETTINGS_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)

MIN_LENGTH = data["MIN_LENGTH"]
MAX_LENGTH = data["MAX_LENGTH"]
FILE_PATH = data["word_lst_pth"]


def gen_weigthed_length():
    LENGTH_WEIGHTS = {}

    F = MAX_LENGTH

    for e in range(MIN_LENGTH, MAX_LENGTH):
        LENGTH_WEIGHTS[e] = randint(MIN_LENGTH, F)
        F = F - 1
    
    LENGTH_DISTRIBUTION = []
    for length, weight in LENGTH_WEIGHTS.items():
        LENGTH_DISTRIBUTION.extend([length] * weight)
    
    return LENGTH_DISTRIBUTION


def generate_words():
    word_list = open(FILE_PATH, "r", encoding="utf-8").read().splitlines()
    
    count = np.fromfile("count.bin", dtype="int32").reshape((256, 256, 256))
    s = count.sum(axis=2)

    s[s == 0] = 1
    p = count / s[:, :, None]
    p[np.isnan(p)] = 0

    for i in range(256):
        for j in range(256):
            if not np.isclose(p[i, j, :].sum(), 1.0):
                p[i, j, :] = 1.0 / 256
    
    outfile = os.path.join(OUTPUT_DIR, f"{uuid4().hex[:4]}.txt")

    with codecs.open(outfile, "w", "utf-8") as f:
        target_length = len(word_list)

        total_generated = 0

        lst = []

        while total_generated < target_length:
            i, j = 0, 0
            word = ""
            TGT  =  choice(gen_weigthed_length())

            while True:
                k = num_choice(range(256), p=p[i, j, :])
                if k == 10:
                    break
                word += chr(k)
                if len(word) == TGT:
                    break
                i, j = j, k
            if word and word not in lst:
                if word not in word_list:
                    f.write(word + "\n")
                    lst = lst + [word]
                    total_generated += 1
                    print(f"generated word : {word}")

for e in range(100):
    generate_words()


