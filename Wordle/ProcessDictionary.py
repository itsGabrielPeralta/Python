"""
Script to process the csv document in order to get all words with the correct format
The words must be with valid character and with exactly length of 5

"""

# Import the libraries needed
import csv
import codecs
import pandas as pd

# Global variables
length_words = 5

# Open the spanish_words content
with open('spanish_words.csv', encoding='utf-8') as spanish_dictionary:
    # Read the csv content setting the element that separate the words
    reader = csv.reader(spanish_dictionary, delimiter=',')
    # Storage the data in a list variable. Because the accent mark some words in the csv file is broken so the data must be processed with decode criteria to translate correctly
    spanish_words = [codecs.decode(word, 'unicode_escape') for word in list(reader)[0]]

# Get the words with 5 letters
spanish_words_5 = [word for word in spanish_words if len(word) == length_words] 

# Eliminate the accent marks
# To replace the letters with accent marks for the same letter without the accent mark it's created two variables with the characters involved
initial_Character = "áéíóúü"
finish_Character = "aeiouu"

# str has a command that make the translation from a character to other
translation = str.maketrans(initial_Character, finish_Character)

# Bucle for to travel throw all words and make the translation
spanish_words_5_without_accent_marks = [word.translate(translation) for word in spanish_words_5]

# Some words without accent mark could be equal than other word in the list so this duplicates must be eliminated. For this works perfectly a set type object
# Defining a set variable the duplicate is eliminated automatically
spanish_words_5_set = set(spanish_words_5_without_accent_marks)

# Right after define a list from the previous set variable and then we get a list variable without duplicates
correct_spanish_words = list(spanish_words_5_set)

# Save the list with the correct words into a csv file
df = pd.DataFrame(correct_spanish_words)
df.to_csv("correct_spanish_words.csv", index=False, header=False, sep=";")