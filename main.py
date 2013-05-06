import wx
import cv2
import numpy as np
import cv2.cv as cv



lowThreshold = 0
max_lowThreshold = 100
ratio = 3
kernel_size = 3
    
  
class MyFrame(wx.Frame):
	def __init__(self, parent, ID, title):
		wx.Frame.__init__(self, parent, ID, title, size=(1000, 800))
		original_img = wx.EmptyImage(480,480)
		processed_img = wx.EmptyImage(480,480)
		self.PINK_MIN = np.array([140,50,50],np.uint8)
		self.PINK_MAX = np.array([170,200,200],np.uint8)

		self.PhotoMaxSize = 500
		self.panel1 = wx.Panel(self,1, style=wx.SUNKEN_BORDER)
		self.panel2 = wx.Panel(self,2, style=wx.SUNKEN_BORDER)
		self.panel3 = wx.Panel(self,3, style=wx.SUNKEN_BORDER)
		self.panel4 = wx.Panel(self,4, style=wx.SUNKEN_BORDER)
		self.panel5 = wx.Panel(self,5, style=wx.SUNKEN_BORDER)
		
		self.original_image = wx.StaticBitmap(self.panel1, wx.ID_ANY,wx.BitmapFromImage(original_img))
		self.processed_image =  wx.StaticBitmap(self.panel2, wx.ID_ANY,wx.BitmapFromImage(processed_img))
		
		self.browse_button= wx.Button(self.panel4, label='Browse')
		self.browse_button.Bind(wx.EVT_BUTTON, self.onBrowse)
		
		
		self.image_processing_button = wx.Button(self.panel5, label='Edge Detection')
		self.image_processing_button.Bind(wx.EVT_BUTTON, self.CannyThreshold)
		
		self.photo_text =wx.TextCtrl(self.panel3,size=(400,-1))
		self.vertical_box = wx.BoxSizer(wx.VERTICAL)
		self.horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
		self.horizontal_box_down= wx.BoxSizer(wx.HORIZONTAL)
		
		self.horizontal_box.Add(self.panel1, 1, wx.EXPAND)
		self.horizontal_box.Add(self.panel2, 2, wx.EXPAND)
		
		self.horizontal_box_down.Add(self.panel3, 0)
		self.horizontal_box_down.Add(self.panel4, 0)
		self.horizontal_box_down.Add(self.panel5, 0)
		self.vertical_box.Add(self.horizontal_box, 0, wx.ALL, 5)
		self.vertical_box.Add(self.horizontal_box_down, 1, wx.ALL, 5)
		self.SetAutoLayout(True)
		self.SetSizer(self.vertical_box)
		self.Layout()
		self.child = ChildFrame(self)
		self.child.Show()
		self.child1 = ChildFrame1(self)
		self.child1.Show()
		
	
	def onBrowse(self, event):
		wildcard = "*.jpg|*.JPG|*.png"
		dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard,style=wx.OPEN)
		if dialog.ShowModal() == wx.ID_OK:
			self.photo_text.SetValue(dialog.GetPath())
		dialog.Destroy()
		self.onView()
	
	def CannyThreshold(self,event):
		img = cv2.imread(self.photo_text.GetValue())
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		row, col, x = img.shape
		detected_edges = cv2.GaussianBlur(gray,(3,3),0)
		detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
		dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.
		self.processed_image.SetBitmap(wx.BitmapFromBuffer(col,row,dst))
		self.panel3.Refresh()

		
	def onView(self):
		filepath = self.photo_text.GetValue()
		img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		# scale the image, preserving the aspect ratio
		W = img.GetWidth()
		H = img.GetHeight()
		if W > H:
			NewW = self.PhotoMaxSize
			NewH = self.PhotoMaxSize * H / W
		else:
			NewH = self.PhotoMaxSize
			NewW = self.PhotoMaxSize * W / H
		#img = img.Scale(NewW,NewH)
		
		self.original_image.SetBitmap(wx.BitmapFromImage(img))
		self.panel1.Refresh()
	
	def  PerformSegmentation(self,event):
		filepath = self.photo_text.GetValue()
		img = cv.LoadImage(filepath, cv.CV_LOAD_IMAGE_COLOR)		
		img_hsv = cv.CreateImage(cv.GetSize(img),8,3)
		cv.CvtColor(img,img_hsv,cv.CV_BGR2HSV)
		frame_threshed = cv.CreateImage(cv.GetSize(img_hsv), 8, 1)
		print self.PINK_MIN
		cv.InRange(img_hsv, cv.fromarray(self.PINK_MIN,allowND=True), cv.fromarray(self.PINK_MAX,allowND=True), frame_threshed)
		cv.SaveImage("/home/saket/Desktop/threshed.jpg", frame_threshed)
		#col = frame_threshed.height
		#row=frame_threshed.width
		#img1 = wx.Image("/home/saket/Desktop/threshed.jpg", wx.BITMAP_TYPE_ANY)#
		img1 = cv2.imread("/home/saket/Desktop/threshed.jpg")
		img = cv2.imread(filepath)
		row, col, x = img1.shape
		#wxImage = wx.EmptyImage(row,col)
		#wxImage.SetData(frame_threshed.tostring())
		#wxBmap = wxImage.ConvertToBitmap()
		#self.processed_image.SetBitmap(wx.BitmapFromBits(frame_threshed.tostring(),row,col))
		dst = cv2.bitwise_and(img,img1)
		#self.processed_image.SetBitmap(wx.BitmapFromImage(img1))
		self.processed_image.SetBitmap(wx.BitmapFromBuffer(col,row,dst))
		#self.processed_image.SetBitmap(wx.BitmapFromImage(dst))
		self.panel2.Refresh()
		print "d"
		
	
	def onSlideHueLow(self,event):
		#hue = self.child.sldh1.GetValue()
		h1 = self.child.sldh1.GetValue()
		h2 = self.child.sldh2.GetValue()
		v1 =  self.child.sldv1.GetValue()
		v2  = self.child.sldv2.GetValue()
		s1 = self.child.slds1.GetValue()
		s2 = self.child.slds2.GetValue()
		
		#print hue
		self.PINK_MIN = np.array([h1,s1,v1],np.uint8)
		self.PINK_MAX = np.array([h2,s2,v2],np.uint8)
		self.PerformSegmentation("event")


