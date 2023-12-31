## PERIHELION  Mercury's perihelion precession and general relativity
#
# In this lab assignment, a student completes a Python program to test with
# data an accurate prediction of Einstein’s theory, namely the perihelion
# precession of Mercury. Mercury’s orbit around the Sun is not a stationary
# ellipse, as Newton’s theory predicts when there are no other bodies. With
# Einstein’s theory, the relative angle of Mercury’s perihelion (position
# nearest the Sun) varies by about 575.31 arcseconds per century.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Bradley Bravender (92%)
# Student CCID: _____
# Others: _____ (4%), _____ (4%)
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
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import csv

## The main function inputs the string 'horizon_results' into the loadata
# function, which uses this argument to extract the data rows of the file, 
# which it returns to the main function as the variable 'data'. This variable
# is then passed as the argument to the function 'locate', which calculates the
# local minimum magnitudes of distance from the x, y, and z coordinates of 
# 'data', and then returns each line that contains the local distance minimums
# (perhelions) to a new list. This new list of perhelions is then inputted as
# an argument in the select function, along with the y step and the tuple of 
# month dates. The select function then refines the list of perhelion data, 
# returning a list of data from each 50th year starting from 1800 for the 
# months of January to March. This data is then passed to the refine function,
# which uses each line to open a file of each row's date, which contains data
# generated by the minute instead of by the day like the original file had.
# these new lists are processed using the same formatting functions as
# previously described, and then this final list of extremely accurate data is
# passed to the to the makeplot function in order to graph it, and the savedata
# function in order to save is as a .csv file.
def main():
    data = loaddata('horizons_results') # invokes the loaddata function with 
    # the filename
    data = locate(data) # Locates each instance of a Perihelia
    data = select(data,50,('Jan','Feb','Mar')) # refines te list of perihelia
    data = refine(data,'horizons_results')
    makeplot(data,'horizons_results')
    savedata(data,'horizons_results')

## loaddata is called from the main function with the argument being the name
# of the file that loaddata opens, with the intent to read it. loaddata saves
# the file it reads as the list 'lines', and then closes the file. It then 
# sets the variable noSOE to true, and creates an empty list called 'data'.
# a for loop within loadata iterates through the list 'lines' line by line. An
# initial if statement in this loop tests if the current line is the string
# $$EOE. If it isn't, then the loop repeats until it detects the line with the
# string $$EOE. Once that string is detected, the function knows that the data
# part of the file been read has been reached, so it closes the if statement
# and then sends each line of the file to the the function str2dict,
# which returns the data preformatted, allowing loadata to then stores it in an
# appended list named 'data'. It also provides a back up option in case the 
# string %%EOE is never detected. Finally, it returns this new list of 
# extracted data back into the main function
def loaddata(filename):
    file = open(filename+'.txt','r') # Opens the file name passed, for reading
    lines = file.readlines() # lines is a list containing all entries
    file.close()
    noSOE = True
    num = 0
    data = []
    for line in lines: # iterating through the list line by line
        if noSOE: # if true:
            if line.rstrip() == "$$SOE": # if when all spaces are stripped,
            # the line equals the string $$SOE, we know that the program has
            # entered the data part of the list lines, and so once $$SOE is
            # detected, the if gets functionally 'removed'
                noSOE = False
        elif line.rstrip() != "$$EOE": # if the stripped line does not equal
            num = num+1
            if num % 10000 == 0:
                print(filename,":",num,"line(s)")
            datum = str2dict(line) # sends the data to str2dict to format it
            data.append(datum) # appends the formated data to the list 'data'
        else:
            break
    if noSOE: # if $$EOE is never detected in the file text
        print(filename,": no $$SOE line")
    else:
        print(filename,":",num,"line(s)")
    return data # returns the list of formatted data

## str2dict is called in the function loaddata with the argument 'line', which 
# is one line from the file. str2dict extracts the numeric date, the string 
# date, and the 3D coordinates from each line passed to it, and converts them 
# into their respective data types. Then, it returns these three arguments in 
# the form of a dictionary.
def str2dict(line): # the input argument is the file line passed to it
    string = line.split(",") # splits the line at every comma, and stores the
    # resulting elements as a list
    numdate = float(string[0].strip()) # takes the first element, strips extra
    # spaces from it, and converts it to a float value
    strdate = str(string[1][6:17]) # extracts the chharacter from 6-17 (which
    # is th string date) and saves it as strdate 
    x = float(string[2].strip()) # saves the x coordinates as a float
    y = float(string[3].strip()) # saves the y coordinates as a float
    z = float(string[4].strip()) # saves the z coordinates as a float
    return {'numdate':numdate,'strdate':strdate, 'coord':(x,y,z)}
# the numdate is the barycentric julian date, a date system used in astronomy
# (see https://ssd.jpl.nasa.gov/tools/jdc/#/jd)

## locatedata is called in main after loadata returns the formatted list 
# 'data'. It creates a list called dist and fills it with an array of the
# magnidtude of vector lengths created by the x, y and z coord values in data.
# It also creates and populates a second list named 'data2' that it extracts 
# values of specific conditions from, from the dist list. Finally, it returns 
# data2 to the main function.
def locate(data1): 
    dist = [] # Vector lengths
    for datum in data1: # datum is the singular form of data i.e. 'for each 
    # element of data in data1:'
        coord = np.array(datum['coord'])
        dot = np.dot(coord,coord)
        dist.append(np.sqrt(dot)) # dist is an array where every entry equals
        # sqrt(x**2 + y**2 + z**2), which is the magnitude of 3 dimensional
        # distance
    data2 = []
    for k in range(1,len(dist)-1):
        if dist[k] < dist[k-1] and dist[k] < dist[k+1]: # chooses the smallest
        # relative distances away from the earth out of the data set
            data2.append(data1[k])
    return data2 # returns data2 to main

