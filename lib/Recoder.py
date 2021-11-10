#-*-coding:utf-8
import threading
import cv2
import time
import os
from PIL import Image
import numpy as np
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
		#cap = cv2.VideoCapture(0)
		video = cv2.VideoWriter(path + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.frame, (self.w,self.h))
		
		print(self.hwnd)
		#try:
			##while(True):
		for i in range(3):
			left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
			self.w= right - left
			self.h= bot - top
			self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
			self.saveDC.SelectObject(self.saveBitMap)
			self.saveDC.BitBlt((0, 0),(self.w, self.h), self.mfcDC, (0, 0), win32con.SRCCOPY)
			self.saveBitMap.SaveBitmapFile(self.saveDC, ("t"+ f'{i}' +".png"))
			temp = self.saveBitMap.GetBitmapBits(True)
			
			bmparray = np.s(dataBitMap.GetBitmapBits(), dtype=numpy.uint8)
			pil_im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmparray, 'raw', 'BGRX', 0, 1)
			pil_array = numpy.array(pil_im)
			cv_im = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)
			
			
			
			
			print(frame)

			#video.write(frame)

		#except Exception as err:
		#	print(err)

		#cap.release()
		video.release()
		cv2.destroyAllWindows()
		print("end")
		