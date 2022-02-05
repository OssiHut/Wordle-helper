'''
    Wordleguess.py
    
    Wordleguess program helps to find right solutions to
    Wordle game. Program contains basic CLI.

    Ossi Huttunen 2022
    ----------------------------------------------------
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


'''

from numpy import empty
import pandas as pd
import random

EMPTY = "*" # character for "empty" characters

df = pd.read_csv("valid_solutions.csv") # solutions dataframe
dfsize = df.size # checks size of dataframe

ignorecharacters = set() # set for ignored characters

def random_guesses():
    '''
        fetches six random solutions from dataset
    '''

    guesses = []
    i = 0
    while i < 6:
        index = random.randrange(0,dfsize)
        guesses.append(df.at[index,"word"])
        i+=1
    return guesses


def find_charpositions(userinput):
    '''
        finds and returns the positions of empty characters (*) in a list
    '''

    list = [] 

    for index, char in enumerate(userinput):
        if char == EMPTY:
            list.append(index)
    return list

def word_helper(userinput):
    '''
        Searches words which matching user input if input has
        empty characters ("*")
    '''

    ndf = df # copy of solutions dataframe
    charpositions = find_charpositions(userinput) # list for empty character positions
    if "*" in userinput:
        userinput = userinput.translate({ord("*"):None}) # remove "empty" characters
    ndf = df[df["word"].str.contains(userinput)] # dataframe for matching solutions
    wordlist = ndf.values.tolist() # dataframe listaksi
        
    userinputlist = [] # list for userinput's characters
    finalsplitlist = [] # list for solutions in splitted form
    solutionlist = [] # list for filtered solutions

    # splits userinput to characters
    for char in userinput:
        userinputlist.append(char)
        
    
    # splits solution words to characters and adds them to list
    splitlist = []
    for index in wordlist:
        for text in index:
            charlist = [] # list for individual word characters
            for char in text:
                charlist.append(char)
        splitlist.append(charlist)  


    # finds solutions that match with empty characters indexes
    for onelist in splitlist:
        chardict = {} # dict for solution's characters indexes

        # add solution's characters indexes to dict
        for ind, char in enumerate(onelist):
            chardict[ind]=char
            
        miss = 0 # counter for empty characters

        # iterate through chardict to find matching solutions
        for key, value in chardict.items():

            # Find unmatching solutions and ignore them:
            # Solution is unmatching if empty character 
            # index matches with solution's index. 
            # For example, userinput *abo* isn't match 
            # with abode but is with labor. This is because 
            # at index 0 userinput has "*" but solution
            # has "a".
            if key in charpositions:
                for inputchar in userinputlist:
                    if inputchar == value:
                        miss+=1
            
            # Remove solutions with ignored letters
            if value in ignorecharacters:
                miss+=1

        if miss == 0:
            finalsplitlist.append(onelist)


    # combine characters to words and add them to list
    for word in finalsplitlist:  
        solution = ""
        for charac in word:
            solution+=charac
        solutionlist.append(solution)
    return solutionlist

def filtered_print_all():
    ''''
        Returns list of filtered solutions. Solutions 
        are filtered by user's ignored characters.
    '''
    ndf = df # copy of solutions dataframe
    wordlist = ndf.values.tolist() # dataframe listaksi
        
    finalsplitlist = [] # list for solutions in splitted form
    solutionlist = [] # list for filtered solutions

    # splits solution words to characters and adds them to list
    splitlist = []
    for index in wordlist:
        for text in index:
            charlist = [] # list for individual word characters
            for char in text:
                charlist.append(char)
        splitlist.append(charlist)  


    # finds solutions that match with empty characters indexes
    for onelist in splitlist:
        chardict = {} # dict for solution's characters indexes

        # add solution's characters indexes to dict
        for ind, char in enumerate(onelist):
            chardict[ind]=char
            
        miss = 0 # counter for empty characters

        # iterate through chardict to find matching solutions
        for key, value in chardict.items():
            # Remove solutions with ignored letters
            if value in ignorecharacters:
                miss+=1

        if miss == 0:
            finalsplitlist.append(onelist)


    # combine characters to words and add them to list
    for word in finalsplitlist:  
        solution = ""
        for charac in word:
            solution+=charac
        solutionlist.append(solution)
    return solutionlist
        
