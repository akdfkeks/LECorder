#-*-coding:utf-8
import threading
import cv2
import time
import os
from PIL import Image
from ctypes import windll
import win32gui
import win32ui
import win32con

class Recorder():
	def __init__(self, winName, frame):
		self.winName = winName
		self.frame = frame
		self.hwnd = win32gui.FindWindow(None, self.winName)

		left, top, right, bot = win32gui.GetWindowRect(self.hwnd)

		self.w= right - left
		self.h= bot - top

		self.hwndDC = win32gui.GetWindowDC(self.hwnd)
		self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
		self.saveDC = self.mfcDC.CreateCompatibleDC()
		
		self.saveBitMap = win32ui.CreateBitmap()
		self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
		self.saveDC.SelectObject(self.saveBitMap)
		self.filename = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
		
		self.record()
	
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
		#try:
			##while(True):
		for i in range(30):
			self.saveDC.SelectObject(self.saveBitMap)
			self.saveDC.BitBlt((0, 0),(self.w, self.h), self.mfcDC, (0, 0), win32con.SRCCOPY)
			#self.saveBitMap.SaveBitmapFile(self.saveDC, "t.png")
			self.saveBitMap.Paint(self.saveDC)
		#except Exception as err:
		#	print(err)

		cap.release()
		cv2.destroyAllWindows()
		
		video.release()