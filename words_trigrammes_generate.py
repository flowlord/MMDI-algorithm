# -*- coding: utf-8 -*-

"""
Word Generator: Generates words based on trigram probabilities with weighted length distribution.
"""

import numpy as np
from numpy.random import choice
import json
import os
from random import shuffle
from uuid import uuid4
from random import randint

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

def gen_weigthed_length(MIN_LENGTH, MAX_LENGTH):
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
    """Generate words based on trigram probabilities."""
    output_file = os.path.join(OUTPUT_DIR, f"{uuid4().hex[:4]}.txt")

    # Load word list and trigram probabilities
    word_set = set()
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        for line in file:
            word_set.add(line.strip())

    count = np.fromfile("count.bin", dtype="int32").reshape((256, 256, 256))

    # Compute probabilities
    sum_counts = count.sum(axis=2, keepdims=True)
    sum_counts[sum_counts == 0] = 1  # Avoid division by zero by setting zero sums to 1 temporarily

    probabilities = count / sum_counts
    probabilities[np.isnan(probabilities)] = 0  # Replace NaNs with 0

    # Ensure that rows with no data are replaced with uniform probabilities
    for i in range(256):
        for j in range(256):
            if not np.isclose(probabilities[i, j, :].sum(), 1.0):
                probabilities[i, j, :] = 1.0 / 256

    # Generate words
    with open("total_word_count.txt", "r", encoding="utf-8") as file:
        target_word_count = int(file.read().strip())-1

    generated_count = 0

    with open(output_file, "w", encoding="utf-8") as file:
        while generated_count < target_word_count:
            i, j = 0, 0
            word = ""
            word_length = choice(gen_weigthed_length(MIN_LENGTH, MAX_LENGTH))

            while True:
                k = choice(range(256), p=probabilities[i, j, :])
                if k == 10 or len(word) >= word_length:
                    break
                word += chr(k)
                i, j = j, k

            if word and word not in word_set and MIN_LENGTH <= len(word) <= MAX_LENGTH:
                file.write(word + "\n")
                generated_count += 1
                print(f"Generated word: {word}")

    print(f"Words saved to {output_file}")



if __name__ == "__main__":
    generate_words()




