import os

def clear_screen(osn):
    """
    clear_screen() clears screen depending on os.name
    """
    if osn == "nt":
        os.system("cls")
    elif osn == "posix":
        os.system("clear")
    else:
        raise SystemError("Unable to clear screen.")
    print("CREW TRAINING PROGRAMMER V 1.0\n")
    
def multiple_select_menu(mt):
    """
    Any parts of the program that require a list to be printed for options
    may reuse this function. It enumerates, formats and prints the items sent to it.
    """
    for ct, item in enumerate(mt, 1):
        print(f"{ct}\t{item}".expandtabs(4))
        

def input_string(msg):
    """
    Function returns a pure alpha string, without numbers, symbols or spaces.
    """
    while True:
        str_in = input(f"{msg}")
        # if test_valid_string(str_in):
        if str_in.isalpha():
            return str_in 
        else:
            print("Only alphabetical characters (with no spaces), please try again.")

            
def input_integer(msg, limits):
    """
    Function returns an integer, whitin the limits specified.
    """
    while True:
        try:
            num_in = int(input(f"{msg}"))
        except ValueError:
            print("Enter only numbers, please try again.")
        else:
            if limits[0] <= num_in <= limits[1]:
                return num_in
            else:
                print("Out of range, please try again.")
                

def input_Y_or_N():
    """
    Get a Yes or No answer. Boolean.
    """
    while True:
        YN_in = input("Enter Y or N: ").strip().upper()
        if YN_in == "Y":
            return True
        elif YN_in == "N":
            return False
        
