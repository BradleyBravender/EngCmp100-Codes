## CORONASIMULATE  Simulate coronagraph and Gerchberg-Saxton algorithm
#
# A simulation of a coronagraph and the Gerchberg-Saxton algorithm, in the
# context of NASA's Roman Space Telescope, developed to help teach ENCMP
# 100 Computer Programming for Engineers at the University of Alberta. The
# program saves output figures to PNG files for subsequent processing.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Bradley Bravender (95%)
# Student CCID: _____
# Others: _____ (4%), _____ (1%)
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
import matplotlib.pyplot as plt
import numpy as np

def main():
    im = loadImage('300_26a_big-vlt-s.jpg')
    (im,Dphi,mask) = opticalSystem(im,300)
    (images,errors) = gerchbergSaxton(im,10,Dphi,mask)
    saveFrames(images,errors)

## loadImage is called from the function 'main' with the input argument being 
# the filename of the image to load. The image is read and its RGB values are
# divided by 255, which normalizes them. The shape is (750, 800, 3), so the if 
# statement then takes the corresponding sums of all of its pixel values for 
# its red, green and blue colors, and divides by 3 to give the average RGB
# value to 'im'. Lastly, it sets any value in im below 0 to 0, and any value
# above 1 to 1, and returns the (750,800) im value to main.
def loadImage(name):
    im = plt.imread(name)/255
    if len(im.shape) > 2:
        im = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3
    im[im < 0] = 0
    im[im > 1] = 1
    return im

## opticalSystem is called from the main function, with the arguments 'im' 
# which is the 'image', and the width, which equals 300. occultCirlce is 
# invoked with the arguments im and width. occultCirlce generates a cirlce with
# a diameter of 300 pixels in the center of im, and an array with the same 
# shape of im, but whereever the circle of 0's exist in im, the value 'True' 
# would exist in mask (and 'False' would exist in all other pixels of mask)
# Thus, occultCirlce returns a 2 dimensional tuple where the first element is
# im and the second is mask. Then, a random value is generated with the seed
# value '12345' and assigned to the variable rng, while another random value is
# generated with the seed value im.shape, which is a (750,800) tuple. Next,
# the dft2 function is invoked with the argument imr. dft2 returns a 2 element
# tuple, where the first element is the amplitude, and the second element is 
# the phase of the @D Fourier transform of the image im. Finally, the function 
# idft2 is invoked with the arguments IMa (the amplitude) and IMp-Dphi. idft2
# returns the grayscale image im. opticalSystem returns the image im, Dphi
# (the true phase abberation), and the image 'mask'.
def opticalSystem(im,width):
    (im,mask) = occultCircle(im,width)
    (IMa,IMp) = dft2(im)
    rng = np.random.default_rng(12345)
    imR = rng.random(im.shape)
    (_,Dphi) = dft2(imR)
    im = idft2(IMa,IMp-Dphi)
    return (im,Dphi,mask)

## occultCircle is invoked in the opticalSystem function, with the arguments
# im and width. im is a 750*800 array of floats, and width is the number 300.
# First, the image 'mask' is created with the same shape as im, and where every
# value is 'False'. The radius is half of the value of width, and the center
# of im is calculated by dividing the horizontal and vertical components of
# width by 2. Then, a for loop iterates through the horizontal values, and 
# another for loop nested instead iterates through im's vertical values. Within
# this for loop, if the magnitude of the value from the center of the image is
# less than the radius, then the value is assigned 0 and the corresponding 
# value in mask is assigned the value 'True'. Then, im and mask are returned to 
# opticalSystem.
def occultCircle(im, width): # width = 300 
    mask = np.full((im.shape), False, dtype=None)
    radius = width/2 # radius of the circle
    center_x, center_y = im.shape[0] // 2, im.shape[1] // 2 # center coords
    for i in range(im.shape[0]): # Iterate over every element in the array
        for j in range(im.shape[1]):
            dist = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
            # Calculates the distance from the center to the current element
            if dist <= radius:
                im[i][j] = 0 
                mask[i][j] = True
    return (im,mask)
    
# (IMa,IMp) = dft2(im) returns the amplitude, IMa, and phase, IMp, of the
# 2D discrete Fourier transform of a grayscale image, im. The image, a 2D
# array, must have entries between 0 and 1. The phase is in radians.
def dft2(im):
    IM = np.fft.rfft2(im)
    IMa = np.abs(IM)
    IMp = np.angle(IM)
    return (IMa,IMp)

# im = idft2(IMa,IMp) returns a grayscale image, im, with entries between
# 0 and 1 that is the inverse 2D discrete Fourier transform (DFT) of a 2D
# DFT specified by its amplitude, IMa, and phase, IMp, in radians.
def idft2(IMa,IMp):
    IM = IMa*(np.cos(IMp)+1j*np.sin(IMp))
    im = np.fft.irfft2(IM)
    im[im < 0] = 0
    im[im > 1] = 1
    return im

