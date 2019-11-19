"""
:code:`help_text.py`
====================

just a bunch of text which renders in the help popup - rst option in kivy is
buggy, check back to see if/when it's working so this can be done nicer.

"""

def texts(arg):
    """

function called from GUI - returns multi-line string to be rendered by the app.

                    ---------------------------------------
::

    :param arg:     (str)

text parameter argument supplied by the GUI/button press.

                    ---------------------------------------
::

    :return:        (str)

requested text associated with the arg.
    """
    if arg == 'ID':
        return r'''
        Input Data can be placed into either a Microsoft Excel 
        (.xlsx) file, a comma-separated .csv file, or a tab-separated .csv 
        file, as a X by 2 array, using columns (1, 2) for the (x, y) data 
        columns derived from experiment. Text above and below the data will 
        be automatically filtered out by the program. There is no restriction 
        on the number of rows utilized for calculation. Locate the file using 
        the built-in file explorer and click 'select'. 
       '''

    elif arg == 'IV':
        return r'''
        Once the GC data has been loaded into the graphing window, click the 
        (x, y) points where you would like to 'guess' there is a gaussian 
        distribution. The program will automatically attempt fit one gaussian 
        distribution to the data set for each point which is picked on the 
        graphing canvas. The points do not need to be selected perfectly, 
        though there is a higher probability of finding the global minimum 
        as your guess is made more accurate. Should you wish to delete any 
        points, the button 'clear last object' will remove the most recently 
        placed point from the graph. If you wish to start over, you can clear 
        the graph entirely by selecting 'clear graph'.
        '''

    elif arg == 'OG':
        return r'''
        Once the program is finished deconvoluting the data set a graph will 
        appear showing the deconvoluted gaussian distributions and the 
        associated integral areas.
        '''

    elif arg == 'OD':
        return r'''
        Once the deconvolution is finished, the graph options window will open 
        allowing the user to adjust the graph as necessary using the built-in 
        buttons which move the plot Up/Down and Left/Right, as well as 
        Expand/Contract along both axes. Adjusting the 'Sensitivity' slider 
        adjusts the magnitude to which each button press adjusts the graph. 
        The 'Center' button returns the graph to the space which the imported 
        data occupies. Once the graph looks as desired, press the 'Export graph 
        to Image' button to save the graph as a .png image. This image will be 
        saved to the file location of the input data. The user can also export 
        the graph data to an excel file by pressing 'Export data to Excel'.  
        '''

    elif arg == 'C':
        return r'''
        The user has the option of selecting between two fitting 
        functions, a Symmetric Gaussian function and an Asymmentric Gaussian 
        function The asymmetric gaussian uses the erf() to allow for 
        distribution skewing.
        '''

    elif arg == 'ACK':
        return r'''
        Support for this research comes from the U.S. National Science 
        Foundation under Federal Research Grant DMR-1609061, the School of 
        Biological and Chemical Sciences at the University of Missouri–Kansas 
        City, and the University of Missouri Research Board.
        '''

    elif arg == 'A':
        return r'''
        Michael Green is a PhD candidate under the supervision of 
        Dr. Xiaobo Chen at the University of Missouri–Kansas City, 
        Department of Chemistry. He received his Bachelors of Science 
        in chemistry with a minor in mathematics from the University of 
        Idaho in 2016, and his Masters of Science in chemistry from the 
        University of Missouri–Kansas City in 2019. His research interests 
        include the development, characterization, modeling, and application 
        of nanomaterials in light/matter interactions, focusing on photolysis, 
        photocatalysis, and microwave absorption, as well as short-range 
        matter/matter interactions with a focus in physical adsorption.

        Contact:
            magwwc@mail.umkc.edu

        Dr. Xiaobo Chen is an Associate Professor with the Department of 
        Chemistry at the  University of Missouri–Kansas City. His research 
        interests include nanomaterials, catalysis, electrochemistry, 
        light-materials interactions and their applications in renewable 
        energy, environment protection, and information protection through 
        microwave absorption. His renowned work includes the discovery of 
        black TiO2 with Professor Samuel S. Mao at the University of 
        California, Berkeley and the new application of black TiO2 
        nanomaterials along with other nanomaterials in microwave absorption 
        application.

        Contact:
            chenxiaobo@umkc.edu
        '''
    else:
        return'''
        Click on the various buttons to the left for explanations 
        to the various functions available in this program.        
        '''