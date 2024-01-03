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

        print("Main menu:")
        print("1. View files")
        print("2. Download")
        print("3. Upload")
        print("4. Chat")
        print("5. Logout\n")
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
       
        return UInput
    

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
    
   
                
