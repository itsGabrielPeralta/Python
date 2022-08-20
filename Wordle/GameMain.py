"""
Script to design the game main logic

"""
#################################
# LIBRARIES IMPORT              #
#################################
import csv
import random



#################################
# GLOBAL VARIABLES              #
#################################
n_attempt = 6 # Maximun number of attemps
word_introduced_length = 5 # Length of word introduced to play

class COLOR():
    GREY = 0    # letter is not in key word
    ORANGE = 1  # letter is in key word but not in this position
    GREEN = 2   # letter is in key word and right in this position

#################################
# FUNCTION TO INITIATE THE GAME
#################################
def init_game(words_to_play):

    print("")
    print("|-------------------------|")
    print("| INITIATING CHEAP WORDLE |")
    print("|-------------------------|")
    print(f"A dictionary with {len(words_to_play)} has been loaded")

    # Get a word radomly to discover
    word_to_discover = random.choice(words_to_play)

    # Define a variable with the first attempt
    attempt = 1

    # Define the bucle while that finish when the attempt variable reach to the maximun attemps number
    while attempt <= n_attempt:

        # Get the word from an input
        word_introduced = str(input(f"Attemp {attempt}: "))

        # Check if the word introduced is correct. Ask a word while the word introduced is not valid
        while valid_word_introduced(word_introduced, words_to_play) == False:
            word_introduced = str(input(f"Attemp {attempt}: "))

        # Check if the word introduced is equal to the word to discover
        if(word_introduced == word_to_discover):
            print("")
            print(f"Congratulations. You discover the word {word_to_discover} in attemp {attempt}")
            break
        else:
            # Compare the introduced word with the word to discover
            #compare_words(word_introduced, word_to_discover)
            filter_word = filter_calculate(word_introduced, word_to_discover)

            # Show filter
            print(filter_word)

            # Add a new attempt
            attempt += 1

    # If all attempt is wasted show the message to inform
    if(attempt > n_attempt):
        print(f"All attemps completed without discover the word {word_to_discover}")
        
#############################################################################
# FUNCTION TO CHECK IF THE WORD INTRODUCED IS VALID
#############################################################################
def valid_word_introduced(word, words_list):

    # Check the length of word introduced
    if len(word) != word_introduced_length:
        print(f"The word introduced must has {word_introduced_length} characters")
        return False

    # Check if the word is in the dictionary
    if  word not in words_list:
        print("The word is not contained into dictionary")
        return False

    # If word is ok return True
    return True

##########################################################################################
# FUNCTION TO SET THE FILTER VALUES COMPARING THE KEY WORD WITH THE INTRODUCED WORD
##########################################################################################
def filter_calculate(word, key_word):

    # Initialize the filter
    filter = [-1,-1,-1,-1,-1]

    # Initialize a empty array to storage the duplicate letter and not process again
    proccessed_letter = []

    # Bucle for apply to word variable related with the appropiate index
    for idx, letter in enumerate(word):
        # Define aux word that we need when the word introduced has duplicate letters
        aux_word = word

        # Check if the letter are in the processed letter list to avoid a new processing
        if letter in proccessed_letter:
            continue

        # Because of the word can has the same letter more than once, it's processed in different ways
        if(word.count(letter) == 1):
            filter[idx] = process_no_duplicate_letter(letter, key_word, idx)
        else:
            filter = process_duplicate_letter(letter, word, key_word, aux_word, filter)

    return filter



##########################################################################################
# FUNCTION TO PROCESS THE UNIQUE LETTERS
##########################################################################################
def process_no_duplicate_letter(letter, key_word, idx):
    if letter not in key_word:
        return COLOR.GREY
    elif letter == key_word[idx]:
        return COLOR.GREEN
    else:
        return COLOR.ORANGE



##########################################################################################
# FUNCTION TO PROCESS THE DUPLICATE LETTERS
##########################################################################################
def process_duplicate_letter(letter, word, key_word, aux_word, filter):

    # First of all get the indixes in introduced word where the letter are colocated
    indexes = [i for i, l in enumerate(word) if l == letter]
    # Get the indixes in key word where the letter are colocated
    indexes_key_word = [i for i, l in enumerate(key_word) if l == letter]

    # Process the indixes variable to compare with indixes_key_word. If there are an index coincidence eliminate the letter in aux_word
    for index in indexes:
        if key_word[index] == letter:
            aux_word = aux_word[:index] + "-" + aux_word[index+1:]
            indexes.remove(index)
            filter[index] = COLOR.GREEN
        else:
            pass

    # Now process the other letters that are the same in introduced word
    for index in indexes:
        if letter in aux_word:
            filter[index] = COLOR.ORANGE
            aux_word = aux_word[:indexes_key_word[0]] + "-" + aux_word[indexes_key_word[0]+1:]
            indexes_key_word.remove(indexes_key_word[0])
        else:
            filter[index] = COLOR.GREY

    return filter




#################################
# MAIN METHOD                   #
#################################

# Import the csv with the words to play
with open("correct_spanish_words.csv", encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    words_to_play = [palabra[0] for palabra in list(reader)]

    init_game(words_to_play)



