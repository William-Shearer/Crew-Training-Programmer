from pilotclass import AirlineCrew as ACrew
from utilityfuncs import clear_screen, multiple_select_menu, input_string, input_integer, input_Y_or_N
from os import name, getcwd, listdir
import sys
import pickle
from tabulate import tabulate
from time import sleep
from re import search

"""
Description:
This program uses the custom AirlineCrew object as a basis to create a Training Programmer sorter.
The user will create a data base with the add_pilot function.
Attributes required by the program will be filled in with appropriate data (the program has safeguards to ensure this).
Only the pid_sequence and records_count will be updated automatically.
It is important to understand the difference between them.
pid is a unique identifier. As this program is not made for a mega airline, up to 200 unique pids will be generated.
count is how many pilots are actually in the data base. This may differ from the pid sequence, as pilots are deleted
from the database.
When the program database assigns pid number 200, adding any more pilots will be inhibited.
This is a feature, the value of the variable could be changed to accomodate more.
A created data base may be saved to disc, and also loaded from disc if one was previously stored.
As a pilot's data changes (ie; they accumulate more hours, or they change position), an edit_pilot function allows the
user to modify a particular pilot via citing that crew members pid.
"""


# GLOBALS, LISTS, DICTS and TUPLES...

menu_tuple = {
    "main":("Add a pilot", "View pilots", "Edit a pilot", "Delete a pilot", "Match training", "Output pdf file", "Load a data base", "Clear current data base (reset)", "Save data current base", "Exit program"),
    "edit":("Edit name", "Edit position", "Edit base month", "Edit hours", "Exit edit")
    }

# heads_short = ["First name", "Surname", "Position", "Base month", "Total hours"]
heads_long = ["PID", "First name", "Surname", "CM Pos", "PC", "LOFT", "Hours"] 

def main():
    pilot_list = []
    # pilot_data = []
    
    while True:
        clear_screen(name)
        print("MAIN MENU")
                
        multiple_select_menu(menu_tuple["main"])
        choice = input_integer("Select: ", (1, len(menu_tuple["main"])))
        #print(f"DEBUG: {choice}")
        #input("Continue")
        if choice == 1:
            p_obj = add_pilot()
            if p_obj != None:
                print("PILOT ENTERED.")
                pilot_list.append(p_obj)
                p_obj = None
                sleep(1)
                # print(p_obj) # DEBUG
                
            else:
                print("ABORTED.")
                sleep(1)
                
            # print(f"DEBUG: {choice}")
            # input("Continue")
            
        elif choice == 2:
            # Boolean return ignored. Not needed here.
            view_pilots(pilot_list)
                        
        elif choice == 3:
            edit_pilot(pilot_list)
            
        elif choice == 4:
            delete_a_pilot(pilot_list)
            
        elif choice == 5:
            ...
            
        elif choice == 6:
            ...
            
        elif choice == 7:
            stage_list = load_data_base()
            # print(stage_list) # DEBUG, comment out
            # input("Hit ENTER to continue... ") # DEBUG
            if stage_list != None:
                if len(pilot_list) > 0:
                    # Just make sure there is a nice, clean list to copy into...
                    pilot_list.clear()
                pilot_list = stage_list[:]
                # NOTE; The [:] is important when intending to make a copy of a list. 
                # If not used, you make a siamese twin of the list, in effect. If one dies, so does the other.
                stage_list.clear()
                
        elif choice == 8:
            reset_data_base(pilot_list)
                
        elif choice == 9:
            save_data_base(pilot_list)
            
        elif choice == 10:
            terminate_program()
            
        else:
            # Trap any error to do with menu selections. Warn and exit.
            sys.exit("Other Error. Terminated. Inform the developer.")


