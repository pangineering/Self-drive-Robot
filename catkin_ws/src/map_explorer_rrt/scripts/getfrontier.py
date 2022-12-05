#!/usr/bin/env python

# MIT License

# Copyright (c) 2021 Mohamed Fazil

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#--------Include modules---------------
from copy import copy
import rospy
from nav_msgs.msg import OccupancyGrid

import numpy as np
import cv2

#-----------------------------------------------------

def getfrontier(mapData):
	data=mapData.data
	w=mapData.info.width
	h=mapData.info.height
	resolution=mapData.info.resolution
	Xstartx=mapData.info.origin.position.x
	Xstarty=mapData.info.origin.position.y
	 
	img = np.zeros((h, w, 1), np.uint8)
	
	for i in range(0,h):
		for j in range(0,w):
			if data[i*w+j]==100:
				img[i,j]=0
			elif data[i*w+j]==0:
				img[i,j]=255
			elif data[i*w+j]==-1:
				img[i,j]=205
	
	
       	o=cv2.inRange(img,0,1)
	edges = cv2.Canny(img,0,255)
	im2, contours, hierarchy = cv2.findContours(o,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(o, contours, -1, (255,255,255), 5)
	o=cv2.bitwise_not(o) 
	res = cv2.bitwise_and(o,edges)
	#------------------------------

	frontier=copy(res)
	im2, contours, hierarchy = cv2.findContours(frontier,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(frontier, contours, -1, (255,255,255), 2)

	im2, contours, hierarchy = cv2.findContours(frontier,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	all_pts=[]
	if len(contours)>0:
		upto=len(contours)-1
		i=0
		maxx=0
		maxind=0
		
		for i in range(0,len(contours)):
				cnt = contours[i]
				M = cv2.moments(cnt)
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				xr=cx*resolution+Xstartx
				yr=cy*resolution+Xstarty
				pt=[np.array([xr,yr])]
				if len(all_pts)>0:
					all_pts=np.vstack([all_pts,pt])
				else:
							
					all_pts=pt
	
	return all_pts