class ChildFrame(wx.Frame):
    def __init__(self, parent):
		wx.Frame.__init__(self, None, size=(350,350), title='Adjust HSV Levels')
        #self.panel1 = wx.Panel(self)
		self.parent = parent
		pan = wx.Panel(self)
		#self.txt = wx.TextCtrl(pan, -1, pos=(0,0), size=(100,20), style=wx.DEFAULT)
		self.text1 =  wx.StaticText(pan, label="Hue Lowe", pos=(0, 0))
		self.sldh1 = wx.Slider(pan, -1, 140, 0, 180, (100,0), (250, -1),          wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS, name="DASD")
		
		self.text2 =  wx.StaticText(pan, label="Hue Upper", pos=(0, 40))		
		self.sldh2 = wx.Slider(pan, -1, 180, 0, 180, (100,40), (250, -1),          wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		
		self.text3 =  wx.StaticText(pan, label="Sat Lower ", pos=(0, 80))		
		self.slds1 = wx.Slider(pan, -1, 60, 0, 255, (100,80), (250, -1),          wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		
		self.text4 =  wx.StaticText(pan, label="Sat Upper ", pos=(0, 120))		
		self.slds2 = wx.Slider(pan, -1, 200, 0, 255, (100,120), (240, -1),          wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		
		self.text5 =  wx.StaticText(pan, label="Val Lower ", pos=(0, 160))				
		self.sldv1 = wx.Slider(pan, -1, 60, 0, 255, (100,160), (250, -1),          wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		
		self.text6 =  wx.StaticText(pan, label="Val Upper", pos=(0, 200))		
		self.sldv2 = wx.Slider(pan, -1, 200, 0, 255, (100,200), (250, -1),          wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		
		self.Bind(wx.EVT_SLIDER, self.parent.onSlideHueLow, self.sldh1)
		self.Bind(wx.EVT_SLIDER, self.parent.onSlideHueLow, self.sldh2)
		self.Bind(wx.EVT_SLIDER, self.parent.onSlideHueLow, self.sldv1)
		self.Bind(wx.EVT_SLIDER, self.parent.onSlideHueLow, self.sldv2)
		self.Bind(wx.EVT_SLIDER, self.parent.onSlideHueLow, self.slds1)
		self.Bind(wx.EVT_SLIDER, self.parent.onSlideHueLow, self.slds2)
		
    def onbutton(self, evt):
        text = self.txt.GetValue()
        self.parent.CannyThreshold("e")

class ChildFrame1(wx.Frame):
	def __init__(self,parent):
		wx.Frame.__init__(self, None, size=(200,300), title='File Chooser')
		self.parent = parent
		pan = wx.Panel(self)
		self.dirBrowser = wx.GenericDirCtrl(pan,-1,size=(200,300),  style=wx.DIRCTRL_SHOW_FILTERS,  filter="All files (*.*)|*.*|Images (*.jpg)|*.jpg")
		self.tree = self.dirBrowser.GetTreeCtrl()
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.dirBrowser_OnItemSelected, self.tree)
	def dirBrowser_OnItemSelected(self,event):
		#print event
		self.dirname = self.dirBrowser.GetPath() 
		self.parent.photo_text.SetValue(self.dirname)
		self.parent.onView()
		print self.dirname

	
		
		

app = wx.PySimpleApp()
frame = MyFrame(None, -1, "Image ")
frame.Show()
app.MainLoop()