def add_pilot():
    """
    Function to build the data for a new pilot in the DB.
    This function must first ask the user if the input data is correct,
    then create the object. The idea is that it does not arbitrarily create
    objects with unique pids if the user makes a mistake.
    (It is quite a monstruous function).
    It returns the object, if it was created, otherwise None.
    """
        
    # Set names
    clear_screen(name)
    print("ADD PILOT")
    firstname, surname = set_names()
    
    # Set CM position
    clear_screen(name)
    print("ADD PILOT")
    position, position_str = set_cm_position()
    
    # Set months
    clear_screen(name)
    print("ADD PILOT")
    basemonth, loftmonth, basemonth_str, loftmonth_str = set_months()
    
    # sys.exit("TESTED") # DEBUG
    clear_screen(name)
    print("ADD PILOT")
    totalhours, totalhours_str = set_hours()
    
    # Class to hold data for tabulation grid.
    p_object = ACrew()
        
    # Delete the attributes from the class that this application does not use (nice trick!).
    del p_object.middlename
    del p_object.licensenum
    del p_object.pichours
    del p_object.sichours
    del p_object.status
    
    # Set the utilized attributes.    
    p_object.firstname = firstname
    p_object.surname = surname
    p_object.position = position
    p_object.basemonth = basemonth
    p_object.tothours = totalhours
       
    # Add an attribute to the class that the application does need (another nice run time trick).
    # The lambda function sets the LOFT month 6 months away from the Base month.
    setattr(p_object, "_LOFTmonth", (lambda a, b: a if (p_object.i_basemonth > 5) else b)((p_object.i_basemonth - 6), (p_object.i_basemonth + 6)))
        
    # DO NOT try to increase pid_sequence or record count manually here, specifically.
    # This is accomplished automatically by the class. Reminder.
    
    pilot_data = []
    
    # pilot_data.append([])
    pilot_data.append(p_object)
    
    clear_screen(name)
    # print(f"ADD PILOT\nIs this data correct?")
    if tabulation_routine(pilot_data, True):
        return p_object
    else:
        del p_object
        # Right here. The pid_sequence is not automatically handled by the class, 
        # and needs addressing. Count is handled automatically (decremented).
        # This is an unusual case, as the instance was already created, and
        # the sequence needs restoring to previous value. It is a ghost instance,
        # yet to be confirmed, and here aborted.
        ACrew.pid_sequence -= 1
        return None
    
    # Clear the pilot data list right here. No issues later with anything like persistence. Just in case.
    # Scratch. Don't be concerned. It is not like that with Python. Not static.
    # pilot_data.clear()
    # If the pilot creation is rejected, some other mechanism must handle it (in main())
 

def tabulation_routine(dl, confirm = False):
    pilot_data = []
    jump, start, stop, end, list_len = 10, 0, 0, False, len(dl)
    # REF: ["PID", "First name", "Surname", "CM Pos", "PC", "LOFT", "Hours"]
    
    # Put everything from the object list into the list of lists first, to
    # avoid any problems with indices later...
    for i in range(len(dl)):
        pilot_data.append([])
        pilot_data[i].append(dl[i].pilot_id) # PID
        pilot_data[i].append(dl[i].firstname)
        pilot_data[i].append(dl[i].surname)
        pilot_data[i].append(dl[i].position)
        pilot_data[i].append(dl[i].basemonth)
        pilot_data[i].append(ACrew.base_month[dl[i]._LOFTmonth])
        pilot_data[i].append(dl[i].tothours)
    
    while end == False:
        if (stop := start + jump) > (list_len - 1):
            stop = start + (list_len - start)
            end = True
        
        # Then just hand tabulate a slice of the pilot_data list at a time, which is good stuff!
        clear_screen(name)
        print("VIEW PILOT(S)")
        print(f"Pilot_count: {ACrew.record_count}") # DEBUG
        print(f"Current pid sequence: {ACrew.pid_sequence}") # DEBUG
        print(tabulate(pilot_data[start:stop], heads_long, tablefmt = "grid"))
            
        start = start + jump
        
        if confirm == False:
            input("Hit ENTER to continue... ")
        else:
            print("Is this data correct?")
            if not input_Y_or_N():
                confirm = False
        
    return confirm
        
    # Self clean up, just a reminder of how it was. Don't worry about it!
    # pilot_data.clear()
 

def view_pilots(pl):
    """
    A function, boolean return, that displays a table of all the pilots in a data base.
    The function return true if instances of the AirlineCrew class exist, and can be transferred to the 
    pilot_data list of lists, which is needed for tabulate to work correctly.
    It returns false if the pilot_data list cannot be built. Usually, this would be
    because there are no instances of the class. Returning false can be used by main() to divert to the
    data base load function, so a data base can be loaded (assumes the user forgot to load before
    checking what data is in it). It is a safeguard, to avoid crashes due to exceptions.
    """
    # clear_screen(name)
    pilot_data =[] 
    # print("VIEW PILOTS")
    
    if len(pl) > 0:
        tabulation_routine(pl)
        table_exists = True
    else:
        clear_screen(name)
        print("VIEW PILOT(S)\nNo pilots entered into data base. Cannot view.")
        # print("Continue?")
        # input_Y_or_N()
        input("Hit ENTER to continue... ")
        table_exists = False
        
    return table_exists


