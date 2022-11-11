"""
window splitter version
"""

import wx
from isotropic_main import show_image
from decorators import timeit


class IsotropicMaterials(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


        topSplitter = wx.SplitterWindow(self)
        vSplitter = wx.SplitterWindow(topSplitter)

        panelOne = PanelTemplate(vSplitter, "lightgrey", wx.SP_3D)
        panelTwo = PanelTemplate(vSplitter, "white", wx.SP_BORDER)

        vSplitter.SplitVertically(panelOne, panelTwo)
        vSplitter.SetSashGravity(0.2)

        panelThree = PanelTemplate(topSplitter, "white", wx.SP_BORDER)
        topSplitter.SplitHorizontally(vSplitter, panelThree)
        topSplitter.SetSashGravity(0.7)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)


class PanelTemplate(wx.Panel):
    def __init__(self, parent, color, style):
        wx.Panel.__init__(self, parent, style = wx.SP_BORDER)
        self.SetBackgroundColour(color)


class AnisotropicMaterials(wx.Panel):
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
        wx.Frame.__init__(self, None, title="disp calc")

        """
        tabs holder
        """

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        """
        tabs management
        """
        tab1 = IsotropicMaterials(nb)
        tab2 = AnisotropicMaterials(nb)
        tab3 = TabThree(nb)
        tab4 = TabFour(nb)
        tab5 = TabFive(nb)
        tab6 = TabSix(nb)
        tab7 = TabSeven(nb)
        tab8 = TabSeven(nb)

        #
        cb1 = wx.CheckBox(tab1, label='checkmark', pos=(1000, 20))
        cb1.SetValue(False)
        cb1 = wx.CheckBox(tab1, label='checkmark', pos=(1000, 40))
        cb1.SetValue(False)

        cb2 = wx.CheckBox(tab2, label='checkmark', pos=(200, 40))
        cb2.SetValue(True)

        cb3 = wx.CheckBox(tab3, label='checkmark', pos=(128, 128))
        cb3.SetValue(True)

        nb.AddPage(tab1, "Isotropic")
        nb.AddPage(tab2, "Anisotropic")
        nb.AddPage(tab3, "Signal simulator")
        nb.AddPage(tab4, "Polar diagrams")
        nb.AddPage(tab5, "Bulk waves")
        nb.AddPage(tab6, "Laminate stiffness")
        nb.AddPage(tab7, "Material editor")
        nb.AddPage(tab8, "Advanced")

        """
        layout management
        """
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.makeMenuBar()

        self.Maximize(True)

    def makeMenuBar(self) -> None:
        """

        :return:
        """

        fileMenu = wx.Menu()

        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)


        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        aboutMenu = wx.Menu()
        about1 = aboutMenu.Append(wx.ID_ABOUT)
        about2 = aboutMenu.Append(wx.ID_ABOUT)
        about3  = aboutMenu.Append(wx.ID_ABOUT)

        materialsMenu = wx.Menu()
        multicoreMenu = wx.Menu()
        homepageMenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(materialsMenu, "&Materials")
        menuBar.Append(multicoreMenu, "&Multicore")
        menuBar.Append(homepageMenu, "&Homepage")
        menuBar.Append(helpMenu, "&Help")
        menuBar.Append(aboutMenu, "&About")

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
        self.Close(True)


    def OnHello(self, event) -> None:
        """
        :param event:
        :return:
        """
        wx.MessageBox("default")

    def OnAbout(self, event):

        wx.MessageBox("link to be generated",
                      wx.OK|wx.ICON_INFORMATION)
        show_image()

if __name__ == "__main__":
    app = wx.App()
    frm = MainFrame()
    frm.Show()

    app.MainLoop()
