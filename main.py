import wx
import scipy.misc
from new import show_image
from new import test_function
from Decorators import timeit

# Define the tab content as classes:
class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "hohohooho", (100, 100))

class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


class TabThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


class TabFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class TabFive(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class TabSix(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class TabSeven(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class TabEight(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class MainFrame(wx.Frame):
    @timeit
    def __init__(self):
        wx.Frame.__init__(self, None, title="Tree Simulator 9000")

        """
         Create a panel and notebook (tabs holder)
        """

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # Create the tab windows
        tab1 = TabOne(nb)
        tab2 = TabTwo(nb)
        tab3 = TabThree(nb)
        tab4 = TabFour(nb)
        tab5 = TabFive(nb)
        tab6 = TabSix(nb)
        tab7 = TabSeven(nb)
        tab8 = TabSeven(nb)

        cb1 = wx.CheckBox(tab1, label='Marcin', pos=(20, 20))
        cb1.SetValue(False)

        cb2 = wx.CheckBox(tab2, label='TIME', pos=(200, 40))
        cb2.SetValue(True)

        cb3 = wx.CheckBox(tab3, label='TIME', pos=(128, 128))
        cb3.SetValue(True)

        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "Isotropic")
        nb.AddPage(tab2, "Anisotropic")
        nb.AddPage(tab3, "Signal simulator")
        nb.AddPage(tab4, "Polar diagrams")
        nb.AddPage(tab5, "Bulk waves")
        nb.AddPage(tab6, "Laminate stiffness")
        nb.AddPage(tab7, "Material editor")
        nb.AddPage(tab8, "Advanced")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.makeMenuBar()

        self.Maximize(True)

    def makeMenuBar(self) -> None:
        """

        :return:
        """
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        #about menu
        aboutMenu = wx.Menu()
        about1 = aboutMenu.Append(wx.ID_ABOUT)
        about2 = aboutMenu.Append(wx.ID_ABOUT)
        about3  = aboutMenu.Append(wx.ID_ABOUT)

        #materials menu
        materialsMenu = wx.Menu()

        #multicore menu
        multicoreMenu = wx.Menu()

        #homepage menu
        homepageMenu = wx.Menu()

        """
        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        
        """

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(materialsMenu, "&Materials")
        menuBar.Append(multicoreMenu, "&Multicore")
        menuBar.Append(homepageMenu, "&Homepage")
        menuBar.Append(helpMenu, "&Help")
        menuBar.Append(aboutMenu, "&About")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)
        """
        associate a handler function with the EVT_MENU event for
        each of the menu items. That means that when that menu item is
        activated then the associated handler function will be called.
        """
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event) -> None:
        """
        :param event:
        :return:
        """
        """
        
        Close the frame, terminating the application.
        """

        self.Close(True)


    def OnHello(self, event) -> None:
        """
        :param event:
        :return:
        """

        """Say hello to the user."""
        wx.MessageBox("Gruszczyk alert\n Run")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)
        show_image()

if __name__ == "__main__":
    app = wx.App()
    #MainFrame().Show() # do wyjebania
    frm = MainFrame()
    #frm.SetIcon(wx.IconFromLocation("C:/Users/xjlksd/Downloads/tree.ico")) #do wyjebania (?)
    frm.Show()
    frm.SetIcon(wx.Icon(r"C:\Users\deefi\PycharmProjects\dispersioncalc_alpha\cropped3815.ico"))
    app.MainLoop()