def edit_pilot(pl):
    """
    Function to edit a specific pilot.
    Contains a submenu to edit particular attributes of the pilot.
    """
    #clear_screen(name)
    #print("EDIT PILOT")
    found_pilot = False
    if len(pl) > 0:
        clear_screen(name)
        print("EDIT PILOT")
        pilot_id = input_integer("Enter Pilot ID (PID) of pilot to edit: ", (1, ACrew.pid_sequence))
        for pid in pl:
            if pid.pilot_id == pilot_id:
                # print("That pilot is present!") # DEBUG
                found_pilot = True
                edited_pilot = pid
                break
                
        if found_pilot == False:
            print("Pilot ID match not found.")
            input("Hit Enter to continue... ")
        else:
            # If the pilot of that ID was found, proceed to edit.
            selection = -1
            while selection != 5:
                clear_screen(name)
                print("EDIT PILOT")
                multiple_select_menu(menu_tuple["edit"])
                selection = input_integer("Select: ", (1, len(menu_tuple["edit"])))
                print("")
                
                # dummy just uses up the rest of the unpacked tuple, a property that
                # will not be used in this program, or at least, not in this function...
                
                if selection == 1:
                    edited_pilot.firstname, edited_pilot.surname = set_names()
                elif selection == 2:
                    edited_pilot.position, dummy = set_cm_position()
                elif selection == 3:
                    edited_pilot.basemonth, edited_pilot._LOFTmonth, dummy, dummy = set_months()
                elif selection == 4:
                    edited_pilot.tothours, dummy = set_hours()
                else:
                    break
                
            #input("Hit ENTER to continue... ") # TEMPORARY!
            print("END EDIT.")
            sleep(1)
    else:
        clear_screen(name)
        print("EDIT PILOT\nNo pilots in data base.")
        input("Hit ENTER to continue... ")
    return found_pilot


def delete_a_pilot(pl):
    """
    Function to delete a pilot from the memory data base.
    As pilot IDs are unique, there will be no resorting of this attribute.
    """
    pilot_found = False
    clear_screen(name)
    print("DELETE A PILOT")
    if len(pl) > 0:
        del_pid = input_integer("Select pilot ID to delete: ", (1, ACrew.pid_sequence))
        for pid in pl:
            if del_pid == pid.pilot_id:
                del_pilot = pid
                pilot_found = True
                break
        if not pilot_found:
            print(f"Pilot of ID {del_pid} not found.\nMaybe already deleted?")
            input("Hit ENTER to continue... ")
            return pilot_found
        else:
            pilot_data = []
            pilot_data.append(del_pilot)
            if tabulation_routine(pilot_data, True):
                print("DELETING PILOT")
                sleep(1)
                pl.remove(del_pilot)
            else:
                print("ABORTED.")
                sleep(1)
            return pilot_found
    else:
        print("No pilots in data base.")
        input("Hit ENTER to continue... ")
        return pilot_found


def load_data_base():
    """
    All databases for the pilotDB are stored in the proprietary .dpb format, saved with pickle dump().
    This function uses regex to locate any file that has that extension, and adds it to a file_list.
    That list, if any items exist, is then presented to the user for loading, or cancel.
    """
    clear_screen(name)
    print("LOAD A DATA BASE")
    # From os lib.
    # First section. IO stuff.
    file_list = []
    temp_pilot_list = None
    path = fr"{getcwd()}"
    
    # print(path)
    # list_dir creates a list of files that are in the directory.
    # Only ones with extension .dpb are required to be displayed.
    # If the regex search satisfies that parameter, the file name is added to file_list. 
    files = listdir(path)
    # From regex (search).
    for file in files:
        try:
            if search(r"(\.[^.]+)", file.lower()).group(0) == ".dpb":
                # print(file)
                file_list.append(file)
        except AttributeError:
            # Nothing to do, just catch the error and stop it from creating a catastrophe.
            # What this means is that regex did not find a match with search. If it did not
            # "try" first, the program would crash with an AttributeError. A failed
            # regex attempt returns a NoneType attribute error.
            pass
    
    # If files were found that had extension .dpb, then here they will be displayed in a menu for selection.
    # If the user did not intend to load a data base and ended up here by accident, no problem;
    # Select any file and when prompted to write the data base to memory, choose the NO option.
    if len(file_list) > 0:
        multiple_select_menu(file_list)
        input_file = file_list[input_integer("Choose the data base to load: ", (1, len(file_list))) - 1]
        
        with open(input_file, "rb") as list_dump_file:
            dump_list = pickle.load(list_dump_file)
        
        print("This will overwrite any existing data base. Continue?")
        if input_Y_or_N():
            ACrew.pid_sequence = dump_list[0][0]
            ACrew.record_count = dump_list[0][1]
            temp_pilot_list = dump_list[1]
            # success = True
            print("DATA BASE LOADED...")
            sleep(1)
            return temp_pilot_list
            
        else:
            # temp_pilot_list = None # Set by default.
            print("LOAD ABORTED...")
            sleep(1)
            return None
        
            
    else:
        print("No saved data base files on disc.")
        input("Hit ENTER to continue... ")
        # temp_pilot_list = None # Set by default.
        return None


