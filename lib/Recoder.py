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
				self.saveDC.BitBlt((0, 0),(self.w, self.h), self.mfcDC, (0, 0), win32con.SRCCOPY)
				self.saveBitMap.SaveBitmapFile(self.saveDC, 'screenshot.bmp')
				break
		except Exception as err:
			print(err)

		cap.release()
		cv2.destroyAllWindows()
		
		video.release()