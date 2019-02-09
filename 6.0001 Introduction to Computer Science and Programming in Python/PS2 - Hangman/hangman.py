# Problem Set 2, hangman.py
# Name: Anthony Lem
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word_list = list(secret_word)
    copy_secret_word_list = secret_word_list[:]
    for letter in copy_secret_word_list:
        if letter in letters_guessed:
            secret_word_list.remove(letter)
        else:
            return False
    return True

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = ""
    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += "_ "
    return word

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    lowercase_letters = list(string.ascii_lowercase) #This returns a list of all lowercase letters
    copy_letters = lowercase_letters[:]
    for letter in letters_guessed:
        if letter in copy_letters:
            lowercase_letters.remove(letter)
    return "".join(lowercase_letters)

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings = 3
    guesses = 15
    vowels = "aeiou"
    letters_guessed = []

    print("Welcome to the game Hangman!\nFor every wrong guess that is a consonant, you lose one guess, and for every wrong guess that is a vowel, you lose two guesses.\nI am thinking of a word that is", len(secret_word), "letters long.")
    
    while guesses > 0:
        print("-------------")
        if get_guessed_word(secret_word, letters_guessed) == secret_word:
            break
        else:
            print("You have", guesses, "guesses left.\nAvailable letters:", get_available_letters(letters_guessed))
            letter = input("Please guess a letter: ")
            if letter in letters_guessed:
                warnings -= 1
                if warnings >= 0:
                    print("Oops! You've already guessed that letter. You now have", warnings, "warnings left.")
                    print(get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess.")
                    print(get_guessed_word(secret_word, letters_guessed))
                    guesses -= 1
            elif letter.isalpha() and len(letter) == 1:
                lower_case = letter.lower()
                letters_guessed += lower_case
                if lower_case in secret_word:
                    print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
                elif lower_case in vowels:
                    print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
                    guesses -= 2
                else:
                    print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
                    guesses -= 1
            else:
                warnings -= 1
                if warnings >= 0:
                    print("Oops! That is not a valid letter. You now have", warnings, "warnings left.")
                    print(get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! That is not a valid letter. You have no warnings left so you lose one guess.")
                    print(get_guessed_word(secret_word, letters_guessed))
                    guesses -= 1

    if get_guessed_word(secret_word, letters_guessed) == secret_word:
        unique_letters = []
        for letter in secret_word:
            if letter not in unique_letters:
                unique_letters += letter
        score = guesses * len(unique_letters)
        print("Congratulations, you won!\nYour total score for this game is:", score)
    else:
        print("-------------\nSorry, you ran out of guesses. The word was", secret_word)
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    stripped_word = my_word.replace(" ", "")
    if len(stripped_word) != len(other_word):
        return False
    else:
        for i in range(len(other_word)):
            if stripped_word[i] == "_" and other_word[i] in stripped_word:
                return False
            elif stripped_word[i] != "_" and stripped_word[i] != other_word[i]:
                return False
    return True          

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    list_of_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            list_of_matches.append(word)
    if len(list_of_matches) > 0:
        return " ".join(list_of_matches)
    else:
        return "No matches found"

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings = 3
    guesses = 15
    vowels = "aeiou"
    letters_guessed = []

    print("Welcome to the game Hangman!\nFor every wrong guess that is a consonant, you lose one guess, and for every wrong guess that is a vowel, you lose two guesses.\nI am thinking of a word that is", len(secret_word), "letters long.\nFor a list of all the words that might match your current guessed word, type in *.")
    
    while guesses > 0:
        print("-------------")
        if get_guessed_word(secret_word, letters_guessed) == secret_word:
            break
        else:
            print("You have", guesses, "guesses left.\nAvailable letters:", get_available_letters(letters_guessed))
            letter = input("Please guess a letter: ")
            if letter == "*":
                print("Possible word matches are:\n" + show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            elif letter in letters_guessed:
                warnings -= 1
                if warnings >= 0:
                    print("Oops! You've already guessed that letter. You now have", warnings, "warnings left.")
                    print(get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess.")
                    print(get_guessed_word(secret_word, letters_guessed))
                    guesses -= 1
            elif letter.isalpha() and len(letter) == 1:
                lower_case = letter.lower()
                letters_guessed += lower_case
                if lower_case in secret_word:
                    print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
                elif lower_case in vowels:
                    print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
                    guesses -= 2
                else:
                    print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
                    guesses -= 1
            else:
                warnings -= 1
                if warnings >= 0:
                    print("Oops! That is not a valid letter. You now have", warnings, "warnings left.")
                    print(get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! That is not a valid letter. You have no warnings left so you lose one guess.")
                    print(get_guessed_word(secret_word, letters_guessed))
                    guesses -= 1

    if get_guessed_word(secret_word, letters_guessed) == secret_word:
        unique_letters = []
        for letter in secret_word:
            if letter not in unique_letters:
                unique_letters += letter
        score = guesses * len(unique_letters)
        print("Congratulations, you won!\nYour total score for this game is:", score)
    else:
        print("-------------\nSorry, you ran out of guesses. The word was", secret_word)

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #secret_word = "christopher"
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
