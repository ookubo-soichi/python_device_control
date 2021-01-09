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

def FullScreen(event_type):
	SendClickKeyEvent(event_type, False, False, [F])
def VolumeUp(event_type):
	SendClickKeyEvent(event_type, False, False, ['volumeup'])
def VolumeDown(event_type):
	SendClickKeyEvent(event_type, False, False, ['volumedown'])
def Close(event_type):
	SendClickKeyEvent(event_type, False, False, ['Alt+F4'])
def Next(event_type):
	SendClickKeyEvent(event_type, False, False, [N])
def Prev(event_type):
	SendClickKeyEvent(event_type, False, False, [P])
def Pause(event_type):
	SendClickKeyEvent(event_type, False, False, [space])
def OneMinLater():
    pa.hotkey('ctrl', 'right')
def TenSecLater():
    pa.hotkey('alt', 'right')
def OneMinAgo():
    pa.hotkey('ctrl', 'left')
def TenSecAgo():
    pa.hotkey('alt', 'left')
def ThreeSecLater():
    pa.press('right')
def ThreeSecAgo():
    pa.press('left')
def Faster(i):
    for _i in range(i):
        pa.press(']')
def Slower(i):
    for _i in range(i):
        pa.press('[')
def PresetSpeed(event_type, x):
	if event_type  == btn_dw:
		pa.press('u')
		Faster(int(x*10)-10)

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
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def SetMousePos(x, y):
	ctypes.windll.user32.SetCursorPos(x, y)

def GetMousePos():
	pt = Point()
	windll.user32.GetCursorPos(byref(pt))
	return pt

def PrintMousePos():
	hwnd = ctypes.windll.user32.GetForegroundWindow()
	print (hwnd)
	l, t, r, b = win32gui.GetWindowRect(hwnd)
	print (l, t, r, b)
	pt = Point()
	windll.user32.GetCursorPos(byref(pt))
	print (pt.x, pt.y)

def SetMousePosClick(x, y):
	rx = (float(wp[x])-wp['x0'])/(wp['x1']-wp['x0'])
	ry = (float(wp[y])-wp['y0'])/(wp['y1']-wp['y0'])
	hwnd = ctypes.windll.user32.GetForegroundWindow()
	l, t, r, b = win32gui.GetWindowRect(hwnd)
	SetMousePos(int(l+rx*(r-l)), int(t+ry*(b-t)))
	ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)

def SetMousePosClickOFF():
	ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

def SendClickKeyEvent(event_type, x, y, key):
	if event_type  == btn_dw:
		if key[0] == False and x != False and y != False:
			SetMousePosClick(x, y)
		else:
			if key[0] == 'volumeup':
				pa.press('volumeup')
			elif key[0] == 'volumedown':
				pa.press('volumedown')
			elif key[0] == 'Alt+F4':
				pa.hotkey('alt', 'f4')
			else:
				for _k in key:
					PressKey(_k)
	elif event_type  == btn_up:
		if key[0] == False and x != False and y != False:
			SetMousePosClickOFF()
		else:
			if key[0] in ['volumeup', 'volumedown', 'Alt+F4']:
				pass
			else:
				for _k in key:
					ReleaseKey(_k)

def LeftClick(event_type):
	if event_type  == btn_dw:
		ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
	elif event_type  == btn_up:
		ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

def RightClick(event_type):
	if event_type  == btn_dw:
		ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
	elif event_type  == btn_up:
		ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)

btn_up = pygame.JOYBUTTONUP
btn_dw = pygame.JOYBUTTONDOWN
hat_mt = pygame.JOYHATMOTION
axs_mt = pygame.JOYAXISMOTION

A = 0x1E;B = 0x30;C = 0x2E;D = 0x20;E = 0x12
F = 0x21;G = 0x22;H = 0x23;I = 0x17;J = 0x24
K = 0x25;L = 0x26;M = 0x32;N = 0x31;O = 0x18
P = 0x19;Q = 0x10;R = 0x13;S = 0x1F;T = 0x14
U = 0x16;V = 0x2F;W = 0x11;X = 0x2D;Y = 0x15;Z = 0x2C
n1 = 0x02;n2 = 0x03;n3 = 0x04;n4 = 0x05;n5 = 0x06
n6 = 0x07;n7 = 0x08;n8 = 0x09;n9 = 0x0A;n0 = 0x0B
enter = 0x1C;space = 0x39;tab = 0x0F
up = 0xC8;down = 0xD0;left = 0xCB;right = 0xCD
pageup = 0xC9;pagedown = 0xD1;Shift = 0x2A;Ctrl = 0x1D
F1 = 0x3B;F2 = 0x3C;F3 = 0x3D;F4 = 0x3E;F5 = 0x3F
F6 = 0x40;F7 = 0x41;F8 = 0x42;F9 = 0x43;F10 = 0x44
F11 = 0x57;F12 = 0x58

pygame.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0)
j.init()
print ('Joystick Name   : ' + j.get_name())
print ('Joystick Number : ' + str(j.get_numbuttons()))

mouse_vel_x1 = 0;mouse_vel_y1 = 0;mouse_vel_x2 = 0;mouse_vel_y2 = 0
mouse_vel_coef_l1 = 10;mouse_vel_coef_l2 = 5;mouse_vel_coef_r1 = 5;mouse_vel_coef_r2 = 2
trigger2 = 0;trigger5 = 0;prevTrigger2 = 0.0;prevTrigger5 = 0.0
toggle = False
toggle2 = False

