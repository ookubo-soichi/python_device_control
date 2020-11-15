# coding: UTF-8
#!/usr/bin/env python
import os, sys, time
import pygame
import pygame.joystick
from pygame.locals import *
import pyautogui as pa

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

enter = 0x1C
space = 0x39
tab = 0x0F
up = 0xC8
down = 0xD0
left = 0xCB
right = 0xCD
pageup = 0xC9
pagedown = 0xD1

pygame.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0)
j.init()

mouse_vel_x1 = 0
mouse_vel_y1 = 0
mouse_vel_x2 = 0
mouse_vel_y2 = 0
mouse_vel_coef1 = 10.0
mouse_vel_coef2 = 5.0
isSet = False
prevTrigger = 0.0
going = True
toggle_speed = True

while 1:
	for e in pygame.event.get():
		print 'event : ' + str(e)
		if e.type == 10 or e.type == 11:
			print str(e.type)+' : ' + str(e.button)
		# change isSet
		if e.type == 10:
			if e.button == 4:
				isSet = True
		if e.type == 11:
			if e.button == 4:
				isSet = False
		# right click/next chapter
		if e.type == 10:
			if e.button == 1:
				if isSet:
					pass
				else:
					ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0,0)
		if e.type == 11:
			if e.button == 1:
				if isSet:
					pa.press('x')
					pa.press('x')
					pa.press('right')
					pa.press('right')
					pa.press('right')
				else:
					ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0,0)
		# left click/prev chapter
		if e.type == 10:
			if e.button == 2:
				if isSet:
					pass
				else:
					ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0,0)
		if e.type == 11:
			if e.button == 2:
				if isSet:
					pass
				else:
					ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0,0)
		# volume up
		if e.type == 10:
			if e.button == 3:
				if isSet:
					pass
				else:
					pass
		if e.type == 11:
			if e.button == 3:
				if isSet:
					pass
				else:
					pa.press('volumeup')
		# volume down
		if e.type == 10:
			if e.button == 0:
				if isSet:
					pass
				else:
					pass
		if e.type == 11:
			if e.button == 0:
				if isSet:
					pass
				else:
					pa.press('volumedown')
		# full screen/x2.5
		if e.type == 10:
			if e.button == 6:
				if isSet:
					pass
				else:
					pass
		if e.type == 11:
			if e.button == 6:
				if isSet:
					pa.press('f11')
				else:
					if toggle_speed:
						pa.press('w')
					else:
						pa.press('q')
		# pause/close
		if e.type == 10:
			if e.button == 7:
				if isSet:
					pa.hotkey('alt', 'f4')
				else:
					pass
		if e.type == 11:
			if e.button == 7:
				if isSet:
					pass
				else:
					pa.press(' ')
		if e.type == 9:
			if e.value[1] == 1:
				PressKey(up)
				time.sleep(0.1)
				ReleaseKey(up)
			if e.value[1] == -1:
				PressKey(down)
				time.sleep(0.1)
				ReleaseKey(down)
			if e.value[0] == 1:
				PressKey(right)
				time.sleep(0.1)
				ReleaseKey(right)
			if e.value[0] == -1:
				PressKey(left)
				time.sleep(0.1)
				ReleaseKey(left)
			print str(e.type)+' : '+str(e.value[0])+' : '+str(e.value[1])
		if e.type == 7:
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
				if abs(j.get_axis(4)) >= 0.1:
					mouse_vel_x2 = mouse_vel_coef2 * j.get_axis(4)
				else:
					mouse_vel_x2 = 0
				if abs(j.get_axis(3)) >= 0.1:
					mouse_vel_y2 = mouse_vel_coef2 * j.get_axis(3)
				else:
					mouse_vel_y2 = 0
			# faster/slower
			if e.axis == 2:
				if prevTrigger <= -0.9 and j.get_axis(2) > -0.9:
					if isSet:
						pass
					else:
						pa.press('s')
				if prevTrigger >= 0.9 and j.get_axis(2) < 0.9:
					if isSet:
						pass
					else:
						pa.press('a')
				prevTrigger = j.get_axis(2)
			print str(e.type)+' : '+str(e.axis)+' : '+str(e.value)
			print str(j.get_axis(0))+' : '+str(j.get_axis(1))+' : '+str(j.get_axis(3))+' : '+str(j.get_axis(2))+' : '+str(j.get_axis(4))
	base_pos = GetMousePos()
	SetMousePos(int(base_pos.x + mouse_vel_x1 + mouse_vel_x2), int(base_pos.y + mouse_vel_y1 + mouse_vel_y2))
	time.sleep(0.01)
