#-*-coding:utf-8
import win32gui
import win32ui
import win32con

def background_screenshot(hwnd, width, height):
    hwndDC = win32gui.GetWindowDC(hwnd)
	
    mfcDC=win32ui.CreateDCFromHandle(hwndDC)
    saveDC=mfcDC.CreateCompatibleDC()
	
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
	
    saveDC.BitBlt((0,0),(width, height) , mfcDC, (0,0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, 'screenshot.bmp')
    mfcDC.DeleteDC()
    saveDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    win32gui.DeleteObject(saveBitMap.GetHandle())

hwnd = win32gui.FindWindow(None, "Discord")
background_screenshot(hwnd, 1280, 720)