# -*- coding: utf-8 -*-

"""
Trigram Counting Script: Reads words and counts trigram frequencies.
"""

import numpy as np
import json

# Load settings
SETTINGS_PATH = "settings.json"
with open(SETTINGS_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)

FILE_PATH = data["word_lst_pth"]

# Initialize trigram count array
count = np.zeros((256, 256, 256), dtype='int32')
total_word_count = 0

# Count trigrams
with open(FILE_PATH, "r", encoding="utf-8") as lines:
    for line in lines:
        i, j = 0, 0
        for k in (ord(c) for c in line.strip()):
            count[i, j, k] += 1
            i, j = j, k
        total_word_count += 1

# Save results
with open("total_word_count.txt", "w", encoding="utf-8") as file:
    file.write(str(total_word_count))

count.tofile("count.bin")

print("Trigram counting completed and saved to 'count.bin'.")
print(f"Total number of words: {total_word_count}")


