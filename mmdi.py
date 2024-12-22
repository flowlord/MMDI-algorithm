# -*- coding: utf-8 -*-
"""
MMDI: Cipher and Decipher Utility
"""

import json

# Load settings
SETTINGS_PATH = "settings.json"
with open(SETTINGS_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)

MIN_LENGTH = data["MIN_LENGTH"]
MAX_LENGTH = data["MAX_LENGTH"]

# Load word lists
WORD_LIST_PATH = data["word_lst_pth"]
KEY_LIST_PATH = data["key_lst_pth"]

word_list = open(WORD_LIST_PATH, "r", encoding="utf-8").read().splitlines()
key_list = open(KEY_LIST_PATH, "r", encoding="utf-8").read().splitlines()

def cipher(text, word_list, key_list):
    """Encrypt a given text using the word list and key list."""
    text = text.lower()
    cipher_dict = {word_list[i]: key_list[i] for i in range(len(word_list))}
    
    return " ".join(cipher_dict.get(word, word) for word in text.split(" "))

def decipher(text, word_list, key_list):
    """Decrypt a given text using the key list and word list."""
    decipher_dict = {key_list[i]: word_list[i] for i in range(len(key_list))}
    
    return " ".join(decipher_dict.get(word, word) for word in text.split(" "))

if __name__ == "__main__":
    # Test the functions
    message = "bonjour tous le monde je dit que je suis une phrase de test"
    print("Original Message:", message, "\n")

    encrypted_text = cipher(message, word_list, key_list)
    print("Encrypted Text:", encrypted_text, "\n")

    decrypted_text = decipher(encrypted_text, word_list, key_list)
    print("Decrypted Text:", decrypted_text)




