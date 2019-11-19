"""
:code:`__main__.py`
=====================

module that pyGC-init points to - includes the main() module function. running
main() initializes the application.
"""
import pyGC.GUI as GUI


def main():
    """

main function which pyGC-init toggles to run the kivy application, which
ultimately calls the run() function in class GUI.GC_decon().

                    ---------------------------------------
::

    :return:        none
    """
    GUI.GC_decon().run()


if __name__ == "__main__":
    main()