# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 18:41:28 2018

@author: Michael Green, Xiaobo Chen
The University of Missouri-Kansas City

---

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

questions regarding implementation can be directed towards magwwc@mail.umkc.edu or chenxiaobo@umkc.edu

---

semantics: # marks a comment string, remove '#' and the line is activate. Also,
text surrounded by triple quotes is commented out (i.e. used for notes/the computer 
generally ignores everything therein).
    
If users wish to look into how the computer responds to each given command, consider
playing around with the 'IPython console' to the right. For example, after running
this script (requires lines 52-77 to be set up accordingly) the function 
'gaussian(x,a,b,c)' will be defined by the computer. try making a simple plot 
of a gaussian function by pasting the following into the prompt: 
    
    plt.plot(x, gaussian(x,1,10,1,0))

the IDE will use the plt. library to construct an (x, y) graph where y is the
gaussian output at each x point given the constants a, b, c. (x was defined on 
line 115). Next, try changing the a, b, and c variables to see how this changes
the function; for example:

    plt.plot(x, gaussian(x,2,20,2,0))

you'll notice that this curve is taller, farther to the right, and shallower, because
the function constants were all increased. This process of playing with the variables
to create different shaped gaussian functions is precisely what the computer is doing
in order to find the set of gaussian's which best fit the data (there are a few caveats 
to this, like the computer will find a local minimum and not necessarily the global,
but that's something covered in more detail in a course like Numerical Methods).     
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy.integrate import quad
from scipy.special import erf

# the raw string for the data file for analysis. 
# if the file is, for example, located on the desktop:

# Windows: file_string = r'C:\Users\1mike\Desktop\Sample GC 1 pt acetone 1 pt cyclohexane.csv'
# Linux: file_string = '/home/michael/Desktop/Sample GC 1 pt acetone 1 pt cyclohexane.csv'
# macOS: file_string = '/Users/1mikegrn/Desktop/Sample GC 1 pt acetone 1 pt cyclohexane.csv'

file_string = r'D:\Research\University of Missouri-Kansas City\Dr. Xiaobo Chen\Literature\Gas Chromatography and Data Functionalization in Python\Version 2; 2019-11-4\Supplemental Files\Sample GC data 1 pt acetone 1 pt cyclohexane.csv'

# reads the input file 

# if data file is in an excel file, use the following line: 
# master = pd.read_excel(file_string).to_numpy()

# if using a '.csv' file, use the following line:
data_set = pd.read_csv(file_string).to_numpy()

# initial guess for gaussian distributions to optimize [height, position, width, skew].
# if more than 2 distributions required, add a new set of [h,p,w,s] initial parameters 
# for each new distribution. New parameters should be of the same format for 
# consistency; i.e. [h,p,w,s],[h,p,w,s],[h,p,w,s],... etc. A 'w' guess of 1 and 
# an 's' guess of 0 are typically a sufficient estimations.

# It should be noted that the parameters don't fit the strict definitions as defined
# with a symmetric gaussian because the error function requires a certain level of 
# interplay with the standard distribution which is a function of the 'c' parameter.
# you can discover the relationships yourself by comparing the symmetric gaussian to
# the asymmetric; for example, the amplitude of the exponential in a symmetric gaussian
# is defined strictly as a function of the constant 'a'. What takes the place of the
# constant 'a' here in the asymmetric function? 
# (the parameter (a / (c * np.sqrt(2 * np.pi))))

initials = [
    [6.5, 13, 1, 0], 
    [4.5, 19, 1, 0]
]

# --- No changes below this line are necessary ---

# determines the number of gaussian functions to compute from the initial guesses
n_value = len(initials)

# defines a typical gaussian function, of independent variable x,
# amplitude a, position b, width parameter c, and erf parameter d.
def gaussian(x,a,b,c,d):
    amp = (a / (c * np.sqrt(2 * np.pi)))
    spread = np.exp((-(x - b) ** 2.0) / 2 * c ** 2.0)
    skew = (1 + erf((d * (x - b)) / (c * np.sqrt(2))))
    return amp * spread * skew

# defines the expected resultant as a sum of intrinsic gaussian functions
def GaussSum(x, p, n):
    gs = sum(
        gaussian(x, p[4*k], p[4*k+1], p[4*k+2], p[4*k+3]) 
        for k in range(n)
    )
    return gs

# defines a residual, which is the  reducing the square of the difference 
# between the data and the function
def residuals(p, y, x, n):
    return y - GaussSum(x,p,n)

# executes least-squares regression analysis to optimize initial parameters
cnst = leastsq(
    residuals, 
    initials, 
    args=(
        data_set[:,1],
        data_set[:,0],
        n_value
        )
    )[0]

# integrates the gaussian functions through gauss quadrature and saves the 
# results to a dictionary.

areas = dict()

for i in range(n_value):
    areas[i] = quad(
            gaussian,
            data_set[0,0],      # lower integration bound
            data_set[-1,0],     # upper integration bound
            args=(
                cnst[4*i],
                cnst[4*i+1],
                cnst[4*i+2], 
                cnst[4*i+3]
            )
        )[0]
    
# defines the independent variable. 
x = np.linspace(0,40,200)

# visualization block; creates and formats a figure variable to place the data 
# in.
fig, ax = plt.subplots()

#sets the axis labels and parameters.
ax.tick_params(direction = 'in', pad = 15)
ax.set_xlabel('time / s', labelpad = 20, fontsize = 15)
ax.set_ylabel('Intensity / a.u.', labelpad = 20, fontsize = 15)

#plots the first two data sets: the raw data and the GaussSum.
ax.plot(data_set[:,0],data_set[:,1], 'ko')
ax.plot(x,GaussSum(x,cnst, n_value))

# adds a plot of each individual gaussian to the graph.
for i in range(n_value):
    ax.plot(x, gaussian(x, cnst[4*i], cnst[4*i+1], cnst[4*i+2], cnst[4*i+3]))

# creates a list of titles for each data set.
ledger = ['Data', 'Resultant']
for i in range(n_value):
    ledger.append('Area = ' + str(round(areas[i], 3))) 

#adds the ledger to the graph.
ax.legend(ledger)

# final formatting of graph, and show the picture.
plt.tight_layout()
plt.show()