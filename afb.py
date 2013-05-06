import cv2.cv as cv
import sys
import cv2
import numpy as np
PINK_MIN = np.array([140,50,50],np.uint8)

PINK_MAX = np.array([170,200,200],np.uint8)
win_name = "Original Image"
img = cv.LoadImage(sys.argv[1], cv.CV_LOAD_IMAGE_COLOR)
img_old=img
img_hsv = cv.CreateImage(cv.GetSize(img),8,3)
cv.CvtColor(img,img_hsv,cv.CV_RGB2HSV)
frame_threshed = cv.CreateImage(cv.GetSize(img_hsv), 8, 1)
cv.InRange(img_hsv, cv.fromarray(PINK_MIN,allowND=True), cv.fromarray(PINK_MAX,allowND=True), frame_threshed)
cv.SaveImage("/home/saket/Desktop/threshed.jpg", frame_threshed)
#contours, hierarchy = cv2.findContours(frame_threshed, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
#print(len(contours))
nomeimg = "/home/saket/Desktop/threshed.jpg"
img = cv2.imread(nomeimg)
gray = cv2.imread(nomeimg,0)#converte in scalagrigi e bn
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(6,6)) #
graydilate = cv2.erode(gray, element) #imgbnbin
ret,thresh = cv2.threshold(graydilate,0,255,cv2.THRESH_BINARY_INV)
imgbnbin = thresh
img = cv2.imread(sys.argv[1])
contours, hierarchy = cv2.findContours(imgbnbin, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
for i in range (0, len(contours)):
    print cv2.boundingRect(contours[i])

    cv2.drawContours(img,contours,i,cv.RGB(0,0,0),5)
storage = cv.CreateMemStorage(0)

#contours = cv.FindContours(imgbnbin, storage,cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE,(0,0))

cv.DrawContours(img=img_old,contour=contours,external_color=cv.RGB(255, 0, 0), hole_color=cv.RGB(0, 255, 0), max_level=1 )
cv2.imshow('draw contour',img)
cv2.waitKey(0)


#cv.NamedWindow(win_name, cv.CV_WINDOW_AUTOSIZE)
#cv.CreateTrackbar(trackbar_name, win_name, 1, 100, on_trackbar
#cv.ShowImage(win_name, img)
#cv.WaitKey(0)
#cv.DestroyAllWindows()


