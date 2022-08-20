"""
Script to get the best word to initiate the game

"""
#################################
# LIBRARIES IMPORT              #
#################################
import csv
import string


#################################
# GLOBAL VARIABLES              #
#################################

# Words to play length
word_length = 5


################################################################################
# METHOD TO COUNT EACH LETTER APPEARANCE IN ALL WORDS IN THE DICTIONARY        #
################################################################################
def letter_count(words_to_play, letters):
    # Initialize the letter dictionary in this method to complete with the information that would be obtain and after return
    letter_dictionary = {}

    # Each letter in letteres dictionary variable is processed
    for letter in letters:
        # Initialize the counter to 0
        counter = 0

        # The letter is compare with all words and get the number of coincidence
        for word in words_to_play:
            counter = counter + word.count(letter)

        # When finish include the result into the letter dictionary variable. The value is set to relative values
        letter_dictionary[letter] = counter / (word_length * len(words_to_play))

    return letter_dictionary

#######################################################
# METHOD TO CALCULATE THE QUALITY OF EACH WORD        #
#######################################################
def word_quality_calculation(word, letter_dictionary):

    # Initialize the quality value 
    quality = 0

    # For each word in potential_words calculate the total sum of his letters relative value calculated before
    for letter in word:
        quality = quality + letter_dictionary[letter]

    return quality
    


#################################
# MAIN METHOD                   #
#################################

# Import the csv with the words to play
with open("correct_spanish_words.csv", encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    words_to_play = [palabra[0] for palabra in list(reader)]

# Get in a list all letters
letters = list(string.ascii_lowercase)

# Because the library string is not a spanish library the letters list don't has the ñ character so we add it
letters.append("ñ")

# Get all letter count into a letter dictionary
letter_dictionary = letter_count(words_to_play, letters)

# Now get the possible words to win the prize of best word to set in first attempt
# Logical thinking give us that the best world would has 5 different letter so obtain this words into a variable
# The set command return the value introduced without repeat characters
potential_words = [word for word in words_to_play if len(set(word)) == word_length]

# In a tupla variable get each word with his quality value
potential_words_V2 = [(word, word_quality_calculation(word, letter_dictionary)) for word in potential_words]

# Sort the potential_words_V2 list
potential_words_V2.sort(key=lambda x:x[1], reverse = True)

# The best word is the first listed in potential_words_V2
print(f"The best word to set into the first attempt is {potential_words_V2[0][0]}")
