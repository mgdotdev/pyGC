This site is a docstring repository for the pyGC library, written by
Michael Green at the University of Missouri-Kansas City.

Use the tabs on the left-hand side of the page to navigate to the
various document sections.

Research was supported by the National Science Foundation under grant
NSF-1609061.

**Connect:**

Michael Green
`@Github <https://github.com/1mikegrn>`_
`@StackOverflow <https://stackoverflow.com/users/10881573/michael-green?tab=profile>`_

Getting Started
===============

The pyGC library can be installed via pip and git

:code:`pip install git+https://github.com/1mikegrn/pyGC`

Where the setup file will automatically check dependencies and install
to the main module library. Once installed, simply call the module as
normal via :code:`pyGC-init`, and the module will open.

Library Structure
=================

::

    pyGC/
        __init__.py         # initial executable
        __main__.py         # main function called by pyGC-init
        GUI.py              # python back-end which runs the app window/functions
        kivy_build.py       # .py file which holds the KVlang
        help_text.py        # function that returns text for the 'help' popup

