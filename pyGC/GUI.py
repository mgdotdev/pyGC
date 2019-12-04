"""
:code:`GUI.py`
==============

pyGC's main application module for spinning up the kivy application. The module
doesn't require any code-level modifications - just initialize with the
pyGC-init command at the terminal and work in the resulting window.

There are a few things to note in the code that are non-PEP8. The big one is
the matplotlib spin-up before the application - there's a bug in kivy which
changes the window resolution when matplotlib is initialized. Since the whole
point of this app is to have an interactive matplotlib window, there was no
avoiding this, and the increased window resolution was actually kind of nice,
so we initialize a mpl graph before the kivy app so the app gets built with the
bugged mpl settings instead of refactoring the kivy app after its built.
"""

# open a dummy mpl figure to usurp kivy's rendering protocols
from matplotlib import pyplot as plt, rcParams

def bug_exploit():
    dummy_fig = plt.figure(dpi=1000)
    plt.close(dummy_fig)

    rcParams['font.family'] = 'serif'
    rcParams['font.sans-serif'] = ['Bookman']
    rcParams['font.size'] = 10
    rcParams['mathtext.fontset'] = 'stix'

    from kivy.config import Config

    window_width = 1000
    window_height = 900

    Config.set('graphics', 'width', str(window_width))
    Config.set('graphics', 'height', str(window_height))
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# comment this out when building sphinx docs
# sphinx doesn't like you for using bug exploits at runtime!
bug_exploit()

from numpy import (
    float64, exp, concatenate,
    arange, delete, sqrt,
    pi, zeros
)

from pandas import(
    read_csv, read_excel,
    ExcelWriter, DataFrame
)

from os.path import(
    sep, expanduser,
    dirname, splitext
)

from scipy.special import erf
from scipy.optimize import leastsq
from scipy.integrate import quad

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.lang import Builder

from pyGC.graph.backend_kivyagg import FigureCanvas
from pyGC.FileBrowser import FileBrowser
from pyGC import kivy_build
from pyGC.help_text import texts


