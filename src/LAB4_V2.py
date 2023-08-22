## TSPANALYZE  Geomatics and the Travelling Sales[person] Problem
#
# According to the ISO/TC 211, geomatics is the "discipline concerned
# with the collection, distribution, storage, analysis, processing, [and]
# presentation of geographic data or geographic information." Geomatics
# is associated with the travelling salesman problem (TSP), a fundamental
# computing problem. In this lab assignment, a University of Alberta
# student completes a Python program to analyze, process, and present
# entries, stored in a binary data file, of the TSPLIB, a database
# collected and distributed by the University of Heidelberg.
#
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
# numbers, adding to 100%, follow-up questions will be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#
import scipy.io as io
import numpy as np
import matplotlib.pyplot as plt
def main(): # The main function that excutes all others based on user input
    tsp = io.loadmat('tspData.mat', squeeze_me=True)
    tsp = np.ndarray.tolist(tsp['tsp']) # defining the value of tsp based on
    # the value of the file tspData.mat, and putting it into an array
    file = open('tspAbout.txt', 'r') # opens this file for reading purposes
    print(file.read())
    file.close()
    menu() # calls the function, menu
    while choice != 0:
        if choice == 1:
            tspPrint(tsp) # calls tspPrint if the user types 1
        elif choice == 2:
            tspLimit(tsp)
        elif choice == 3:
            tspPlot(tsp) # calls tspPLot if the user types 3
        menu()
## MENU takes no formal paramenters. Instead, when called, it defines choice
# as a global variable, and prints the menu screen. It prompts the user for 
# input, and screens that input to ensure that it is between 0 and 3. If the
# user's input is within those parameters, it returns that input as an integer.
def menu():
    global choice # as global, choice retains its value outside the function
    print()
    print("MAIN MENU")
    print("0. Exit program")
    print("1. Print database")
    print("2. Limit dimension")
    print("3. Plot one tour")
    print()
    choice = int(input("Choice (0-3)? ")) 
    while not (0 <= choice <= 3): # repeats prompt if the input doesn't match
        choice = int(input("Choice (0-3)? "))
    return choice # choice is the output of this function, and is an integer
## TSPPRINT takes the argument tsp, which is the data imported from tspData.mat
# It then prints the header for the data, and uses a for loop to go through 
# tsp and print it's data in the right columns, row by row.
def tspPrint(tsp):
    global dimension
    print()
    print("NUM  FILE NAME  EDGE TYPE  DIMENSION  COMMENT")
    for k in range(1,len(tsp)):
        name = tsp[k][0] # names are stored in the kth row, 0th column of tsp
        edge = tsp[k][5] # edges are stored in the kth row, 5th column of tsp
        dimension = tsp[k][3] # the above comments apply for dim. and comment
        comment = tsp[k][2]
        print("%3d  %-9.9s  %-9.9s  %9d  %s" # prints the k, name, edge, etc
              % (k,name,edge,dimension,comment))
## TSPPLOT takes the formal parameter tsp. It prompts the user for input and 
# stores that input in the variable num as an integer. It then stores the
# numth row, 5th column of tsp in the variable edge (stores tsp's 'edge'
# data in the variable edge), and the numth row into the variable tsp1. 
def tspPlot(tsp):
    num = int(input("Number (EUC_2D)? "))
    while not (0 < num <= len(tsp)-1): 
        num = int(input("Number (EUC_2D)? "))
    edge = tsp[num][5] # that number represents the rows of the array, and the 
    # the value in the column in that equals edge
    tsp1 = tsp[num]
    if edge == 'EUC_2D': # if the edge type is EUC_2D:
        plotEuc2D(tsp1[10],tsp1[2],tsp1[0]) # calls the function plotEUC2D
        # with the formal parameeters coord, comment, and name input
    else:
        print("Invalid (%s)!!!" % edge) # rejects edge types other than EUC_2D
## PLOTEUC2D takes the formal parameters coord, comment, and name. It prints
# the variable coord's length, and then creates a list for x-axis and y-axis
# values stored in the variable coord. It stored the first and last x and y 
# values into seperate lists. Then, a for loop that runs the length of the
# variable coord adds the correlating x and y values into the y and x axis 
# lists so that this data can be plotted against each other. Finally, this 
# function plots the data with corresponding labels and saves the plot as a
# .png file.
def plotEuc2D(coord, comment, name): # coord is a 52*2 array of x and y values
    print("See tspPlot.png")    
    xaxis = [] # the list I'll extract the coord x-axis values to
    yaxis = [] # the list I'll extract the coord y-axis values to
    betweenx = [coord[0][0], coord[-1][0]] # coord's first and last x values
    betweeny = [coord[0][1], coord[-1][1]] # coord's first and last y values
    for i in range(0,len(coord)): # extracts coord's coordinates into 2 lists
        xaxis.append(coord[i][0])
        yaxis.append(coord[i][1])
    plt.plot(xaxis,yaxis, marker='o') # the marker gives each data point a dot
    plt.title(comment)
    plt.xlabel('x-Coordinate')
    plt.ylabel('y-Coordinate')
    plt.plot(betweenx, betweeny, 'r')
    plt.legend([name], loc="lower center") # displays the data set's name
    plt.savefig('tspPlot.png') # saves the plot as tspPlot.png
    plt.show()
## TSPLIMIT recieves the input argument tsp, and then calls tspMinMax with the 
# argument tsp. tspMinMax returns the maximum dimensions in tsp, which this 
# function then prints. The function then prompts a user to enter in a value
# that is used to limit the dimenions of the tsp data set. If the user types
# a dimension outside of the max and min within tsp, it prompts them for a 
# limiting value again. If they do enter a dimension within tsp, then the 
# function goes through the dataset tsp, removing all rows with a dimension
# greater than the one the user sets. A while loop with an if and else 
# statement is used to meet this end, as a for loop would skip over values it
# pops. Lastly, the function then returns the value tsp. 
def tspLimit(tsp):
    tspMinMax(tsp)
    print("Min dimension:", minVal)
    print("Max dimension:", maxVal)
    valuelim = int(input('Limit value? '))
    while not (minVal <= valuelim <= maxVal): 
        valuelim = int(input('Limit value? '))
    i = 1 
    while i < len(tsp):   
        if tsp[i][3] > valuelim:      
            tsp.pop(i)   
        else:      
            i = i + 1
    return tsp
## TSPMINMAX This function declares minVal and maxVal as globals, as they are
# used as parameters in the function tspLimit(). It then makes the list 
# dimenValue, which is used to store all of tsp's dimensions values using a for
# loop. Then, the minimum and maximum value within this loop is saved in 
# respective variables, and lastly, the function returns the values of the
# variables, being minVal and maxVal
def tspMinMax(tsp):
    global minVal # Global so that tspLimit can access their values
    global maxVal
    dimenValue = [] # a list where tsp's dimensions will all be stored
    for i in range(1, len(tsp)): # starting at 1 to avoid the header row
        dimenValue.append(tsp[i][3]) # stores all of tsp's dimensions here
    minVal = min(dimenValue) # saves the smallest value of the list as minVal
    maxVal = max(dimenValue)
    return minVal, maxVal # returns the value of the min and max dimensions
main() # calls the main function
