# Gas Chromatography and Data Functionalization in Python

This GitHub repository is designed to have multiple functions:

- Act as a Binder/CoLab host
- Act as a data/code repository for JCE supplemental
- pip installation for pyGC

# Binder and Colab

First, this repository includes an example jupyter notebook which is
linked to both a binder environment and a google colab environment, 
which allows for demonstration without any necessary
installations. To use, simply press either the 'launch Binder' or the 
'Open in CoLab' button below:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/1mikegrn/pyGC/master?filepath=binder)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/1mikegrn/pyGC/blob/master/binder/index.ipynb)

We've also included two more notebooks called 'Asymmetric GC integration' and
'Symmetric GC integration' which are directly available for students to use for
GC analysis. Open these by pressing the buttons below:

Asymmetric GC integration: [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/1mikegrn/pyGC/blob/master/colab/Asymmetric_GC_integration.ipynb)

Symmetric GC integration: [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/1mikegrn/pyGC/blob/master/colab/Symmetric_GC_integration.ipynb)

To note, the Binder notebook takes several minutes to spin up, so
plan accordingly if you choose to use it in presentation. We recommend
using the CoLab option for faster implementations,
though it may prompt a warning saying that colab
is going to link to your google drive account.

# Supplemental Files

Secondly, this repository includes as a file directory the contents of
the JCE manuscript supplemental files. That directory can be downloaded
using the following link:

[JCE-Supplemental](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/1mikegrn/pyGC/tree/master/JCE-supplemental)

# pyGC

Finally, this repository hosts the pyGC module, which can be installed
into python using pip ang git:

    pip install git+https://github.com/1mikegrn/pyGC
    
once installed, the application can be run by opening your python
terminal and running:

    pyGC-init