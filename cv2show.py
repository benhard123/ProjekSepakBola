import cv2
import numpy as np

colorLower = (-2, 100, 100) 
colorUpper = (18, 255, 255) 

cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform 
 	# a series of dilations and erosions to remove any small 
 	# blobs left in the mask 
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
 		cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0: 
 		# find the largest contour in the mask, then use 
 		# it to compute the minimum enclosing circle and 
 		# centroid 
        c = max(cnts, key=cv2.contourArea) 
        ((x, y), radius) = cv2.minEnclosingCircle(c) 
        M = cv2.moments(c) 
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 
        if int(M["m10"] / M["m00"]) > 400:
            print("kanan")
        elif int(M["m10"] / M["m00"]) < 400 and int(M["m10"] / M["m00"]) > 200:
            print("tengah")
        elif int(M["m10"] / M["m00"]) < 200:
            print("kiri")
            
 		# only proceed if the radius meets a minimum size 
        if radius > 10: 
 			# draw the circle and centroid on the frame, 
 			# then update the list of tracked points 
            cv2.circle(frame, (int(x), int(y)), int(radius), 
 				(80, 127, 255), 2)  
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
 	 
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
