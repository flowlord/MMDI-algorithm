# -*- coding: utf-8 -*-

import numpy as np
import codecs
import json

# Load settings
SETTINGS_PATH = "settings.json"
with open(SETTINGS_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)

FILE_PATH = data["word_lst_pth"]

def generate_trigram_counts():
    count = np.zeros((256, 256, 256), dtype='int32')

    with codecs.open(FILE_PATH, "r", "utf-8") as lines:
        for line in lines:
            i, j = 0, 0
            for k in [ord(c) for c in line.strip()]:
                count[i, j, k] += 1
                i, j = j, k


    count.tofile("count.bin")


generate_trigram_counts()

