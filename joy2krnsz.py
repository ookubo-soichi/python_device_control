# coding: UTF-8
#!/usr/bin/env python
import os, sys, time
import pygame
import pygame.joystick
from pygame.locals import *
import pyautogui as pa

import win32gui
import ctypes
from ctypes import windll, Structure, c_long, byref

hllDll = ctypes.WinDLL ("User32.dll")

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class Point(Structure):
	_fields_ = [("x", c_long), ("y", c_long)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def SetMousePos(x, y):
	ctypes.windll.user32.SetCursorPos(x, y)

def GetMousePos():
	pt = Point()
	windll.user32.GetCursorPos(byref(pt))
	return pt

def debug():
	hwnd = ctypes.windll.user32.GetForegroundWindow()
	print (hwnd)
	l, t, r, b = win32gui.GetWindowRect(hwnd)
	print (l, t, r, b)
	pt = Point()
	windll.user32.GetCursorPos(byref(pt))
	print (pt.x, pt.y)

def SetMousePosClick(x,y):
	rx = (wp[x]-wp['x0'])/(wp['x1']-wp['x0'])
	ry = (wp[y]-wp['y0'])/(wp['y1']-wp['y0'])
	hwnd = ctypes.windll.user32.GetForegroundWindow()
	l, t, r, b = win32gui.GetWindowRect(hwnd)
	SetMousePos(int(l+rx*(r-l)), int(t+ry*(b-t)))
	ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0,0)

def SetMousePosClickOFF():
	ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0,0)

wp = {
	'x0':0,
	'x1':1280,
	'y0':0,
	'y1':745,
	'xauto':1080,
	'yauto':725,
	'xskip':1040,
	'xlog':745,
	'xsave':1120,
	'xload':1160,
	'xsystem':1195,
    'xlog':1260,
    'ylog':695,
}

btn_up = pygame.JOYBUTTONUP
btn_dw = pygame.JOYBUTTONDOWN
hat_mt = pygame.JOYHATMOTION
axs_mt = pygame.JOYAXISMOTION

A = 0x1E
B = 0x30
C = 0x2E
D = 0x20
E = 0x12
F = 0x21
G = 0x22
H = 0x23
I = 0x17
J = 0x24
K = 0x25
L = 0x26
M = 0x32
N = 0x31
O = 0x18
P = 0x19
Q = 0x10
R = 0x13
S = 0x1F
T = 0x14
U = 0x16
V = 0x2F
W = 0x11
X = 0x2D
Y = 0x15
Z = 0x2C
n1 = 0x02
n2 = 0x03
n3 = 0x04
n4 = 0x05
n5 = 0x06
n6 = 0x07
n7 = 0x08
n8 = 0x09
n9 = 0x0A
n0 = 0x0B
enter = 0x1C
space = 0x39
tab = 0x0F
up = 0xC8
down = 0xD0
left = 0xCB
right = 0xCD
pageup = 0xC9
pagedown = 0xD1
Shift = 0x2A
Ctrl = 0x1D
F1 = 0x3B
F2 = 0x3C
F3 = 0x3D
F4 = 0x3E
F5 = 0x3F
F6 = 0x40
F7 = 0x41
F8 = 0x42
F9 = 0x43
F10 = 0x44
F11 = 0x57
F12 = 0x58

pygame.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0)
j.init()
print ('Joystick Name   : ' + j.get_name())
print ('Joystick Number : ' + str(j.get_numbuttons()))

mouse_vel_x1 = 0
mouse_vel_y1 = 0
mouse_vel_x2 = 0
mouse_vel_y2 = 0
mouse_vel_coef1 = 10
mouse_vel_coef2 = 5
up_hold = False
down_hold = False
left_hold = False
right_hold = False
space_hold = False
tab_hold = False
enter_hold = False
isSet = False
prevTrigger2 = 0.0
prevTrigger5 = 0.0
going = True

