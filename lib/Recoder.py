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
		
		video = cv2.VideoWriter(path + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.frame, (self.w,self.h))
		
		print(self.hwnd)
		#try:
			##while(True):
		for i in range(100):
			start_time = time.time()

			left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
			self.w= right - left
			self.h= bot - top
			self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
			self.saveDC.SelectObject(self.saveBitMap)
			self.saveDC.BitBlt((0, 0),(self.w, self.h), self.mfcDC, (0, 0), win32con.SRCCOPY)


			bmp = np.fromstring(self.saveBitMap.GetBitmapBits(True), dtype='uint8')
			pil_im = Image.frombuffer('RGB', (self.w, self.h), bmp, 'raw', 'BGRX', 0, 1)

			pil_array = np.array(pil_im)
			frame = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)

			video.write(frame)

			end_time = time.time()
			print("WorkingTime: {} sec".format(end_time-start_time))
		#except Exception as err:
		#	print(err)

		video.release()
		cv2.destroyAllWindows()
		print("end")
		