"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: K444362
Name:       Paavo Hintsa
Email:      paavo.hintsa@tuni.fi
This program is a scoreboard for '55 darts games.
More information about the game: https://www.youtube.com/watch?v=NjKVVAXdBP0
The scoreboard basically first asks all the information it needs from the user
and then turns into scoreboard and keeps up with the score until there is a
winner.
"""

from tkinter import *
class Darts:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Darts")
        self.__window.option_add("*Font", "Verdana 16")

        #Menubar
        self.__menubar =  Menu(self.__window)
        self.__quit_menu = Menu(self.__menubar)
        self.__sub_menu = Menu(self.__quit_menu, tearoff= 0)
        self.__sub_menu.add_command(label= "Yes", command= self.quit)
        self.__quit_menu.add_cascade(label= "Are you sure that you "
                                            "want to quit?",
                                     menu= self.__sub_menu)
        self.__quit_menu.add_separator()
        self.__menubar.add_cascade(label= "quit", menu= self.__quit_menu)
        self.__window.config(menu= self.__menubar)


        #Some key values that must be determined somewhere
        self.__whose_turn = 1
        self.__player_number = 1
        self.__playerdict = {}

        #The stuff on the first screen
        self.__user_input_label = Label(self.__window,
                                       text= f"Enter the target score")
        self.__user_input = Entry()

        self.__start_button = Button(self.__window, text= "Start the game!",
                                     command= self.start)

        self.__new_name_button = Button(self.__window,
                                        text= f"I have entered the right "
                                              f"target score",
                                        command= self.target_score)

        self.__error_panel = Label(self.__window)

        # The order of the stuff on first screen
        self.__error_panel.grid(row= 0, column= 0, columnspan= 2, sticky= E+W)
        self.__user_input_label.grid(row= 1, column= 0, sticky= W)
        self.__user_input.grid(row= 1, column= 1)
        self.__new_name_button.grid(row= 2, column= 1, sticky= W+E)
        self.__start_button.grid(row= 3, column= 1, sticky= W+E)

        self.__window.mainloop()

    def quit(self):
        """
        This method destroys the window
        """
        self.__window.destroy()

    def target_score(self):
        """
        This method receives target score from the user, evaluates it and
        turns the question asked from user to be the names of the players.
        """
        try:
            if len(self.__user_input.get()) < 3 or \
                    len(self.__user_input.get()) > 4:
                self.__error_panel.configure(
                    text= "Your target score must be reasonable!")

            elif int(self.__user_input.get()) < 155 or \
                    int(self.__user_input.get()) > 1055:
                self.__error_panel.configure(
                    text="Your target score must be between 155 and 1055!")

            elif int(self.__user_input.get()) % 5 != 0:
                self.__error_panel.configure(
                    text= "Your target score must be dividable by 5!")

            else:
                self.__target = int(self.__user_input.get())
                self.__user_input_label.configure(
                    text=f"Enter the name for the player"
                         f"{self.__player_number}")
                self.__new_name_button.configure(
                    text=f"I have entered name for the player"
                         f"{self.__player_number}",
                    command= self.new_name)
                self.__user_input.delete(0, END)
                self.__error_panel.configure(text="")

        except ValueError:
            self.__error_panel.configure(
                text="Your target score must be numbers!")

    def new_name(self):
        """
        Values the player name given to it and saves it to the playerdict.
        """
        if len(str(self.__user_input.get())) < 1 or \
                len(str(self.__user_input.get())) > 20:
            self.__error_panel.configure(
                text="The length of the name should be "
                     "between 1 and 20 characthters")

        else:
            self.__playerdict[self.__player_number] = []
            # It saves name as first member of the list
            self.__playerdict[self.__player_number].append(
                str(self.__user_input.get()))
            # The total score is second member of list. Everyone starts with
            # the target score
            self.__playerdict[self.__player_number].append(self.__target)
            self.__player_number += 1
            self.__user_input_label.configure(
                text=f"Enter the name for the player{self.__player_number}")
            self.__new_name_button.configure(
                text=f"I have entered name for "
                     f"the player{self.__player_number}")
            self.__user_input.delete(0, END)
            self.__error_panel.configure(text="")

    def clear_start_screen(self):
        """
        This method clears the start screen so that new screen can be built on
        it.
        """
        self.__error_panel.grid_forget()
        self.__user_input_label.grid_forget()
        self.__user_input.grid_forget()
        self.__new_name_button.grid_forget()
        self.__start_button.grid_forget()


    def scoreboard_view(self):
        """
        This method creates scoreboard view on empty screen.
        """
        #The stuff that is always the same on the screen
        self.__target_points = Label(self.__window, text= int(self.__target),
                                     bg= "red")
        self.__insert_score_button = Button(self.__window,
                                            text= "Insert score!",
                                            command= self.score)
        self.__insert_score = Entry()
        self.__notepanel = Label(self.__window,
                                 text= f"In turn: {self.in_turn()}")

        index = 1
        #the index determines the row of players name and score labels
        self.__point_labels = []
        #The point label list is necessary for updating the scoreboard

        #The changeable stuff on scoreboard view are made here
        for number in self.__playerdict:
            participant = Label(self.__window,
                                text= self.__playerdict[number][0])
            participant.grid(row= index, column= 0)

            current_score = Label(self.__window, text= self.__target)
            current_score.grid(row= index, column= 1)
            index += 1
            self.__point_labels.append(current_score)

        #The order of stuff that doesn't change
        self.__target_points.grid(row=0, column=0)
        self.__notepanel.grid(row=0, column= 1)
        self.__insert_score_button.grid(row= index, column= 0)
        self.__insert_score.grid(row= index, column= 1)


    def start(self):
        """
        This method checks whether user input is empty and then combines
        methods clear_start_screen and scoreboard_view to create new view
        """
        if len(str(self.__user_input.get())) > 0:
            self.__error_panel.configure(text= f"Attention: Player "
                                               f"{self.__user_input.get()} "
                                               f"is not joining you until you "
                                               f"press \"I have entered...\"")
        else:
            self.clear_start_screen()
            self.scoreboard_view()


    def whose_turn(self):
        """
        This method determines whether whose turn as number is not too big.
        :return: The information of whose turn it is as a number.
        """
        if self.__whose_turn > len(self.__playerdict):
            self.__whose_turn = 1

        return self.__whose_turn

    def in_turn(self):
        """
        :return: the information of whose turn it is as the players name
        """
        return self.__playerdict[self.whose_turn()][0]

    def score(self):
        """
        This method receives, evaluates and updates the score.
        """
        try:
            if int(self.__insert_score.get()) % 5 != 0:
                self.__notepanel.configure(text= "Score must be dividable by 5!")

            elif self.__playerdict[self.whose_turn()][1] -\
                    int(self.__insert_score.get()) < 0:
                self.__notepanel.configure(text= f"{self.in_turn()} "
                                                 f"bust the limit."
                                                 f" Insert score as 0")

            elif self.__playerdict[self.whose_turn()][1] - \
                    int(self.__insert_score.get()) == 0:
                self.__playerdict[self.whose_turn()][1] -= int(
                    self.__insert_score.get())
                self.__insert_score_button.configure(state= DISABLED)
                self.update_scoreboard()
                self.__notepanel.configure(text=f"{self.in_turn()} won!"
                                            f" Next up Pasila, "
                                                f"Porilaisten marssi")
            else:
                self.__playerdict[self.whose_turn()][1] -= \
                    int(self.__insert_score.get())
                self.__whose_turn += 1
                self.update_scoreboard()

        except ValueError:
            self.__notepanel.configure(text= "Score must be numbers!")


    def update_scoreboard(self):
        """
        This method updates the scoreboard.
        """
        for i in range(0, len(self.__playerdict)):
            self.__point_labels[i].configure(text=self.__playerdict[i+1][1])
        self.__notepanel.configure(text= f"In turn: {self.in_turn()}")
        self.__insert_score.delete(0, END)

def main():
    Darts()


if __name__ == "__main__":
    main()