## the select function is called in the main function with the arguments data,
# ystep, and the string tuple of months Jan, Feb, and Mar. It selects data 
# from every 50th year starting from 1800, and when that data is within the 
# the first three months of the year, it appends that data to the list
# updatedData, which will be graphed in a different function once returned.
def select(data,ystep,month): # data = the list of formatted data,
# ystep = 25, Month = the strings Jan, Feb, and March
    updatedData = [] # a new, empty list to add the selected data list values
    for i in range (len(data)): # iterates throughout the entire length of data
        if int(data[i]['strdate'][0:4])%ystep == 0 and \
        data[i]['strdate'][5:8] in month:
            # In the ith element of data, in the 'strdate' sub element, take 
            # the year (characters 0-4) and test if it's divisible by 25. If
            # this condition is met, and the month in data is either the string
            # Jan, Feb, or Mar, then add this line of data to the new list
            updatedData.append(data[i])
    return updatedData # return this summarized version of the list 'data' to 
# main to be graphed.

## the makeplot fucntion takes the final list of data and the filename as its
# arguments. It passes data to the function precess, which extracts specific 
# sub lists generated from the data list, and performs computations on some of
# the data before returning three arguments to the makeplot function (the 
# numerical date, string date, and arcseconds). This function the plots the
# precession in arcseconds against the perhelion date, and saves it as a png.
def makeplot(data,filename):
    (numdate,strdate,arcsec) = precess(data)
    plt.plot(numdate,arcsec,'bo')
    plt.xticks(numdate,strdate,rotation=45)
    add2plot(numdate,arcsec)
    plt.savefig(filename+'.png',bbox_inches='tight') # saves the plot as a png
    plt.xlabel('Perihelion Date')
    plt.ylabel('Precession (arcsec)')
    plt.show()

## precess is called from the makeplot function with the argument newdata, which
# is the final list of data. It extracts the numerical and string dates of
# newdata into seperate lists, and performs linear algebra calculations on the
# coord tuple of newdata to calculate the arcseconds of every row of data. 
# It returns the numerical and string dates, and the arcseconds list to the 
# makeplot function.
def precess(newdata):
    numdate = [] # generates three new lists
    strdate = []
    arcsec = []
    v = np.array(newdata[0]['coord']) # Reference (3D)
    for datum in newdata:
        u = np.array(datum['coord']) # Perihelion (3D)
        ratio = np.dot(u,v)/np.sqrt(np.dot(u,u)*np.dot(v,v))
        if np.abs(ratio) <= 1:
            angle = 3600*np.degrees(np.arccos(ratio))
            numdate.append(datum['numdate'])
            strdate.append(datum['strdate'])
            arcsec.append(angle)
    return (numdate,strdate,arcsec)

## the add2plot function is called from the makeplot function, and it has the
# input arguments numdate and actual. It calculates the line of best fit of
# this data using regression, and plots the title and legend on the graph.
def add2plot(numdate,actual):
    r = stats.linregress(numdate,actual)
    bestfit = []
    for k in range(len(numdate)):
        bestfit.append(r[0]*numdate[k]+r[1])
    plt.plot(numdate,bestfit,'b-')
    plt.legend(["Actual data","Best fit line"])
    plt.title("Slope of best fit line: %.2f arcsec/cent" % (100*r[0]*365.25))
    # Displays the arcseconds per century

## The sdvedata function receives the filename and the finished data arguments,
# which is uses to save the data as a .csv file. As a final function, it does
# not return any values.
def savedata(data,filename):
    table = [['NUMDATE','STRDATE','XCOORD','YCOORD','ZCOORD']] # table is a
    # list of data with these headers
    row = []
    for i in range (len(data)):
        numdate = data[i]['numdate']
        strdate = data[i]['numdate']
        xcoord = data[i]['coord'][0]
        ycoord = data[i]['coord'][1]
        zcoord = data[i]['coord'][2]
        row = ['%.6f' % numdate, '%.6f' % strdate, '%.6f' % xcoord, 
                '%.6f' % ycoord, '%.6f' % zcoord]
            # iterates through the data list and saves each entry as a row
            # formatted to be exported as a .csv file
        table.append(row)
    with open(filename+'.csv', 'w', newline='') as line: # saves the file as
    # it's preset filename, and 'opens' it with the intent to write to it.  
        writer = csv.writer(line)
        # uses the csv library to write each line of the formatted list of data
        # as a row in the .csv file
        writer.writerows(table) # writes the full table to the file
    line.close()

# refine takes the data after it has been filtered through many of the 
# functions before it in main, and uses the remaining rows of data, which are
# of specific days of perhelion occurance, to open correlating files of the
# same dates, but of data down to the minute, which it feeds through the 
# loaddata and locate functions to refine it into usable data where the exact
# minute of the perhelions are located. It essentially appends this more 
# precise data to the variable refinedData, which is a list with each row being
# a dict. Finally, it returns refinedData to main, to be graphed and saved
# as a .csv
def refine(data,filename):
    refinedData = []
    for i in range (len(data)):
        lines = loaddata(filename+'_'+str(data[i]['strdate']))
        lines = locate(lines)
        refinedData = refinedData + lines # appends each dict row to this
        # existing list
    return refinedData
    # open each file individually, load it's data into select, append the 
    #parahelis into a new list that gets sent to plot and the csv file
    # the original file is daily, the more accruate are by the minute
    
main()

