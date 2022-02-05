# Wordle-helper
Helper for wordle.

------------------------------------------------------------------------------
wordleguess.py 

Instructions: 
    Write a maximum of five letter word or part of word.
    Unknown characters can be written as "*" and program
    finds all the solutions which have character's in
    the desired place. There are also three commands.

        Examples of use: 
            1. User inputs "abo", and finds all the 
            solutions containing "abo". In this case 
            character position doesn't matter.
            2. User inputs "*abo*" which isn't match 
            with 'abode' but is a match with 'labor'. 
            This is because at index 0 there is
            "*" in user's input but solution 'adobe'
            has "a" at the index 0.

        List of commands:
            - info : instructions 
            - quit : exit program 
            - all : prints all of the solutions
            - random : prints 6 random solutions 
            - remove : removes desired characters
            - ignored : prints ignored characters
            - clear : clears all ignored characters
------------------------------------------------------------------------------

valid_solutions.csv is from: https://www.kaggle.com/bcruise/wordle-valid-words