class CycleSkip:
	def __init__(self,skip_length):
		self.skip_length = skip_length
		self.cycle_index = 0
	def cycle_reset(self):
		self.cycle_index = 0
	def cycle_skip(self, offset):
		skip_time = self.skip_length[self.cycle_index]
		if self.cycle_index == 0:
			skip_time += 90
		if self.cycle_index != len(self.skip_length) - 1
			skip_time += offset
		min = skip_time // 60
		sec = int((skip_time % 60)/10)
		for _i in range(min):
			OneMinLater()
		for _i in range(sec):
			TenSecLater()
		self.cycle_index += 1
		if self.cycle_index >= len(self.skip_length):
			self.cycle_index = 0

cycle_skip = CycleSkip([60, 50, 80])

while 1:
	for e in pygame.event.get():
		print ('event : ' + str(e))
		# change toggle
		if e.type == btn_dw:
			if e.button == 4:
				toggle = True
				#PrintMousePos()
		if e.type == btn_up:
			if e.button == 4:
				toggle = False
		# change toggle2
		if e.type == btn_dw:
			if e.button == 8:
				toggle2 = True
		if e.type == btn_up:
			if e.button == 8:
				toggle2 = False
		if e.type in [btn_up, btn_dw]:
			#print (str(e.type)+' : ' + str(e.button))
			# volume down/load
			if e.button == 0:
				VolumeDown(e.type)
			# right click/next
			if e.button == 1:
				if toggle:
					Next(e.type)
					cycle_skip.cycle_reset()
				else:
					RightClick(e.type)
			# left click/prev
			if e.button == 2:
				if toggle:
					Prev(e.type)
					cycle_skip.cycle_reset()
				else:
					LeftClick(e.type)
			# volume up
			if e.button == 3:
				VolumeUp(e.type)
			# cycle skip
			if e.button == 5:
				if e.type == btn_dw:
					if toggle:
						cycle_skip.cycle_skip(-30)
					elif toggle2:
						cycle_skip.cycle_skip(30)
					else:
						cycle_skip.cycle_skip(0)
			# full screen/x2.5
			if e.button == 6:
				if toggle:
					PresetSpeed(e.type, 2.5)
				else:
					FullScreen(e.type)
			# auto/close
			if e.button == 7:
				if toggle:
					Close(e.type)
				else:
					Pause(e.type)
		# later/ago
		if e.type == hat_mt:
			#print (str(e.type)+' : '+str(e.value[0])+' : '+str(e.value[1]))
			if e.value[1] == 1:
				OneMinLater()
			if e.value[1] == -1:
				OneMinAgo()
			if e.value[0] == 1:
				TenSecLater()
			if e.value[0] == -1:
				TenSecAgo()
		# mouce cursor
		if e.type == axs_mt:
			#print (str(e.type)+' : '+str(e.axis)+' : '+str(e.value))
			#print (str(j.get_axis(0))+' : '+str(j.get_axis(1))+' : '+str(j.get_axis(3))
			#		+' : '+str(j.get_axis(2))+' : '+str(j.get_axis(4))+' : '+str(j.get_axis(5)))
			# mouce cursor
			if e.axis == 0 or e.axis == 1:
				if abs(j.get_axis(0)) >= 0.1:
					if toggle:
						mouse_vel_x1 = mouse_vel_coef_l2 * j.get_axis(0)
					else:
						mouse_vel_x1 = mouse_vel_coef_l1 * j.get_axis(0)
				else:
					mouse_vel_x1 = 0
				if abs(j.get_axis(1)) >= 0.1:
					if toggle:
						mouse_vel_y1 = mouse_vel_coef_l2 * j.get_axis(1)
					else:
						mouse_vel_y1 = mouse_vel_coef_l1 * j.get_axis(1)
				else:
					mouse_vel_y1 = 0
			if e.axis == 3 or e.axis == 4:
				if abs(j.get_axis(3)) >= 0.1:
					if toggle:
						mouse_vel_x2 = mouse_vel_coef_r2 * j.get_axis(3)
					else:
						mouse_vel_x2 = mouse_vel_coef_r1 * j.get_axis(3)
				else:
					mouse_vel_x2 = 0
				if abs(j.get_axis(4)) >= 0.1:
					if toggle:
						mouse_vel_y2 = mouse_vel_coef_r2 * j.get_axis(4)
					else:
						mouse_vel_y2 = mouse_vel_coef_r1 * j.get_axis(4)
				else:
					mouse_vel_y2 = 0
			# faster/slower
			if e.axis == 2 or e.axis == 5:
				if prevTrigger5 >= 0.9 and j.get_axis(5) < 0.9:
					if toggle:
						Faster(1)
					else:
						Faster(10)
				if prevTrigger2 >= 0.9 and j.get_axis(2) < 0.9:
					if toggle:
						Slower(1)
					else:
						Slower(10)
				prevTrigger2 = j.get_axis(2)
				prevTrigger5 = j.get_axis(5)
	# mouce cursor
	base_pos = GetMousePos()
	SetMousePos(int(base_pos.x + mouse_vel_x1 + mouse_vel_x2), int(base_pos.y + mouse_vel_y1 + mouse_vel_y2))
	time.sleep(0.01)
