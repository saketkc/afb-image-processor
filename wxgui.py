import wx
import cv2
class MainFrame(wx.Frame):
    def __init__(self,parent):
         wx.Frame.__init__(self, parent)
         self.displayPanel = wx.Panel(self)
         self.displayPanel.SetSize(wx.Size(600,600))

