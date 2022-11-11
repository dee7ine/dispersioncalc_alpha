import os
import wx
from dataclasses import dataclass
from isotropic_main import show_image
from Decorators import timeit
@dataclass
class IsotropicMaterials(wx.Panel):
    def __init__(self, parent) -> None:
        wx.Panel.__init__(self, parent)

    @classmethod
    def InitializeWidgets(cls, panel) -> None:





        specimen_annotation = wx.StaticText(panel, label="Specimen",
                                            style = wx.ALIGN_LEFT,
                                            pos = (10, 15))

        fluidCheckBox = wx.CheckBox(panel, label = 'Fluid-loading',
                          style=wx.ALIGN_RIGHT,
                          pos=(5, 60))
        fluidCheckBox.SetValue(True)



        fluidChoiceBox = wx.Choice(panel, -1,
                                    pos = (85, 95),
                                    choices= ["air", "water"],
                                    style = wx.ALIGN_LEFT)

        fluidChoiceBox_annotation = wx.StaticText(panel,
                                         label = "Fluid",
                                         pos = (10, 100),
                                         style = wx.ALIGN_LEFT)

class PanelTemplate(wx.Panel):
    def __init__(self, parent, color, style):
        wx.Panel.__init__(self, parent, style = wx.SP_BORDER)
        self.SetBackgroundColour(color)

class AnisotropicMaterials(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class MaterialEditor(wx.Panel):
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
@dataclass
class MainFrame(wx.Frame):
    @timeit
    def __init__(self):
        wx.Frame.__init__(self, None, title="Racoon Simulator 9000", size = (1500, 750))

        """
        tab management
        """

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        """
        
        initialize tabs
        
        """

        tab1 = IsotropicMaterials(nb)
        tab2 = AnisotropicMaterials(nb)
        tab3 = MaterialEditor(nb)
        tab4 = TabFour(nb)
        tab5 = TabFive(nb)
        tab6 = TabSix(nb)
        tab7 = TabSeven(nb)
        tab8 = TabSeven(nb)

        IsotropicMaterials.InitializeWidgets(panel = tab1)

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
        sizer.Add(nb, 3, wx.EXPAND)
        p.SetSizer(sizer)

        self.makeMenuBar()
        self.Maximize(False)

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
    mainframe = MainFrame()

    mainframe.Show()
    icon_path = os.path.join("C:/Users",
                             "deefi",
                             "PycharmProjects",
                             "dispersioncalc_alpha",
                             "graphics",
                             "bearicon.ico")
    mainframe.SetIcon(wx.Icon(icon_path))
    app.MainLoop()