def reset_data_base(pl):
    clear_screen(name)
    
    if len(pl) > 0 and ACrew.pid_sequence > 0 and ACrew.record_count > 0:
        print("RESET THE DATA BASE.\nWARNING: All unsaved changes will be lost! Continue?")
        # if input("Y for Yes, or enter any other key for No: ").upper() == "Y":
        if input_Y_or_N():
            # Reset the whole data base and class in memory to start up situation.
            pl.clear()
            ACrew.pid_sequence = 0
            ACrew.record_count = 0
            print("DATA BASE RESET.")
            sleep(1)
            return True
        else:
            print("RESET ABORTED.")
            sleep(1)
            return False
    else:
        print("No data base to reset.")
        input("Hit Enter to continue... ")
        return False
        
   
def save_data_base(pl):
    clear_screen(name)
    if len(pl) == 0:
        print("No data base in memory to save.")
        input("Hit ENTER to continue... ")
        return False
    
    # Format the list for the pickle dump.
    save_list = [[ACrew.pid_sequence, ACrew.record_count], pl]
    file_name = input_string("Enter a name for the file to save (no numbers or extension)")
    with open(fr"{file_name}.dpb", "wb") as list_dump_file:
        pickle.dump(save_list, list_dump_file)
        
    save_list.clear()
    print("Data base saved.")
    input("Hit ENTER to continue... ")
    return True


def terminate_program():
    """
    As the title says. Nothing special here... :)
    """
    clear_screen(name)
    sys.exit("Program terminated.\nThank you for using CREW TRAINING PROGRAMMER V 1.0\nBy William Shearer, 2022, programmed in Python 3\n")
    

def set_names():
    print("Set Name")
    # while True:
    firstname = input_string("Input given name: ").strip().capitalize()
    surname = input_string("Input surname: ").strip().capitalize()
    # print(f"Pilot name is {firstname} {surname}. Is this correct?")
    # if input_Y_or_N():
    #     break
    
    return (firstname, surname)

        
def set_cm_position():
    print("Set Crew Member Position")
    # while True:
    multiple_select_menu(ACrew.cm_position)
    position = input_integer("Pilot's crew position: ", (1, 2)) - 1
    position_str = ACrew.cm_position[position]
    # print(f"Crew member position is {position_str}. Is this correct?")
    # if input_Y_or_N():
    #     break
    
    return (position, position_str)


def set_months():
    print("Set Base Month")
    # while True:
    multiple_select_menu(ACrew.base_month)
    basemonth = input_integer("Base month: ", (1, 12)) - 1
    basemonth_str = ACrew.base_month[basemonth]
    loftmonth = (lambda a, b: a if (basemonth > 5) else b)((basemonth - 6), (basemonth + 6))
    loftmonth_str = ACrew.base_month[loftmonth]
    # print(f"LOFT month: {ACrew.base_month[loftmonth]}") # DEBUG
    # print(f"Base Month is {basemonth_str}. Is this coorect?")
    # if input_Y_or_N():
    #     break
            
    return (basemonth, loftmonth, basemonth_str, loftmonth_str)

def set_hours():
    print ("Set Total Hours")
    # while True:
    totalhours = input_integer("pilot's total flying hours: ", (ACrew.LOWER_LIMIT, ACrew.UPPER_LIMIT))
    totalhours_str = f"{totalhours:,}"
    # print(f"Total hours are {totalhours_str}. Is this correct?")
    # if input_Y_or_N():
    #     break
            
    return (totalhours, totalhours_str)
    
def function1():   
    ...
    
def function2():
    ...
    
def function3():
    ...
    
    
if __name__ == "__main__":
    main()