from tkinter import *
import wordleguess

# errormessages
ERRORCHARACTER = "ERROR: Input must include only alphabetic characters.\n"
TOOLONGERROR = "ERROR: Input can't be over five characters.\n"
ONLYEMPTY = "ERROR: Input can't contain only empty characters.\n"

# other messages

HELP = "\nInstructions: \n- Unknown characters can be written as '*',"\
    "e.g. h*llo (*=e).\n- There can be maximum of 4 unknown characters, except for commands.\n\n"

STARTINGMESSAGE = "Give a word or part of the word (max 5 characters) or a command. \n\n"\
            "Commands: \n"\
            "   help    : instructions \n"\
            "   all     : prints all of the solutions, filtered ignored \n"\
            "   random  : prints 6 random solutions \n"\
            "   remove  : removes desired characters to ignore set \n"\
            "   ignored : prints ignored characters \n"\
            "   add     : add ignored characters back \n"\
            "   clear   : clears all ignored characters\n\n"


class WordleGUI():
    '''
        GUI for Wordle helper
    '''
    def __init__(self):
        self.window = Tk()
        self.mainwindow()

    def run(self):
        '''
            executing program
        '''
        self.window.mainloop()
    
    def mainwindow(self):
        '''
            a frame for program
        '''

        # title and size configuration
        self.window.title("Wordle helper")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=800,height=400)

        # text in the top of created frame
        lbl_toptext = Label(self.window)
        lbl_toptext.place(relwidth=1)

        # messagebox for output
        self.textwidget = Text(self.window,width=20,height=2)
        self.textwidget.place(relheight=0.8,relwidth=0.85,rely=0.05,relx=0.15)
        self.textwidget.config(cursor="arrow",state=DISABLED)
       
        

        # scrollbar for output messagebox
        scrollbar = Scrollbar(self.textwidget)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.configure(command=self.textwidget.yview)
        self.textwidget.config(yscrollcommand=scrollbar.set)

        lbl_bottom = Label(self.window,bg="grey",height=80)
        lbl_bottom.place(relwidth=1,rely=0.85)
        
        # inputbox 
        self.ent_message = Entry(lbl_bottom,bg="lightgrey")
        self.ent_message.place(relwidth=1)
        self.ent_message.focus()
        self.ent_message.bind("<Return>",self.on_enter_pressed)

        self.textwidget.configure(state=NORMAL)
        self.textwidget.insert(END,STARTINGMESSAGE)
        self.textwidget.configure(state=DISABLED)

    def on_enter_pressed(self,event):
        '''
            get userinput and display it
        '''
        msg = self.ent_message.get()
        self.insert_message(msg,"Your input")

    def insert_message(self,message,sender):
        '''
            response to userinput
        '''
        if not message:
            return
        else:
            # transform message to lowercase
            message = message.lower()

            # delete message from inputbox
            self.ent_message.delete(0,END)

            # display message that user sent
            message1 = f"{sender}: {message}\n"
            self.textwidget.configure(state=NORMAL)
            self.textwidget.insert(END,message1)
            self.textwidget.configure(state=DISABLED)
            
            

            self.textwidget.configure(state=NORMAL) # allow writing

            ##################
            #  ERRORS START  #
            ##################

            # check that message contains only characters or stars
            if not message.isalpha() and "*" not in message:
                self.textwidget.insert(END,ERRORCHARACTER)
            
            
            # check that message contains only stars
            elif message == "*****":
                self.textwidget.insert(END,ONLYEMPTY)
            
            ##################
            #   ERRORS END   #
            ##################


            ##################
            # COMMANDS START #
            ##################

            # command: help
            elif message == "help":
                self.textwidget.insert(END,HELP)

            # command: random
            elif message == "random":
                guesses = wordleguess.random_guesses()
                self.textwidget.insert(END,"\nSix random solutions:\n\n")
                for i in guesses:
                    self.textwidget.insert(END,f"{i}\n")
                self.textwidget.insert(END,"\n")
            

            # command: all
            elif message == "all":
                allsolutions = wordleguess.filtered()
                solutionamount = len(allsolutions)
                if len(wordleguess.ignorecharacters)!=0:
                    self.textwidget.insert(END,"Following characters are ignored in results: \n")
                    self.textwidget.insert(END,*sorted(wordleguess.ignorecharacters),sep=", ")
                    self.textwidget.insert(END,"\n")
            
                self.textwidget.insert(END,f"Total of {solutionamount} solutions found. " + 
                    "Solutions are listed below:\n")
                for solution in allsolutions:
                    self.textwidget.insert(END,f"{solution}\n")

            # command: add
            elif message == "add":
                charstoadd = self.textwidget.insert(END,"Write characters to add back (use ',' to separate): \n")
                if len(wordleguess.ignorecharacters) == 0:
                    self.textwidget.insert(END,"You must remove characters first.")
                else:
                    addcharslist = list(filter(None,charstoadd.split(",")))
                    for item in addcharslist:
                        wordleguess.ignorecharacters.remove(item)
                    self.textwidget.insert(END,"Following characters were added back:\n")
                    self.textwidget.insert(END,*sorted(addcharslist), sep = ", ")

            ################
            # COMMANDS END #
            ################

            # solution finding
            else:
                # check that word or part of word isn't over 5 chars long
                if len(message)>5:
                    self.textwidget.insert(END,TOOLONGERROR)
                else:
                    solutions = wordleguess.word_helper(message)
                    amountofsolutions = len(solutions)
                    if len(solutions) == 0:
                        self.textwidget.insert(END,"No solutions found.")
                    else:
                        self.textwidget.insert(END,f"\nWith userinput '{message}' " +
                        f"total amount of {amountofsolutions}. " + 
                        "Solutions are listed below: \n\n")
                        for word in solutions:
                            self.textwidget.insert(END,f"{word}\n")


            self.textwidget.configure(state=DISABLED) # unallow writing

            # focus scrollbar to latest message
            self.textwidget.see(END)

            
            



if __name__ == "__main__":
    app = WordleGUI()
    app.run()