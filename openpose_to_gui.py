# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 05:37:13 2019

"""

import win32gui
import win32ui
import win32con
from time import sleep
import  win32com.client



toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

firefox = [(hwnd, title) for hwnd, title in winlist if 'openpose' in title.lower()]
# just grab the hwnd for first window matching firefox
firefox = firefox[0]
hwnd = firefox[0]



#def _get_windows_bytitle(title_text, exact = False):
#    def _window_callback(hwnd, all_windows):
#        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
#    windows = []
#    win32gui.EnumWindows(_window_callback, windows)
#    if exact:
#        return [hwnd for hwnd, title in windows if title_text == title]
#    else:
#        return [hwnd for hwnd, title in windows if title_text in title]
#
#
#hwnd = _get_windows_bytitle('OpenPose', exact = False)
#hwnd=hwnd[0]

if not hwnd:
    hwnd=win32gui.GetDesktopWindow()
    
    
#shell = win32com.client.Dispatch("WScript.Shell")
#shell.SendKeys('%')
    
l,t,r,b=win32gui.GetWindowRect(hwnd)
h=b-t
w=r-l
hDC = win32gui.GetWindowDC(hwnd)
myDC=win32ui.CreateDCFromHandle(hDC)
newDC=myDC.CreateCompatibleDC()

myBitMap = win32ui.CreateBitmap()
myBitMap.CreateCompatibleBitmap(myDC, w, h)

newDC.SelectObject(myBitMap)



win32gui.SetForegroundWindow(hwnd)
sleep(.2) #lame way to allow screen to draw before taking shot
newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
myBitMap.Paint(newDC)
myBitMap.SaveBitmapFile(newDC,'G:\\Pakistan Sign Language Recognition and Translation Using Webcam\\tmp.bmp')


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
