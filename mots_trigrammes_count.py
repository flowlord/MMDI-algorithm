# -*- coding: utf-8 -*-

import numpy as np
import codecs
import json


with open("settings.json", 'r') as file:
    data = json.load(file)

filepath = data["word_lst_pth"]

count = np.zeros((256, 256, 256), dtype='int32')
total_word_count = 0


with codecs.open(filepath, "r", "utf-8") as lines:
    for line in lines:
        i, j = 0, 0
        for k in [ord(c) for c in line.strip()]:
            count[i, j, k] += 1
            i, j = j, k
        total_word_count += 1


with open("total_word_count.txt", "w") as f:
    f.write(str(total_word_count-1))


count.tofile("count.bin")

print("Comptage des trigrammes terminé et sauvegardé dans 'count.bin'")
print(f"Nombre total de mots : {total_word_count}")