## gerchbergSaxton is invoked from the main function. It recieves four inputs: 
# im, which is a 750*800 array of floats, maxIters, which is the number 10,
# Dphi, the true phase abberation (a 750*401 array of floats), and mask, which
# is an image with a center circle of the values 'TRUE'. This function first 
# invokes the function dft2 with the argument im, which is returned as a 1*2
# tuple, where both elements, saved as IMa and IMp, are 750*401 arrays of 
# floats. Then, it creates an empty list called images, and an empty list 
# called errors. Finally, it runs a for loop with the range maxIters+1 (which 
# equals 11). Within this loop, it prints which iteration is occuring out of 
# the limit 11 iterations. Next, it invokes the function idft2 with the 
# arguments IMa (the 750*401 array), and the second argument, which is a linear
# equation with the 'y-intercept' at IMp (the other 750*401 array of floats), 
# and the slope Dphi/maxIters, being multiplied by the 'x' variable k (which 
# iterates from 0 - 11). Therefore, at k = 0, the second argument equals IMp, 
# and at k = max, k/maxIters equals one, so the second argument at k max is 
# simply Dphi + IMp. Each of these iterations is saved as an appended element 
# in the list images. Within this same for loop, occultError is called with the
# arguments im and mask. occultError returns the sum of values in im which 
# correlate with the same positions as all the values of 'mask' that equal
# 'True', an these values are appended to the list 'errors'. finally, im and 
# errors are returned to the main function.
def gerchbergSaxton(im,maxIters,Dphi,mask):
    (IMa,IMp) = dft2(im)
    images = []
    errors = []
    for k in range(maxIters+1):
        print("Iteration %d of %d" % (k,maxIters))
        im = idft2(IMa,(Dphi/maxIters)*k+IMp) # IMp is phase
        images.append(im)
        error = occultError(im,mask)
        errors.append(error)
    return (images,errors)

## occultError is called from the function gerchbergSaxton with the arguments
# im and mask. It then indexes throughout all the horizontal and vertical 
# components of im, if the corresponding values in mask are True, then it takes
# the value of im, squares it, adds it to error, and assigns the total value 
# to error. Lastly, it returns errr to gerchbergSaxton. 
def occultError(im,mask):
    error = 0
    for i in range(im.shape[0]): # Iterate over every element in the array
        for j in range(im.shape[1]):
            if mask[i][j] == True:
                error = error + (im[i][j])**2 
    return error
    # go through mask, make list of all indexes where its true,
    # go thorugh im, make list of every location

## saveframes is the last function called in the main function. It takes the 
# argument 'images', which was the list returned from the gerchbergSaxton
# function, and 'errors', which is the list of errors. images is a list of 
# eleven 'pictures', stored as 750*800 float arrays. This function first 
# creates a 1*3 tuple. The first element of this tuple is the shape of the 0th
# element of the first row in 'images', which is equal to 750. The second 
# element of this tuple is the shape of the first element of the first row in 
# 'images', which is equal to 800. The final element of this tuple is '3', 
# which gives a tuple of (750,800,3), allowing us to save a 3-digit RGB value 
# for each of the pictures in 'images'. Next, the maximum error in the list
# errors is assignd to the variable maxErrors. The variable 'image' is then 
# assigned a float array of zeroes with the shape of the tuple 'shape' that was
# described above. maxIters is assigned the value 10, and is used as the range 
# for the following for loop. This for loop iterates through images' eleven 
# pictures, saving each of these in the # Red (0), Green (1), and Blue(2) 
# columns of the 3D array image. It also plots the list of errors from 0 to the
# error's index position 'k+1' overtop of the image im. It sets the parameters
# for positions and aspects of the graphics so that both images
# are scaled correctly. Finally, the function prints a title, outputs the 
# respective image (and saves it as a png), and turns the axis label off. As a 
# final function, it does not return anything.
def saveFrames(images,errors):
    shape = (images[0].shape[0],images[0].shape[1],3) # the images array has 11
    # elements, and each element is a 750*800 array. Thus, images[0] calls
    # the 0th element, and within this element, shape[0] calls the shape of the
    # row (being [0], while columns being [1]. Thus this equals 750
    maxErrors = max(errors)
    image = np.zeros(shape,images[0].dtype)
    maxIters = len(images)-1
    for k in range(maxIters+1): # maxIters = 10   
        plt.plot(errors[0:k+1], 'r')
        plt.xlabel('Iteration')
        plt.ylabel('Sum Square Error')
        image[:,:,0] = images[k] # because the same value is being saved for
        # each pixels R, G and B values, the resulting color is a shade of grey
        image[:,:,1] = images[k] 
        image[:,:,2] = images[k]
        plt.imshow(image, extent=[0,maxIters,0,maxErrors])
        plt.gca().set_aspect(maxIters/maxErrors)
        plt.title('Coronagraph Simulation')
        plt.savefig('coronagraph'+str(k)+'.png')
        plt.show()

main()
