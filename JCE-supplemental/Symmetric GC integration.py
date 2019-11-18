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
text surrounded by triple quotes is a milti-line string (typically used 
for notes as if the string is not assigned to an operator, the computer 
generally ignores everything therein).
    
If users wish to look into how the computer responds to each given command, 
consider playing around with the 'IPython console' to the right. For example,
after running this script (requires lines 51-68 to be set up accordingly) 
the function  'gaussian(x,a,b,c)' will be defined in the computer. Try making 
a simple plot of a gaussian function by pasting the following into the prompt: 
    
    plt.plot(x, gaussian(x,1,10,1))

the IDE will use the matplotlib.pyplot library to construct an (x, y) graph 
where y is the gaussian output at each x point given the constants a, b, c. 
(x was defined on line 104). Next, try changing the a, b, and c variables to 
see how this changes the function - for example:

    plt.plot(x, gaussian(x,2,20,2))

you'll notice that this curve is taller, farther to the right, and broader, 
because the function constants were all increased. This process of playing 
with the variables to create different shaped gaussian functions is precisely 
what the computer is doing in order to find the set of gaussians which best 
fit the data (there are a few caveats to this, like the computer will find 
a local minimum and not necessarily the global, but that's something 
covered in more detail in a course like Numerical Methods).     
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy.integrate import quad

# the raw string for the data file for analysis. 
# if the file is, for example, located on the desktop:

# Windows: file_string = r'C:\Users\1mike\Desktop\Sample GC 1 pt acetone 1 pt cyclohexane.csv'
# Linux: file_string = '/home/michael/Desktop/Sample GC 1 pt acetone 1 pt cyclohexane.csv'
# macOS: file_string = ‘/Users/1mikegrn/Desktop/Sample GC 1 pt acetone 1 pt cyclohexane.csv’

file_string = r'D:\Research and Teaching\University of Missouri-Kansas City\Dr. Xiaobo Chen\Literature\Gas Chromatography and Data Functionalization in Python\Version 2; 2019-11-4\Supplemental Files\Sample GC data 1 pt acetone 1 pt cyclohexane.csv'

# reads the input file 

# if data file is in an excel file, use the following line: 
# master = pd.read_excel(file_string).to_numpy()

# if using a '.csv' file, use the following line:
master = pd.read_csv(file_string).to_numpy()

# initial guess for gaussian distributions to 
# optimize [height, position, width]. If more than 2 distributions required, 
# add a new set of [h,p,w] initial parameters to 'initials' for each new 
# distribution. New parameters should be of the same format for consistency; 
# i.e. [h,p,w],[h,p,w],[h,p,w]... etc. A 'w' guess of 1 is typically a 
# sufficient estimation.

initials = [4.5, 13, 1], [2.5, 19, 1]

# --- No changes below this line are necessary ---

# determines the number of gaussian functions 
# to compute from the initial guesses
n = len(initials)

# data matrix
M = np.array(master)

# defines a typical gaussian function, of independent variable x,
# amplitude a, position b, and width parameter c.
def gaussian(x,a,b,c):
    return a*np.exp((-(x-b)**2.0)/c**2.0)

# defines the expected resultant as a sum of intrinsic gaussian functions
def GaussSum(x, p):
    return sum(gaussian(x, p[3*k], p[3*k+1], p[3*k+2]) for k in range(n))

# defines condition of minimization, called the resudual, which is defined
# as the difference between the data (y) and the model'func(x,p)'
def residuals(p, y, x):
    return y - GaussSum(x,p)

# executes least-squares regression analysis to optimize initial parameters
cnst = leastsq(residuals, initials, args=(M[:,1],M[:,0]))[0]

# integrates the gaussian functions through gauss quadrature and saves the 
# results to a list. This is an example of whats called a list comprehension:
# for loops are notoriously slow in python, so the python developers created
# this comprehension protocol for faster execution.
areas = [quad(gaussian,M[0,0],M[M.shape[0]-1,0],
        args=(cnst[3*i], cnst[3*i+1], cnst[3*i+2]))[0] 
        for i in range(n)]

# defines the independent variable. 
x = np.linspace(0,40,200)

# visualization block; creates and formats a figure variable to 
# place the data in.
fig, ax = plt.subplots(dpi = 100)

#sets the axis labels and parameters.
ax.tick_params(direction = 'in', pad = 15)
ax.set_xlabel('time / s', labelpad = 20, fontsize = 15)
ax.set_ylabel('Intensity / a.u.', labelpad = 20, fontsize = 15)

# plots the first two data sets: the raw data and the GaussSum.
ax.plot(M[:,0],M[:,1], 'ko')
ax.plot(x,GaussSum(x,cnst))
# adds a plot of each individual gaussian to the graph.
for i in range(n):
    ax.plot(x, gaussian(x, cnst[3*i], cnst[3*i+1], cnst[3*i+2]))

# creates a list of titles for each data set.
ledger = ['Data', 'Resultant']
for i in range(n):
    ledger.append(str(round(cnst[3*i+1], 2)) + '$e^{(x-' + str(round(cnst[3*i], 2)) + ')^2 / ' + str(round(cnst[3*i + 2], 2)) + '^2}$' + ' \n Area = ' + str(round(areas[i], 3))) 

#adds the ledger to the graph.
ax.legend(ledger)

# final formatting of graph, and show the picture.
plt.tight_layout()
plt.show()