def calc_primer(dataFile):
    """

refactors the given user data from the file_popup into an array of GC data.

::

    :param dataFile:    (str)

GC data of Nx2 dimensions. Given as a string equivalent to the directory and
file name of either a .csv or .xlsx of Nx2 dimensions. Text above and below
data array will be automatically avoided by the program.

::

    :return:            (array)

refactored data set of Nx2 dimensionality in numpy array
    """

    if dataFile is None:
        error_msg = 'Data must be passed as an array which is mappable ' \
                   'to an Nx5 numpy array with columns ' \
                   '[freq, e1, e2, mu1, mu2]'
        raise RuntimeError(error_msg)

    # allows for file location to be passed as the data variable.
    elif isinstance(dataFile, str) is True:

        if splitext(dataFile)[1] == '.csv':
            data = read_csv(dataFile, sep=',').to_numpy()

            if data.shape[1] == 1 \
                    and "\t" in data[data.shape[0]//2][0]:
                data = read_csv(dataFile, sep='\t').to_numpy()

        elif splitext(dataFile)[1] == '.xlsx':
            data = read_excel(dataFile).to_numpy()

        else:
            error_msg = 'Error partitioning input data from string'
            raise RuntimeError(error_msg)

    else:
        data = dataFile

    # check each position in numpy array
    # if it can be a number, make it a number
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            try:
                data[row, col] = float64(data[row, col])
            except:
                pass

    # finds all rows in numpy array which aren't
    # a part of the Nx5 data array expected.
    #
    # NOTE:
    # if the file contains more/less than
    # 5 columns this fails as the 6th row is
    # always filled with NaN. That being said,
    # most instruments output a Nx5 data file.

    set_to_del = {row for row in arange(data.shape[0]) for col in
                  arange(data.shape[1]) if
                  isinstance(data[row, col], (int, float)) is False
                  or data[row, col] != data[row, col]}

    # removes non-data rows from input array to yield the data array
    data = delete(data, list(set_to_del), axis=0)
    return data


def add_plot(event):
    """

adds an 'initials' point for each gaussian guess to  the graph. Activated by
clicking the graph inside the borders.

::

    :param event:       ('button_press_event')

takes a 'button_press_event' from the app and places a point on the graph at
the click point, and adds that point to the initials list.

::

    :return:            (none)

updates the matplotlib canvas visible on the application screen.
    """

    #if clicked outside of plot, dont do anyting
    if isinstance(event.ydata, (int, float, float64)) is False or isinstance(
            event.xdata, (int, float, float64)) is False or (
    event.ydata, event.xdata) != (
            event.ydata, event.xdata): return

    # add clicked point to the list of initial parameters
    ax.plot(event.xdata, event.ydata, 'o',
            color=(242 / 255, 206 / 255, 14 / 255, 1), markersize=10)[0]
    initials.append([event.ydata, event.xdata])
    fig.canvas.draw()


def pull_plot(self):

    # clears the last item added to the axis, if there is an item
    if len(ax.lines) > 1:
        del ax.lines[-1]
        del initials[-1]
    fig.canvas.draw()


def pull_all_plots(self):

    # clears all items from plot axis, if there are any items
    if len(ax.lines) > 1:
        del ax.lines[:]
        del initials[:]
        ax.get_legend().remove()
    fig.canvas.draw()


def graph():
    """

graph widget which sits in the application window. Looks graph-y. Called from
the Meta() class.

::

    :return:    (fig)

returns the graph widget to be added to the application window.
    """
    global fig, ax
    fig = plt.figure(tight_layout=True, dpi=100)
    ax = fig.add_subplot(111)
    ax.tick_params(direction='in')
    wid = FigureCanvas(fig)
    fig.canvas.mpl_connect('button_press_event', add_plot)
    return wid


def graph_popup(self):
    # open the graph controls popup
    App.get_running_app().graph_popup.open()


def functionalize(data_var, initials_var, condition):
    """

main functionalization protocol for pyGC. Takes the user inputs given via the
GUI and initializes the least square regression analysis of the data for n-set
of gaussian distrbutions.

::

    :param data_var:        (array)

data_var is the x, y data which is derived from experimentation, passed through
from calc_primer.

::

    :param initials_var:    (list)

a list of lists which define the n-set of gaussians to fit to the data.

::

    :param condition:       (str)
                            ('Symmetric Gaussian'); 'Asymmetric Gaussian'

defines which function the app will attempt to fit the data set with.

::

    :return:                (tuple)
                            (plot_data, ledger, val_length)

a len(3) tuple of the necessary data for plotting - the data of each of the
gaussian distributions, a text ledger for each plot, and the number of
distributions.
    """
    val_length = len(initials_var)
    ledger = ['Data', 'Resultant']

    if condition == 'Function Type: Symmetric Gaussian':

        for i in range(len(initials_var)):
            initials_var[i].append(1)

        vars = concatenate(initials_var)

        def gaussian(x, a, b, c):
            return a * exp((-(x - b) ** 2.0) / c ** 2.0)

        def GaussSum(x, p):
            return sum(
                gaussian(x, p[3 * k],
                         p[3 * k + 1],
                         p[3 * k + 2])
                for k in range(val_length)
            )

    if condition == 'Function Type: Asymmetric Gaussian':

        for i in range(len(initials_var)):

            initials_var[i].append(1)
            initials_var[i].append(0)

        vars = concatenate(initials_var)

        def gaussian(x, a, b, c, d):
            y = (a / (c * sqrt(2 * pi))) * exp(
                (-(x - b) ** 2.0) / 2 * c ** 2.0) * (
                1 + erf((d * (x - b)) / (c * sqrt(2))))
            return y

        def GaussSum(x, p):

            y= sum(
                gaussian(
                    x,
                    p[4 * k],
                    p[4 * k + 1],
                    p[4 * k + 2],
                    p[4 * k + 3])
                for k in range(val_length))

            return y
    def residuals(p, y, x):
        return (y - GaussSum(x, p)) ** 2

    lsq = leastsq(residuals, vars, args=(data_var[:, 1], data_var[:, 0]))
    cnst = lsq[0]

    del ax.lines[:]
    del initials[:]

    plot_data = zeros((len(
        arange(data_var[0, 0],
               data_var[data_var.shape[0] - 1, 0] + 0.025,
               0.025)), val_length + 2
    ))

    plot_data[:, 0] = arange(
        data_var[0, 0],
        data_var[data_var.shape[0] - 1, 0] + 0.025,
        0.025
    )

    plot_data[:, 1] = GaussSum(
        plot_data[:, 0], cnst
    )

    ax.plot(data_var[:, 0], data_var[:, 1], 'o', color='k')
    ax.plot(plot_data[:, 0], plot_data[:, 1], color='r')

    areas = []

    if condition == 'Function Type: Symmetric Gaussian':

        for i in range(val_length):

            plot_data[:, i + 2] = gaussian(
                plot_data[:, 0], cnst[3 * i],
                cnst[3 * i + 1], cnst[3 * i + 2]
            )

            ax.plot(plot_data[:, 0], plot_data[:, i + 2])

        for i in range(val_length):

            areas.append(
                quad(
                    gaussian, data_var[0, 0],
                    data_var[data_var.shape[0] - 1, 0],
                    args=(
                        cnst[3 * i],
                        cnst[3 * i + 1],
                        cnst[3 * i + 2]
                    )
                )[0]
            )

        for i in range(val_length):
            ledger.append(str(round(cnst[3 * i + 1], 2)) + '$e^{(x-' + str(
                round(cnst[3 * i], 2)) + ')^2 / ' + str(
                round(cnst[3 * i + 2], 2)) + '^2}$' + ' \n Area = ' + str(
                round(areas[i], 3)))

    if condition == 'Function Type: Asymmetric Gaussian':
        for i in range(val_length):
            plot_data[:, i + 2] = gaussian(plot_data[:, 0], cnst[4 * i],
                                           cnst[4 * i + 1],
                                           cnst[4 * i + 2],
                                           cnst[4 * i + 3])
            ax.plot(plot_data[:, 0], plot_data[:, i + 2])

        for i in range(val_length):
            areas.append(quad(gaussian, data_var[0, 0],
                              data_var[data_var.shape[0] - 1, 0], args=(
                cnst[4 * i], cnst[4 * i + 1], cnst[4 * i + 2],
                cnst[4 * i + 3]))[0])

        for i in range(val_length):
            ledger.append('Area = ' + str(round(areas[i], 3)))

    ax.legend(ledger, fontsize=7)

    fig.canvas.draw()

    App.get_running_app().graph_popup.open()

    return plot_data, ledger, val_length


class file_popup(Popup):
    """

Presents the file_popup from FileBrowser.
    """

    def __init__(self, **kwargs):
        super(file_popup, self).__init__(**kwargs)
        self.add_widget(self.file_loader())

    def file_loader(self):

        if platform == 'win':
            user_path = dirname(expanduser('~')) + sep + 'Documents'
        else:
            user_path = expanduser('~') + sep + 'Documents'

        browser = FileBrowser(
            select_string='Select',
            favorites=[(user_path, 'Documents')]
        )

        browser.bind(
            on_success=self.file_browser_success,
            on_canceled=self.file_browser_canceled
        )
        return browser

    def file_browser_success(self, instance):
        file_popup.dismiss(self)
        file = instance.selection

        global data, plot_bounds, file_location_name

        data = calc_primer(file[0])
        file_location_name = splitext(file[0])[0]

        pull_all_plots(self)

        ax.plot(
            data[:, 0], data[:, 1], '-', linewidth=2,
            color=(0 / 255, 102 / 255, 204 / 255, 1)
        )

        plot_bounds = (
        min(data[:, 0]), max(data[:, 0]), min(data[:, 1]), max(data[:, 1])
        )

        ax.set_xlim(
            plot_bounds[0] - 0.1 * (plot_bounds[1] - plot_bounds[0]),
            plot_bounds[1] + 0.1 * (plot_bounds[1] - plot_bounds[0]))

        ax.set_ylim(
            plot_bounds[2] - 0.1 * (plot_bounds[3] - plot_bounds[2]),
            plot_bounds[3] + 0.1 * (plot_bounds[3] - plot_bounds[2])
        )

        fig.canvas.draw()

    def file_browser_canceled(self, instance):
        file_popup.dismiss(self)


class graph_options(Popup):
    """

graph options popup for the GC_decon app. Allows for changing graphical bounds
so to zoom and pan in 4 dimensions. Also toggles data and image exporting.
Inherets from Kivy (Popup) parent class.
    """

    def update_graph(self, text):
        """

protocol for updating the matplotlib space. Takes text objects from the
buttons pushed in the graph_options panel.

::

        :param text:    (text)
                        "Up", "Down", "Left", "Right", "Contract L/R",
                        "Expand L/R", "Contract U/D", "Expand U/D", "Center",

text of the button pressed. Options are predefined.

::

        :return:        (none)

automatically toggles a redrawing of the matplotlib graph with updated graph
parameters.
        """

        if text == 'Up':
            bounds = ax.get_ylim()
            ax.set_ylim(
                bounds[0] - 1 * self.ids.sensitivity.value,
                bounds[1] - 1 * self.ids.sensitivity.value
            )

        if text == 'Down':
            bounds = ax.get_ylim()
            ax.set_ylim(
                bounds[0] + 1 * self.ids.sensitivity.value,
                bounds[1] + 1 * self.ids.sensitivity.value
                )

        if text == 'Left':
            bounds = ax.get_xlim()
            ax.set_xlim(
                bounds[0] + 1 * self.ids.sensitivity.value,
                bounds[1] + 1 * self.ids.sensitivity.value
            )

        if text == 'Right':
            bounds = ax.get_xlim()
            ax.set_xlim(
                bounds[0] - 1 * self.ids.sensitivity.value,
                bounds[1] - 1 * self.ids.sensitivity.value
            )

        if text == 'Contract L/R':
            bounds = ax.get_xlim()
            ax.set_xlim(
                bounds[0] - 1 * self.ids.sensitivity.value,
                bounds[1] + 1 * self.ids.sensitivity.value
            )

        if text == 'Expand L/R':
            bounds = ax.get_xlim()
            ax.set_xlim(
                bounds[0] + 1 * self.ids.sensitivity.value,
                bounds[1] - 1 * self.ids.sensitivity.value
            )

        if text == 'Contract U/D':
            bounds = ax.get_ylim()
            ax.set_ylim(
                bounds[0] - 1 * self.ids.sensitivity.value,
                bounds[1] + 1 * self.ids.sensitivity.value
            )

        if text == 'Expand U/D':
            bounds = ax.get_ylim()
            ax.set_ylim(
                bounds[0] + 1 * self.ids.sensitivity.value,
                bounds[1] - 1 * self.ids.sensitivity.value
            )

        if text == 'Center':
            try:
                ax.set_xlim(
                    plot_bounds[0] - 0.1 * (plot_bounds[1] - plot_bounds[0]),
                    plot_bounds[1] + 0.1 * (plot_bounds[1] - plot_bounds[0])
                )
                ax.set_ylim(
                    plot_bounds[2] - 0.1 * (plot_bounds[3] - plot_bounds[2]),
                    plot_bounds[3] + 0.1 * (plot_bounds[3] - plot_bounds[2])
                )
            except:
                pass

        fig.canvas.draw()

    def save_fig(self):
        """

saves the graph image of the deconvolutions to the file location of the input
data.

::

        :return:        (none)

saves a *png file to the location of the data import.
        """
        plt.savefig(file_location_name + ' deconvolution.png')

    def export_to_excel(self):
        """

saves excel data of the deconvolutions to the file location of the input data.
Doesn't explicitly take function inputs, but relies on global variables
returned by functionalize() to save data.

::

        :return:        (none)

generates a writer which saves an excel file to the location of the data
import.
        """
        data_to_exp = plot_data_global[0]
        ledger = plot_data_global[1]
        val_length = plot_data_global[2]
        output_file = file_location_name + ' deconvolution.xlsx'
        ledger[0] = 'x'
        df_ledger = {
            ledger[i]: data_to_exp[:, i]
            for i in range(val_length + 2)
        }
        writer = ExcelWriter(output_file)
        df1 = DataFrame(df_ledger)
        df1.to_excel(writer, sheet_name='Sheet1')
        writer.save()


class help_popup(Popup):
    """

changes the text of the help_popup window depending on the button pressed.
    """

    def help_text(self, event):
        """

takes button information and updates the popup text.

::

        :param event:   (str)

the string id of the pressed button.

::

        :return:        (none)

updates the GUI display without returning information to the class.
        """

        if event == 'Input Data':
            text = texts(arg='ID')
            self.ids.label.text = text

        elif event == 'Function Type':
            text = texts(arg='C')
            self.ids.label.text = text

        elif event == 'Input Graph':
            text = texts(arg='IV')
            self.ids.label.text = text

        elif event == 'Output Graph':
            text = texts(arg='OG')
            self.ids.label.text = text

        elif event == 'Output Data':
            text = texts(arg='OD')
            self.ids.label.text = text

        elif event == 'About':
            text = texts(arg='A')
            self.ids.label.text = text

        elif event == 'Acknowledgments':
            text = texts(arg='ACK')
            self.ids.label.text = text

        else:
            text = texts(arg='Main')
            self.ids.label.text = text


class GraphButtons(BoxLayout):
    """

Inherits from BoxLayout, adds buttons to the app window which allow for graph
interaction.
    """

    def __init__(self, **kwargs):
        """

adds three buttons to the window on initialization.
- :code:`clear last object`: removes from the graph the last added object.
- :code:`clear graph`: removes all objects from the graph.
- :code:`graph options`: opens the graph_options menu.
        """
        super(GraphButtons, self).__init__(**kwargs)
        self.size_hint_y = 0.1
        self.add_widget(
            Button(text='clear last object', on_release=pull_plot)
        )
        self.add_widget(
            Button(text='clear graph', on_release=pull_all_plots)
        )
        self.add_widget(
            Button(text='graph options', on_release=graph_popup)
        )


class Body(GridLayout):
    """

App body, inheriting from the Kivy Gridlayout, which binds the button actions
to the python backend.
    """
    def file_popup(self):
        """

opens the file_import popup which allows users to locate GC data on the
computer.

::

        :return:    (none)

opens the file_import popup in the kivy application.
        """

        App.get_running_app().file_popup.open()

    def help_popup(self):
        """

opens the help popup which contains instructional text for users regarding app
use.

::

        :return:    (none)

opens the help popup in the kivy application.
        """
        App.get_running_app().help_popup.open()

    def calc(self):
        """

triggers deconvolution in the function functionalize() from pressing the
button "Start" in the main GUI window

::

        :return:    (none)

toggles the "functionalize" function herein, passing the data from the GUI to
the function.
        """

        global plot_data_global
        plot_data_global = functionalize(
            data_var=data,
            initials_var=initials,
            condition=self.ids.condition.text
        )

    def reset_app(self):
        """

clears all variables and the graph space.

::

        :return:    (none)

toggles pull_all_plots() via pressing the 'reset' button.
        """
        pull_all_plots(self)


class Meta(BoxLayout):
    """

class which is the layout on which the application is built. Contains three
blocks of widgets:

- graph() - the widget from the graph() function which is placed at the top of
  the Kivy window.
- GraphButtons() - buttons immediately under the Graph() widget which control
  user options for clearing graph objects.
- Body() - Buttons which user interacts with to import data and run analysis.
    """
    def __init__(self, **kwargs):
        super(Meta, self).__init__(**kwargs)
        self.add_widget(graph())
        self.add_widget(GraphButtons())
        self.add_widget(Body())


class GC_decon(App):
    """

class which inherits from the Kivy App to initialze the applicaiton.
    """
    global initials
    initials = []

    Builder.load_string(kivy_build.KVlang)

    def build(self):
        """

Builds the application window and populates it with widgets

::

    :return:    (class)

returns the Meta() class to the App.
        """
        self.help_popup = help_popup()
        self.graph_popup = graph_options()
        self.file_popup = file_popup()
        return Meta()


