#-*-coding:utf-8
import threading
import cv2
import time
import os
from PIL import Image
from ctypes import windll
import win32gui
import win32ui

class Recorder():
	def __init__(self, winName, frame):
		self.w = 0
		self.h = 0
		self.frame = frame
		self.winName = winName
		self.filename = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

		self.hwnd = win32gui.FindWindow(None, self.winName)
		self.hwndDC = win32gui.GetWindowDC(self.hwnd)
		self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
		self.saveDC = self.mfcDC.CreateCompatibleDC()
		
		self.saveBitMap = win32ui.CreateBitmap()
		self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
		self.saveDC.SelectObject(self.saveBitMap)
		
		self.result = windll.user32.PrintWindow(self.hwnd, self.saveDC.GetSafeHdc(), 0)
		
		self.bmpinfo = self.saveBitMap.GetInfo()
		self.bmpstr = self.saveBitMap.GetBitmapBits(True)
		self.default_bmpinfo = self.bmpinfo
		self.default_bmpstr = self.bmpstr
		
		self.setwindowSize()
	
	def __del__(self):
		win32gui.DeleteObject(self.saveBitMap.GetHandle())
		self.saveDC.DeleteDC()
		self.mfcDC.DeleteDC()
		win32gui.ReleaseDC(self.hwnd, self.hwndDC)
		
	def record(self):
		path = os.path.join(os.path.expanduser('~'),'Desktop','LECoder', self.filename)
		cap = cv2.VideoCapture(0)
		video = cv2.VideoWriter(path + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), self.frame, (self.w,self.h))
		
		print(self.hwnd)
		try:
			while(True):
				if not (self.default_bmpinfo['bmWidth']==self.bmpinfo['bmWidth'] and self.default_bmpinfo['bmHeight']==self.bmpinfo['bmHeight']):
					self.setwindowSize()
				im = Image.frombuffer('RGB',(self.default_bmpinfo['bmWidth'], self.default_bmpinfo['bmHeight']), self.default_bmpstr, 'raw', 'BGRX', 0, 1)
				im.show()
				time.sleep(1.0)
				#video.write(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
		except Exception as err:
			print(err)

		cap.release()
		cv2.destroyAllWindows()
		
		video.release()

	def setwindowSize(self):
		left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
		self.w= right - left
		self.h= bot - top
		self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
		self.bmpinfo = self.saveBitMap.GetInfo()
		self.default_bmpinfo = self.bmpinfo
		self.default_bmpstr = self.saveBitMap.GetBitmapBits(True)
