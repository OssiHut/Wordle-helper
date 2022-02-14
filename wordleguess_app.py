from tkinter import *
import wordleguess

# errormessages
ERRORCHARACTER = "Input must include only alphabetic characters.\n"

# other messages

HELP = "\nInstructions: \n- Unknown characters can be written as '*',"\
    "e.g. h*llo (*=e).\n- There can be maximum of 4 unknown characters, except for commands.\n"

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
        self.window.configure(width=600,height=350)

        # text in the top of created frame
        lbl_toptext = Label(self.window, text="Hei")
        lbl_toptext.place(relwidth=1)

        # messagebox for output
        self.textwidget = Text(self.window,width=20,height=2)
        self.textwidget.place(relheight=0.8,relwidth=1,rely=0.05)
        self.textwidget.config(state=DISABLED)
        

        # scrollbar for output messagebox
        scrollbar = Scrollbar(self.textwidget)
        scrollbar.place(relheight=1, relx=0.95)
        scrollbar.configure(command=self.textwidget.yview)

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
            message = message.lower()
            # delete message from inputbox
            self.ent_message.delete(0,END)

            # display message that user sent
            message1 = f"{sender}: {message}\n"
            self.textwidget.configure(state=NORMAL)
            self.textwidget.insert(END,message1)
            self.textwidget.configure(state=DISABLED)
            

            
            self.textwidget.configure(state=NORMAL)
            # check that message contains only characters or stars
            if not message.isalpha() and "*" not in message:
                self.textwidget.insert(END,ERRORCHARACTER)
            elif message == "help":
                self.textwidget.insert(END,HELP)
            # command: random
            elif message == "random":
                guesses = wordleguess.random_guesses()
                self.textwidget.insert(END,"\n")
                for i in guesses:
                    self.textwidget.insert(END,f"{i}\n")
            
            self.textwidget.configure(state=DISABLED)
            self.textwidget.see(END)
            



if __name__ == "__main__":
    app = WordleGUI()
    app.run()