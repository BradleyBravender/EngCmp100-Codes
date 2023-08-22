# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Bradley Bravender (100%)
# Student CCID: ____
# Others:
#
# To avoid plagiarism, list the names of persons, Version 0 author(s)
# excluded, whose code, words, ideas, or data you used. To avoid
# cheating, list the names of persons, excluding the ENCMP 100 lab
# instructor and TAs, who gave you compositional assistance.
#
# After each name, including your own name, enter in parentheses an
# estimate of the person's contributions in percent. Without these
# numbers, adding to 100%, follow-up questions may be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#
# ----------Students write/modify their code below here ---------------------

## Setting up the lists, importing numpy, and recieivng user input
#
import numpy as np
print('Lab 2 - Version 2')
day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday", \
            "Sunday"] # a 0-6 list of day name strings
place_list = ["bridge","library","river crossing","airport","bus terminal", \
              "hospital","railway station"] # a second string list
code = input('Please enter a code to break: ')
code = np.array(list(code),dtype=int)

## Rule1: equals the length of the users input so that I can detect if the 
# length is correct  
rule_1 = len(code) # I could make this code perform the same function without 
# the variable rule_1, but am keeping it to align with the instructions

## Rule2: equals the sum of all the digits of the user's input 
rule_2 = np.sum(code)

## Becauase this 'elimination and deciphering process' is nested, seperate 
# sections to describe each rule would not be realistic. Instead, I will
# decribe the function of each rule within this one section.
## Starting with rule_1, right off the bat it will eliminate any non-9 digit 
# numbers, so that my code[length] functions don't cause a runtime error.
if rule_1 == 9: # eliminates non-nine digit numbers
    ## Rule3 equals the 3rd digit of the user's input multiplied by the 
    # second, and then is subtracted by the first.  
    rule_3 = code[2]*code[1]-code[0]
    ## Rule4 is the 3rd digit of the user's input to the power of the second. 
    # div3 is the value calculated if the value of rule_4 is divisible by 3. 
    # notdiv3 has just the opposite function of div3. 
    rule_4 = code[2]**code[1]
    div3 = code[5]-code[4] # the calculation if rule 4 is divisble by 3 
    notdiv3 = code[4]-code[5] # the calculation if rule 4 is not divisble by 3 
    if (rule_2 % 2) == 0: # eliminates even integer sums of the array
        print("Decoy message. Sum is Even.")
    elif (rule_3 < 1) or (rule_3 > 7): # eliminates extraneous rule_3 instances
        print("Decoy message. Invalid rescue day.")   
    elif (rule_4 % 3) == 0 and div3 in range (1,8): # learned 'range' in class
        print("Rescued on",day_list[rule_3-1],"at the",place_list[div3-1])
    # the day to print is the value of rule_3 in the list day_list, minus one
    elif (rule_4 % 3) != 0 and notdiv3 in range (1,8):
        print("Rescued on",day_list[rule_3-1],"at the",place_list[notdiv3-1])
    else:
        print("Decoy message: Invalid rendevous point.")
else: 
    print("Decoy message: Not a nine-digit number.")
