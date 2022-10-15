class AirlineCrew:
    """
    This class is for a large, crew training orientated application for an airline.
    It includes these attributes:
    - Company Unique Pilot Record ID
    - Pilot given name
    - Pilot middle name
    - Pilot surname
    - Pilot CM position
    - Pilot license number
    - Pilot training base month
    - Pilot total hours experience
    - Pilot hours PIC
    - Pilot hours SIC
    - Pilot hours as Instructor
    - Pilot hours as Student
    Any class attributes may be deleted if the current application does not require them.
    The class is adaptable to different UI styles, in as much as possible, as it contains its own
    error catching routines. It is, however, the task of the application that uses this class to
    ensure data submission is presented:
    - In a manner that response to errors is properly manages.
    - That data is not passed to attributes that were suppressed (del) in creating the class instances.
    """
    
    # The pid will not necessarily be sequential in an application. It is a unique identifier.
    # If a pilot record is deleted, all pids remain as they were originally, and blanks will
    # develop between a pid sorted sequence. This is intentional, as it is a reference to pilots
    # who have left the company.
    
    UPPER_LIMIT = 55000
    LOWER_LIMIT = 200
    NEVER_LIMIT = 0
    
    pid_sequence = 0
    record_count = 0
    cm_position = ("CAP", "FO")
    base_month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
        
    def __init__(self):
        """
        Initializes a blank record with all attributes active.
        The application can tailor the requirements by setting and deleting attributes that will be used 
        or are otherwise not needed.
        """
        self._pid = AirlineCrew.pid_sequence + 1
        AirlineCrew.pid_sequence = self._pid
        AirlineCrew.record_count += 1
        self._fname = ""
        self._mname = ""
        self._sname = ""
        self._pos = 0
        self._licno = ""
        self._bmonth = 0
        self._totalhrs = 0
        self._pichrs = 0
        self._sichrs = 0
        self._status = True

    
    def __del__(self):
        """
        Completely removes a record.
        """
        AirlineCrew.record_count -= 1
        # DEBUG
        # print(f"Record {self._pid} successfully deleted.")
        
    def __str__(self):
        """
        Formats a record resume.
        NOTE: Any record should at least contain:
        - Pilot's first name
        - Pilot's surname
        - Pilot's total hours
        These are what is printed.
        Functions to delete these attributes in the properties are suppressed for this reason.
        All records have a pid, which cannot be modified in any way (set by __init__).
        """
        return f"Pilot record ID {self._pid} is {self._fname} {self._sname}, with {self._totalhrs:,} hours (total)"
    
    # For the learning experience, this is being done the "old fashioned Python" way deliberately.
    # The neo decorated @attribute method is understood, but not used.
    # -----------------------------------------------------------------------------------------------
    # CLASS METHODS
    
    def check_number(self, val):
        """
        General class method to catch error where entry should be a positive integer. 
        Returns -1 on Error.
        The application that uses this class must ensure that on Error return the user is reprompted,
        or an error message is sent.
        """
        try:
            ival = int(val)
        except ValueError:
            # DEBUG
            # print("Invalid data.")
            return -1
        else:
            if ival >= 0:
                return ival
            else:
                # DEBUG
                # print("Invalid data.")
                return -1
    
    def check_hours_limits(self, hours, limits):
        """
        Method checks that pilot hours are within reasonable limits.
        Variable limits is a tuple, passed when calling the method.
        """
        if hours < limits[0] or hours > limits[1]:
            return -1
        else:
            return hours
    
    def check_hours_integrity(self):
        """
        Specific method, to be called by the application, that checks if the hours have integrity in the object.
        Neither PIC hours, SIC hours, or the sum of them, should ever be greater than the TOTAL hours.
        As PIC hours and SIC hours are deletable attributes, their existence must be checked first.
        Returns boolean. The application can do what it needs to to correct the problem.
        """
        if hasattr(self, "_pichrs") and not hasattr(self, "_sichrs"):
            # DEBUG
            # print(f"PIC hours: {self._pichrs:,}") 
            if self._pichrs > self._totalhrs:
                return False
        elif hasattr(self, "_sichrs") and not hasattr(self, "_pichrs"):
            # DEBUG
            # print(f"SIC hours: {self._sichrs:,}")
            if self._sichrs > self._totalhrs:
                return False
        elif hasattr(self, "_pichrs") and hasattr(self, "_sichrs"):
            # DEBUG
            # print(f"PIC hours: {self._pichrs:,}")
            # print(f"SIC hours: {self._sichrs:,}")
            if (self._pichrs + self._sichrs) > self._totalhrs:
                return False
        
        return True
            
    # -----------------------------------------------------------------------------------------------
    # SETS
    def _set_pid(self, pid):
        """
        Sets the pid manually. To be used very carefully.
        A mechanism should be implemented in the application to guarantee that
        it does not duplicate existing pids in other instances of this class.
        """
        if AirlineCrew.check_number(self, pid):
            self._pid = pid
    
    def _set_fname(self, fname):
        """
        Sets the pilot's first name. String.
        """
        self._fname = fname.strip().capitalize()
        
    def _set_mname(self, mname):
        """
        Sets the pilots middle name. String.
        """
        self._mname = mname.strip().capitalize()
        
    def _set_sname(self, sname):
        """
        Sets the pilot's surname. String.
        """
        self._sname = sname.strip().capitalize()
        
    def _set_pos(self, pos):
        """
        Sets the crew member position, CAP or FO.
        If the position is > 1, and error is thrown (-1), and returned.
        The application must handle it.
        Otherwsie, the position is set 0 = CAP, 1 = FO.
        """
        temp_pos = AirlineCrew.check_number(self, pos)
        if temp_pos > 1:
            return -1
        else:
            self._pos = temp_pos
    
    def _set_licno(self, licno):
        """
        Sets the license number. This is actually a string. Some licenses include alpha characters.
        """
        self._licno = licno.strip().upper()
    
    def _set_bmonth(self, bmonth):
        """
        Sets the base month.
        Catch error. If the month is greater than 11, it is invalid.
        Less than 0 is already caught in check_number method.
        Base month is set to -1 if there is an error.
        The application must consider this return value, and correct as needed.
        """
        temp_bmonth = AirlineCrew.check_number(self, bmonth)
        if temp_bmonth > 11:
            # DEBUG
            # print("Month error.")
            self._bmonth = -1
        else:
            self._bmonth = temp_bmonth
            
        
    def _set_totalhrs(self, totalhrs):
        """
        Sets the total hours for the pilot. If the total hours exceed the limits
        provided by the tuple, then -1 is returned.
        The limits are based on 200 hours total minimum hours to be an airline pilot
        and a career maximum of 55000.
        """
        temp_hours = AirlineCrew.check_number(self, totalhrs)
        self._totalhrs = AirlineCrew.check_hours_limits(self, temp_hours, (AirlineCrew.LOWER_LIMIT, AirlineCrew.UPPER_LIMIT))
                
    def _set_pichrs(self, pichrs):
        """
        Sets the PIC hours for the pilot. If the PIC hours exceed the limits
        provided by the tuple, then -1 is returned.
        """
        temp_hours = AirlineCrew.check_number(self, pichrs)
        self._pichrs = AirlineCrew.check_hours_limits(self, temp_hours, (AirlineCrew.NEVER_LIMIT, AirlineCrew.UPPER_LIMIT))
        
    def _set_sichrs(self, sichrs):
        """
        Sets the SIC hours for the pilot. If the total hours exceed the limits
        provided by the tuple, then -1 is returned.
        """
        temp_hours = AirlineCrew.check_number(self, sichrs)
        self._sichrs = AirlineCrew.check_hours_limits(self, temp_hours, (AirlineCrew.NEVER_LIMIT, AirlineCrew.UPPER_LIMIT))
        
    def _set_status(self, status):
        """
        Resets the pilot status to either True or False. If the input variable is neither
        True or False, it does not change the status.
        """
        if status == True or status == False:
            return status
        
            
    
    # GETS
    def _get_pid(self):
        """
        Get the pid attribute. It is an integer.
        """
        return self._pid
    
    def _get_fname(self):
        """
        Get the _fname attribute, usually for printing. It is a string.
        """
        return self._fname
    
    def _get_mname(self):
        """
        Get the _mname attribute, usually for printing. It is a string.
        """
        return self._mname
    
    def _get_sname(self):
        """
        Get the _sname attribute, usually for printing. It is a string.
        """
        return self._sname
        
    def _get_pos(self):
        """
        Get the _pos attribute. It is an integer.
        It returns a string form the class global tuple cm_position.
        """
        return AirlineCrew.cm_position[self._pos]
        
    def _get_int_pos(self):
        """
        Get the raw integer of the attribute _pos.
        """
        return self._pos
        
    def _get_licno(self):
        """
        Get the _licno attribute, usually for printing. It is a string.
        """
        return self._licno
        
    def _get_bmonth(self):
        """
        Get the _pos attribute. It is an integer.
        It returns a string form the class global tuple base_month.
        """
        return AirlineCrew.base_month[self._bmonth]
        
    def _get_int_bmonth(self):
        """
        Special getter to return the integer of the base month, not formatted to string.
        """
        return self._bmonth
        
    def _get_totalhrs(self):
        """
        Get the _totalhrs attribute.
        It is an integer, formatted to a string for output.
        """
        return f"{self._totalhrs:,}"
        
    def _get_int_totalhrs(self):
        """
        Get the raw integer of the attribute _totalhrs.
        """
        return self._totalhrs
    
    def _get_pichrs(self):
        """
        Get the _pichrs attribute.
        It is an integer, formatted to a string for output.
        """
        return f"{self._pichrs:,}"
        
    def _get_int_pichrs(self):
        """
        Get the raw integer of the attribute _pichrs.
        """
        return self._pichrs
        
    def _get_sichrs(self):
        """
        Get the _sichrs attribute.
        It is an integer, formatted to a string for output.
        """
        return f"{self._sichrs:,}"
        
    def _get_int_sichrs(self):
        """
        Get the raw integer of the attribute _sichrs.
        """
        return self._sichrs
        
    def _get_status(self):
        """
        Return the status as an Active or Passive string value.
        """
        if self._status == True:
            return "Active"
        else:
            return "Passive"
        
    
    # DELETES
    
    # pid protected.
    # def _del_pid(self):
    #     del self._pid
    
    # fname protected.
    # def _del_fname(self):
    #     del self._fname
    
    def _del_mname(self):
        """
        Deletes attribute _mname from the class member (instance).
        It will no longer be accessible.
        Recommendation using attributes in an application, for safety.
        try:
            ...
            # Do something with the attribute. If it is not there...
        except AttributeError:
            print("No attribute present.")
        """
        del self._mname
    
    # sname protected    
    # def _del_sname(self):
    #     del self._sname
        
    def _del_pos(self):
        """
        Delete the attribute _pos from the instance.
        """
        del self._pos
        
    def _del_licno(self):
        """
        Delete the attribute _licno from the instance.
        """
        del self._licno
        
    def _del_bmonth(self):
        """
        Delete the attribute _bmonth from the instance.
        """
        del self._bmonth
    
    # totalhrs protected
    # def _del_totalhrs(self):
    #     del self._totalhrs
        
    def _del_pichrs(self):
        """
        Delete the attribute _pichrs from the instance.
        """
        del self._pichrs
        
    def _del_sichrs(self):
        """
        Delete the attribute _sichrs from the instance.
        """
        del self._sichrs
        
    def _del_status(self):
        """
        Delete the attribute _status from the instance.
        """
        del self._status
         
    
    # CLASS ATTRIBUTE PROPERTIES
    pilot_id = property(
        fget = _get_pid,
        fset = _set_pid,
        # fdel = _del_pid,
        doc = "Property to set or retrieve the pid attribute."
        )
    
    firstname = property(
        fget = _get_fname,
        fset = _set_fname,
        # fdel = _del_fname,
        doc = "Property to set or retrieve the pilot's first name attribute."
        )
        
    middlename = property(
        fget = _get_mname,
        fset = _set_mname,
        fdel = _del_mname,
        doc = "Property to set, retrieve or delete the pilot's middle name attribute."
        )
    
    surname = property(
        fget = _get_sname,
        fset = _set_sname,
        # fdel = _del_sname,
        doc = "Property to set or retrieve the pilot's surname attribute."
        )
        
    position = property(
        fget = _get_pos,
        fset = _set_pos,
        fdel = _del_pos,
        doc = "Property to set, retrieve or delete the pilot's CM position attribute."
        )
        
    i_position = property(
        fget = _get_int_pos,
        doc = "Special property to return the raw integer of the position attribute."
        )
        
    licensenum = property(
        fget = _get_licno,
        fset = _set_licno,
        fdel = _del_licno,
        doc = "Property to set, retrieve or delete the pilot's license number attribute."
        )
        
    basemonth = property(
        fget = _get_bmonth,
        fset = _set_bmonth,
        fdel = _del_bmonth,
        doc = "Property to set, retrieve or delete the pilot's base month attribute."
        )
    
         
    i_basemonth = property(
        fget = _get_int_bmonth,
        doc = "Special property to return the raw integer attribute value of basemonth."
        )
        
    tothours = property(
        fget = _get_totalhrs,
        fset = _set_totalhrs,
        # fdel = _del_totalhrs,
        doc = "Property to set or retrieve the pilot's total hours attribute."
        )
        
    i_tothours = property(
        fget = _get_int_totalhrs,
        doc = "Special property to get the raw integer of the totalhrs attribute."
        )
        
    pichours = property(
        fget = _get_pichrs,
        fset = _set_pichrs,
        fdel = _del_pichrs,
        doc = "Property to set, retrieve or delete the pilot's PIC hours attribute."
        )
    
    i_pichours = property(
        fget = _get_int_pichrs,
        doc = "Special property to get the raw integer of the pichrs attribute."
        )
    
    sichours = property(
        fget = _get_sichrs,
        fset = _set_sichrs,
        fdel = _del_sichrs,
        doc = "Property to set, retrieve or delete the pilot's SIC hours attribute."
        )
    
    i_sichours = property(
        fget = _get_int_sichrs,
        doc = "Special property to get the raw integer of the sichrs attribute."
        )
    
    status = property(
        fget = _get_status,
        fset = _set_status,
        fdel = _del_status,
        doc = "Property to set, retrieve or delete the pilots status."
        )



