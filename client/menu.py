#######################################################################
# File: Menu.py
# Author(s): Chester Chan
# Date: 02/01/2024
# Description: Implements the menu system. 
####################################################################### 

class Menu:
    def __init__(self) -> None:
        pass


    def showMain(self):
        '''
        Show the main menu with all the options and wait for user input.
        Also checks if the given input is valid.

        Returns:
            int: chosen option
        '''
        
        options = { # Dictionary with all the options
            1: "logout",
            2: "download",
            3: "upload",
            4: "batch download",
            5: "chatting"
        }
        
        print("Main Menu: ")
        for num, option in options.items(): # Print all the options
            print(f"{num}. {option}")
        
        UInput = input("Enter option (number): ")
        # Check with a loop if the input is valid. 
        while(True):
            if(UInput.isnumeric() == False):
                print("Input was not a number, try again.")
                UInput = input("Enter option (number): ")

            else:
                UInput = int(UInput)
                if((UInput<1) or (UInput>5)):
                    print("Input was not a valid option, try again.")
                    UInput = input("Enter option (number): ")

                else:
                    break
       
        return options.get(UInput)

    # Op het moment niet gebruikt ivm mogelijke hoeveelheid parameters/variable die meegegeven moeten worden.
    # Zie client.py call_chosen_option() voor de huidige gebruikte implementatie.
    def excOption(self, option):
        '''
        Executes a function based on the given argument.

        Args:
            option (int): the function to excute
        
        Returns:
            options (int): the given option
        '''
        
        match option:
            case 1:
                # Function to execute
                # DUMMY
                print(option)
            
            case 2:
                # DUMMY
                print(option)
            
            case _:
                # DUMMY
                print("nothing")
        
        return option
    
   
                
