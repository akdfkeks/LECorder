import win32gui
import win32ui


def findWindow(winname):
	hwnd = win32gui.FindWindow(None, winname)
	if hwnd >=1:
		try:
			left, top, right, bot = win32gui.GetWindowRect(hwnd)
			w= right - left
			h=bot -top
			hwndDC = win32gui.GetWindowDC(hwnd)
			mfcDC = win32ui.CreateDCFromHandle(hwndDC)
			saveDC = mfcDC.CreateCompatibleDC()
			#result = windll.
		except:
			return False