# TESTING CLASS (Documentation examples)
"""
# Create a record.
P1 = AirlineCrew()
P1.firstname = "   fred   "
P1.surname = "greg"
P1.tothours = 4567
P1.basemonth = "APR"
P1.basemonth = "4"

# Delete attributes that are not used.
del P1.middlename
del P1.position
del P1.licensenum
del P1.pichours
del P1.sichours

print(P1, P1.basemonth)

P2 = AirlineCrew()
P2.firstname = "Anne"
P2.surname = "    Coughlan"
P2.tothours = "   2345"
P2.pichours = "1250   "
P2.sichours = "  1150  "
# No need to strip spaces around numbers if entered as string.

print(f"Integrity of hours is {P2.check_hours_integrity()}")

# Test that integrity adheres to conditions.
del P2.sichours

print(f"Integrity of hours is {P2.check_hours_integrity()}")

# Try to delete an attribute that has no delete call (protected).
try:
    del P2.tothours
except AttributeError:
    print("Cannot delete that attribute.")

print(f"Total Hours: {P2.tothours}")
print(f"Record count: {AirlineCrew.record_count}")

# Check that record count updates correctly
del P2

print(f"Record count: {AirlineCrew.record_count}")

# Complete example
P2 = AirlineCrew()
P2.firstname = "alexander "
P2.middlename = "   DANIEL "
P2.surname = "  RowaN"
P2.position = "1"
P2.licensenum = "2094PTLA"
P2.basemonth = 4
P2.tothours = 2345
P2.pichours = 1250
P2.sichours = 1150

# lambda to create and set attributs example:
setattr(P2, "_LOFTmonth", (lambda a, b: a if (P2._bmonth > 5) else b)((P2._bmonth - 6), (P2._bmonth + 6)))

print(f"BASE MONTH: {P2._bmonth}\nLOFT MONTH: {P2._LOFTmonth}")

print(f"New pid: {P2._pid}")

print(f"Record: {P2._pid}: {P2.firstname} {P2.middlename} {P2.surname} is a {P2.position} with licence {P2.licensenum}.")
print(f"PIC: {P2.pichours}\nSIC: {P2.sichours}\nTOTAL: {P2.tothours}")
print(f"Base Month: {P2.basemonth}")

print(f"Record count: {AirlineCrew.record_count}")
"""