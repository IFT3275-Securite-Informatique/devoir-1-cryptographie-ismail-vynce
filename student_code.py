# Devoir 1 - Question 2
# Vyncent Larose  - 20189960
# Ismail El Azhari - 20196185

import random as rnd
import numpy as np
import requests
from collections import Counter

# Fonction pour déchiffrer C avec une clé K
# Si K est la bonne, le message retourné devrait être bon, cependant, on utilise
# cette fonction avec des clés potentielles qui ne sont pas nécessairement
# adéquates
def dechiffrer(C, K):
    # Dictionnaire inverse
    K_inv = {v: k for k, v in K.items()}

    # Message chiffré divisé en segments de 8 bits
    decoded_text = []
    for i in range(0, len(C), 8):
        segment = C[i:i+8]

        # Vérifier si le segment binaire est dans le dictionnaire inverse
        if segment in K_inv:
            decoded_text.append(K_inv[segment])
        else:
            # Si le segment n'est pas trouvé:
            decoded_text.append(' ERROR ')

    return ''.join(decoded_text)

# Fonction qui permet de compter le nombre de fois que chaque symbole de la
# liste symboles se retrouve dans texte
def count_symbols(texte, symboles):
    occurrences = {symbole: 0 for symbole in symboles}
    i = 0

    while i < len(texte):
        # Bi-caractère?
        if i + 1 < len(texte) and texte[i:i+2] in symboles:
            bi = texte[i:i+2]
            occurrences[bi] += 1
            i += 2
        # Uni-caractère
        elif texte[i] in symboles:
            occurrences[texte[i]] += 1
            i += 1
        # Caractère non trouvé
        else:
            i += 1

    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)

# Génère tous les arrangements possibles de 8 bits
def generate_8bit_symbols():
    return [format(i, '08b') for i in range(256)]

# Crée un dictionnaire de symboles avec leur nombre de répétitions
def count_symbols_binary(texte_binaire):
    symboles_8bits = generate_8bit_symbols()
    occurrences = {symbole: 0 for symbole in symboles_8bits}

    i = 0
    while i < len(texte_binaire):
        # Bi-caractère
        if i + 15 < len(texte_binaire) and texte_binaire[i:i+16] in occurrences:
            bi = texte_binaire[i:i+16]
            occurrences[bi[:8]] += 1
            occurrences[bi[8:]] += 1
            i += 16
        # Uni-caractère
        elif i + 7 < len(texte_binaire) and texte_binaire[i:i+8] in occurrences:
            char = texte_binaire[i:i+8]
            occurrences[char] += 1
            i += 8
        # Caractère non trouvé
        else:
            i += 8

    occurrences_sorted = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)

    return occurrences_sorted


##### Pas utilisé avec la technique présenté dans ce code

# Load un dictionnaire francais à partir d'un fichier local afin de comparer les
# mots trouvés avec la clé potentielle. Ceci devrait servir afin d'obtenir un
# score qui déterminerait si la clé potentielle donne une message contenant de
# vrais mots francais

#from google.colab import files
#uploaded = files.upload()
#file_path = list(uploaded.keys())[0]

def load_french_dictionary(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        french_words = set(line.strip().lower() for line in f)

    # Add common symbols and digits to the set
    common_symbols = {" ", "\n", "\r", ".", ",", "!", "?", ":", ";", "'", '"', "-", "(", ")", "[", "]"}
    digits = {str(digit) for digit in range(10)}
    french_words.update(common_symbols)
    french_words.update(digits)

    return french_words

#french_words = load_french_dictionary(file_path)
#print(french_words)  # Display the set of French words

#####


# Permet de trouver une clé potentielle en égalisant les fréquences de chaque
# symbole du message chiffré avec celles du message de référence
def assign_key(ref, bin):
    potential_key = dict({})
    for i in range(len(ref)):
        potential_key[ref[i][0]] = bin[i][0]
    return potential_key

# Génération de plusieurs clés potentielles à partir de celle trouvé avec les
# fréquences. Ceci permet de donner des clés aléatoirement tout en apportant des
# changements qui font du sens. Les nouvelles clés restent proche de la première
# clé en termes de fréquences. Par exemple, dict tel que:

# {symbole: count}:
# {"e": 14000, "a": 10000, "s": 8500, "tt": 8200, " ": 8000, ...} et
# {symbole: binaire}:
# {"e": "00001111", "a": "11110000", "s": "10101010", "tt": "01010101", " ": "00110011", ...}
#pourrait devenir:
# {symbole: binaire}:
# {"e": "00001111", "a": "10101010", "s": "01010101", "tt": "11110000", " ": "00110011", ...}

# distance: échange de deux symbole à cette distance selon leur fréquence
# chance: pourcentage de chance que l'échange soit fait
# amount: nombre de clés générées
def generate_potential_keys(potential_key, distance, chance, amount):
    new_keys = []
    for i in range(amount):
        new_key = potential_key.copy()
        keys = list(new_key.keys())

        for i in range(len(keys) - distance):
            if rnd.random() < min(chance*i/100, chance):
                key1, key2 = keys[i], keys[i + distance]
                new_key[key1], new_key[key2] = new_key[key2], new_key[key1]
        new_keys.append(new_key)
    return new_keys


##### Fonctions fournies

def cut_string_into_pairs(text):
    pairs = []
    for i in range(0, len(text) - 1, 2):
        pairs.append(text[i:i + 2])
    if len(text) % 2 != 0:
        pairs.append(text[-1] + '_')  # Add a placeholder if the string has an odd number of characters
    return pairs

def load_text_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading the text: {e}")
        return None

#####


def decrypt(C):

    # Donnees necessaires venant de code fourni:
    # Utilisation d'un grand texte afin d'évaluer les fréquences des mots français
    url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
    text = load_text_from_web(url)
    url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"
    text = text + load_text_from_web(url)

    caracteres = list(set(list(text)))
    nb_caracteres = len(caracteres)
    nb_bicaracteres = 256-nb_caracteres
    bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
    symboles = caracteres + bicaracteres

    occurrences_bin = count_symbols_binary(C)
    occurrences_ref = count_symbols(text, symboles)

    potential_key = assign_key(occurrences_ref, occurrences_bin)
    text_decoded = dechiffrer(C, potential_key)

    # Exemple de génération de clés potentielles qui ne donnent pas de résultats
    # convaincants
    #potential_keys = generate_potential_keys(potential_key, 1, 0.1, 1)
    
    # Test désactivé afin de visualiser les résultats avec les clés
    #for i in range(len(potential_keys)):
    #M = dechiffrer(text_C, potential_keys[i])
    #print("With key", i+1, ":\n", M[10004:10090], "\n")

    return text_decoded