def commands():
    '''
        CLI
        ----------------------------------------------------
        Possible userinput:
            - A word or part of the word
            - a maximum of five characters long word:
                - can contain empty ("*") characters (max 4)
            - A command: 
                - info : instructions
                - quit : exit program 
                - all : prints all of the solutions, filtered ignored
                - random : prints 6 random solutions
                - remove : removes desired characters
                - ignored : prints ignored characters
                - clear : clears all ignored characters
    '''
    
    while True:

        userinput = input(
            "\n--------------------------------------------------------------- \n" +
            "Give a word or part of the word (max 5 characters) or a command \n" +
            "Commands: \n" +
            "   - quit : exit program \n" +
            "   - info : instructions \n" +
            "   - all : prints all of the solutions, filtered ignored \n"
            "   - random : prints 6 random solutions \n"
            "   - remove : removes desired characters to ignore set \n"
            "   - ignored : prints ignored characters \n"
            "   - add : add ignored characters back \n"
            "   - clear : clears all ignored characters\n\n"
            "Write word here: "
        )

        if not userinput:
            print("Input can't be empty")

        elif not userinput.isalpha() and "*" not in userinput:
            print("Input must include only alphabetic characters.")

        # quit command: exit program
        elif userinput == "quit":
            print("Program has been succesfully ended.")
            break
        
        # all command: prints all of the solutions
        #  no solutions with ignored characters are printed
        elif userinput == "all":
            allsolutions = filtered_print_all()
            solutionamount = len(allsolutions)
            if len(ignorecharacters)!=0:
                print("Following characters are ignored in results: \n")
                print(*sorted(ignorecharacters),sep=", ")
                print("\n")
            
            print(f"Total of {solutionamount} solutions found. " + 
                "Solutions are listed below::\n")
            for solution in allsolutions:
                print(solution)

        # info command: gives program's instructions
        elif userinput == "info":
            print(
                "\nInstructions: \n"
                "   - Unknown characters can be written as '*', e.g. h*llo (*=e).\n" +
                "   - There can be maximum of 4 unknown characters, except for commands.\n"
                )

        # random command: prints 6 random solutions
        elif userinput == "random":
            randomsolutions = random_guesses()
            for randomsolution in randomsolutions:
                print(randomsolution)

        # remove command: removes characters that can be included in solutions
        elif userinput == "remove":
            charstoremove = input("Write characters to remove (use ',' to separate): \n")
            if not charstoremove:
                print("You must give one or more characters to remove.\n")
            else:
                removecharslist = list(filter(None,charstoremove.split(",")))
                if len(removecharslist) > 21:
                    print("There can't be over 21 characters ignored.")
                else:
                    for item in removecharslist:
                        if len(ignorecharacters) <= 21:
                            ignorecharacters.add(item)
                print("\nYou have succesfully removed following characters:\n")
                print(*sorted(removecharslist), sep = ", ")
                

        # ignored command: print ignored characters
        elif userinput == "ignored":
            if len(ignorecharacters) == 0:
                print("There are no ignored characters.")
            else:
                print("Next characters are ignored in solution results:\n")
                print(*sorted(ignorecharacters), sep = ", ")
                

        # add command: adds characters back to be included in solutions
        elif userinput == "add":
            charstoadd = input("Write characters to add back (use ',' to separate): \n")
            if not charstoadd:
                print("You must give one or more characters to add.")
            else:
                if len(ignorecharacters) == 0:
                    print("You must remove characters first.")
                else:
                    addcharslist = list(filter(None,charstoadd.split(",")))
                    for item in addcharslist:
                        ignorecharacters.remove(item)
                    print("Following characters were added back:\n")
                    print(*sorted(addcharslist), sep = ", ")

        # removes all the ignored characters
        elif userinput == "clear":
            ignorecharacters.clear()
            print("Ignored characters cleared.")

        # check that input isn't over 5 characters long
        elif len(userinput)>5:
            print("Word can't have over five characters. \n")

        # check that input isn't empty
        elif len(userinput)==0:
            print("Input can't be empty. \n")

        else:
            if userinput == "*****":
                print("Word can't have only empty characters. \n")
            else:
                solutions = word_helper(userinput)
                amountofsolutions = len(solutions)
                if len(solutions) == 0:
                    print("No solutions found.")
                else:
                    print(f"\nWith userinput '{userinput}' " +
                    f"total amount of {amountofsolutions}. " + 
                    "Solutions are listed below: \n")
                    for word in solutions:
                        print(f"{word}")

    return 
                
def main():
    '''
        Main function of program which includes commands function
    '''

    commands()
    
if __name__ == "__main__":
    main()
