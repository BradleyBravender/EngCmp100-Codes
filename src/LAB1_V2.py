## HSPECTRUM  Quantum Chemistry and the Hydrogen Emission Spectrum
#
# The periodic table is central to chemistry. According to Britannica,
# "Detailed understanding of the periodic system has developed along with
# the quantum theory of spectra and the electronic structure of atoms,
# beginning with the work of Bohr in 1913." In this lab assignment, a
# University of Alberta student explores the Bohr model's accuracy in
# predicting the hydrogen emission spectrum, using observed wavelengths
# from a US National Institute of Standards and Technology database.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Bradley Bravender (96%)
# Student CCID: ____
# Others: _____ (2%), ____ (2%)
# 
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
import matplotlib.pyplot as plt

## EXPERIMENT DATA
# This section establishes an array of data and sets 'n' equal to the length 
# of the data in this array.
data = [656.460,486.271,434.1692,410.2892,397.1198,389.0166,383.6485] # nm
nist = np.array(data)
n = len(nist)

## MODEL SETUP
# This section establishes variable values needed ro calculate the scale 
# factor, and Rydberg's constant, which is multiplied by this scale factor.
# Finally, it prints this value with the unit m⁻¹
proton_mass = 1.672621937e-27 # proton mass in kg
electron_mass = 9.1093837e-31 # electron mass in kg
fund_charge = 1.6021766e-19 # fundamental charge in coulombs
free_space = 8.8541878e-12 # permittivity of free space
planck = 6.6260702e-34 # Planck constant
light_speed = 2.9979246e8 # the 'speed of light' in a vacuum in m/s
scale_factor = proton_mass/(proton_mass+electron_mass)
rydberg = (scale_factor*(electron_mass*fund_charge**4) \
    /((8*free_space**2*planck**3*light_speed))) 
# r = the LHS of equation 1 in the pdf
print("Rydberg constant:", int(rydberg), "m"+chr(8315)+chr(185))

## SIMULATION DATA
# This section prompts the end user for an input, which input is then
# used to establish the x boundaries for the plot. 
nf = input("Final state (nf): ")
nf = int(nf)
ni = np.arange(nf+1,nf+n+1) # a set spanning from 3 (nf+1) to but 
# excluding 10 (2+6+1)
wavelength = ((1e9))/((rydberg*(1/(nf**2)-(1/(ni**2))))) # formula for 
# wavelength converted to nm 
plt.plot(ni,nist,'bx')
plt.plot(ni,wavelength,'r.') # x axis = ni, y axis = wavelength
# r. means the color red and the shape 'dot'
plt.title('Hydrogen Emission Spectrum') # axis titles explained to 
# me by a matplotlib development website article
plt.xlabel('Initial state (ni)')
plt.ylabel('Wavelength (nm)')
plt.legend(['NIST data', 'Bohr model'], loc="upper right") # legend syntax 
# explained to me by Max Dannish
plt.grid(True)
plt.show()

## ERROR ANALYSIS
# This section calculates the difference between the NIST and Bohr data sets, 
# and then plots this difference on a bar graph in magenta. It then finds the 
# absolute value of the distance between each corresponding value in both 
# arrays. Then, the maximum of these difference is found and printed as the
# variable "worst_case".
difference = nist - wavelength
plt.bar(ni, difference, color = "m") # the x axis is the array ni. The y axis
# is the difference between both data sets. The color of each bar is magenta.
plt.title('Hydrogen Emission Spectrum')
plt.xlabel('Initial state (ni)')
plt.ylabel('Wavelength (nm)')
plt.legend(['NIST-Bohr', 'Bohr model'], loc="lower right")
worst_case = (np.max(np.abs(difference))) # the absolute value of the 
# difference in each data pont is found, which allows np.max() to easily  
# identify the maximum difference between any two correlating data points.
print("Worst-case error: %.3f nm" % (worst_case))