while 1:
	for e in pygame.event.get():
		print ('event : ' + str(e))
		if e.type == btn_up or e.type == btn_dw:
			print (str(e.type)+' : ' + str(e.button))
		# change isSet
		if e.type == btn_dw:
			if e.button == 4:
				isSet = True
				debug()
		if e.type == btn_up:
			if e.button == 4:
				isSet = False
		# message log
		if e.type == btn_dw:
			if e.button == 5:
				SetMousePosClick('xlog','ylog')
		if e.type == btn_up:
			if e.button == 5:
				SetMousePosClickOFF()
		# right click/quick load
		if e.type == btn_dw:
			if e.button == 1:
				if isSet:
					SetMousePosClick('xload','yauto')
				else:
					ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0,0)
		if e.type == btn_up:
			if e.button == 1:
				if isSet:
					SetMousePosClickOFF()
				else:
					ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0,0)
		# left click/quick save
		if e.type == btn_dw:
			if e.button == 2:
				if isSet:
					SetMousePosClick('xsave','yauto')
				else:
					ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0,0)
		if e.type == btn_up:
			if e.button == 2:
				if isSet:
					SetMousePosClickOFF()
				else:
					ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0,0)
		# volume up/save
		if e.type == btn_dw:
			if e.button == 3:
				if isSet:
					SetMousePosClick('xsave','yauto')
				else:
					pa.press('volumeup')
		if e.type == btn_up:
			if e.button == 3:
				if isSet:
					SetMousePosClickOFF()
				else:
					pass
		# volume down/load
		if e.type == btn_dw:
			if e.button == 0:
				if isSet:
					SetMousePosClick('xload','yauto')
				else:
					pa.press('volumedown')
		if e.type == btn_up:
			if e.button == 0:
				if isSet:
					SetMousePosClickOFF()
				else:
					pass
		# full screen/skip
		if e.type == btn_dw:
			if e.button == 6:
				if isSet:
					SetMousePosClick('xskip','yauto')
				else:
					pa.hotkey('alt', 'enter')
		if e.type == btn_up:
			if e.button == 6:
				if isSet:
					SetMousePosClickOFF()
				else:
					pass
		# auto/close
		if e.type == btn_dw:
			if e.button == 7:
				if isSet:
					pa.hotkey('alt', 'f4')
				else:
					SetMousePosClick('xauto','yauto')
		if e.type == btn_up:
			if e.button == 7:
				if isSet:
					SetMousePosClickOFF()
				else:
					pass
		if e.type == hat_mt:
			if e.value[1] == 1:
				PressKey(up)
				up_hold = True
			if e.value[1] == -1:
				PressKey(down)
				down_hold = True
			if e.value[0] == 1:
				PressKey(right)
				right_hold = True
			if e.value[0] == -1:
				PressKey(left)
				left_hold = True
			if e.value[0] == 0 and e.value[1] == 0:
				if up_hold:
					ReleaseKey(up)
					up_hold = False
				if down_hold:
					ReleaseKey(down)
					down_hold = False
				if right_hold:
					ReleaseKey(right)
					right_hold = False
				if left_hold:
					ReleaseKey(left)
					left_hold = False
			print (str(e.type)+' : '+str(e.value[0])+' : '+str(e.value[1]))
		if e.type == axs_mt:
			if e.axis == 0 or e.axis == 1:
				if abs(j.get_axis(0)) >= 0.1:
					if isSet:
						mouse_vel_x1 = mouse_vel_coef2 * j.get_axis(0)
					else:
						mouse_vel_x1 = mouse_vel_coef1 * j.get_axis(0)
				else:
					mouse_vel_x1 = 0
				if abs(j.get_axis(1)) >= 0.1:
					if isSet:
						mouse_vel_y1 = mouse_vel_coef1 * j.get_axis(1)
					else:
						mouse_vel_y1 = mouse_vel_coef2 * j.get_axis(1)
				else:
					mouse_vel_y1 = 0
			if e.axis == 3 or e.axis == 4:
				if abs(j.get_axis(3)) >= 0.1:
					mouse_vel_x2 = mouse_vel_coef2 * j.get_axis(3)
				else:
					mouse_vel_x2 = 0
				if abs(j.get_axis(4)) >= 0.1:
					mouse_vel_y2 = mouse_vel_coef2 * j.get_axis(4)
				else:
					mouse_vel_y2 = 0
			# space/tab/enter
			if e.axis == 2 or e.axis == 5:
				if prevTrigger5 < 0.9 and j.get_axis(5) >= 0.9:
					if isSet:
						#SetMousePosClick('xsystem','yauto')
						tab_hold = True
					else:
						#SetMousePosClick('xvoice','yauto')
						enter_hold = True
				if tab_hold:
					#SetMousePosClickOFF()
					tab_hold = False
				if enter_hold:
					#SetMousePosClickOFF()
					enter_hold = False
				if prevTrigger2 < 0.9 and j.get_axis(2) >= 0.9:
					#SetMousePosClick('xhide','yauto')
					space_hold = True
				if space_hold:
					#SetMousePosClickOFF()
					space_hold = False
				prevTrigger2 = j.get_axis(2)
				prevTrigger5 = j.get_axis(5)
			print (str(e.type)+' : '+str(e.axis)+' : '+str(e.value))
			print (str(j.get_axis(0))+' : '+str(j.get_axis(1))+' : '+str(j.get_axis(3))+' : '+str(j.get_axis(2))+' : '+str(j.get_axis(4))+' : '+str(j.get_axis(5)))
	base_pos = GetMousePos()
	SetMousePos(int(base_pos.x + mouse_vel_x1 + mouse_vel_x2), int(base_pos.y + mouse_vel_y1 + mouse_vel_y2))
	time.sleep(0.01)
