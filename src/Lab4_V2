# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Bradley Bravender (100%)
# Student CCID: _____
# Others: none
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
import matplotlib.pyplot as plt
import numpy as np
print('Version 1 - Solution')
# ------------Students edit/write their code below here--------------------
## SAVING CALCULATION. this section calculates the accumulated balance over the
# course of 216 months. It saves this data as a list. Then, it scales this list
# to range over the span of 0 to 18. 
year = [] # this list will serve as my x-axis on the graph
month_cost = [] # to provide values for year 0 on the graph
old_balance = 2000
for i in range(1,216): # b/w months 1 to 215 incl. Month 216 is not compounded.
    old_balance = (193/192)*old_balance + 200
    month_cost.append(old_balance) # adds the balance as a new list entry
    year+=[i/12] # this list shrinks the i into the right shape [0,215]
## TUITION CALCULATION. This section calculates the tuition change for each 
# department, and stores the tuiution per department per year in correlating 
# lists. Then, the sum of these lists are calculated using a for loop.
arts = 5550 # the initial cost of each program per year
arts_sum = 0
sci = 6150
sci_sum = 0
eng = 6550
eng_sum = 0
arts_tui = []
sci_tui = []
eng_tui = []
for i in range(21): # between the years 1 to 22 inclusive
    arts = (107/100)*arts # the arts calculation
    arts_tui.append(arts)
    sci = (107/100)*sci # the science calculation
    sci_tui.append(sci)
    eng = (107/100)*eng # the engineering calculation
    eng_tui.append(eng)
for i in range(4):
    arts_sum += arts_tui[17+i] # calcuating the sum of each list
    sci_sum += sci_tui[17+i]
    eng_sum += eng_tui[17+i]
## PLOT. This section prints the values specified in the rubric, and plots the
# related data. Program cost is given the same shape as the month_cost list
print("The savings amount is $%.2f" % (old_balance))
print("The cost of the arts program is $%.2f" % arts_sum)
print("The cost of the science program is $%.2f" % sci_sum)
print("The cost of the engg program is $%.2f" % eng_sum)
plt.plot(year, month_cost) # x-axis: year, y-axis: the month_cost list
plt.plot(np.ones(19)*arts_sum) # Here I'm converting integers to arrays
plt.plot(np.ones(19)*sci_sum) # These arrays theb have the right shape to graph
plt.plot(np.ones(19)*eng_sum)
plt.axis([0, 18, 0, 100000]) # making the range in the scope asked for
plt.xticks(np.arange(0, 19, 1.0)) # making the x-axis increment annually
plt.title('Savings vs Tuition') # my  plot title
plt.xlabel('Years')
plt.ylabel('Amount $')
plt.legend(['Saving Balance', 'Arts', 'Science', 'Engineering'], \
           loc="lower right")
plt.show
## SOLUTION 2. This section asks the user to choose a program. It determines if
# they can afford it, and what they need to contribute monthly to do so.
print() # giving a space between Solution 1 and 2 in the console
print("Version 2 - Solution")
increment = 1 # the monthly amount contributed will start at $1
new_balance = 2000 # new_balance refers to the bank balance in solution 2
tuition = [arts_sum, sci_sum, eng_sum] #the program costs are in list form
response = ["Fortunately, you", "Unfortunately, you do not", \
            "Unfortunately, you do not", "arts", "science", "engineering"]
# storing responses in a list simplifies my code by avoiding any if statements
opt = int(input('Enter a program: 1. Arts, 2. Science, 3. Engineering: ')) 
while (new_balance < tuition[opt-1]): # input value correlates w/ tuition list
   new_balance = 2000 # I needed to specify it's initial value for each run
   for i in range(215): 
       new_balance = (193/192)*new_balance + increment # same calc as in Sol 1
   increment+=1 # if balance isn't enough, increase increment and try it again
print(response[opt-1],"have enough saved for the",response[opt+2], "program")
print("The optimal monthly contribution amount is $%.0f" % (increment-1))  
