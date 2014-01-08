import numpy as np
import cv2
import cv2.cv as cv

#im = cv2.imread('/Users/asafvaladarsky/Documents/img/Ad0010401.png')
im = cv2.imread('pic.png')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

invert = 255 - imgray
cv2.imwrite('/Users/asafvaladarsky/Documents/pic1.png', invert)

#ret,thresh = cv2.threshold(invert,0,0,0)
contours, hierarchy = cv2.findContours(invert,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for i in range(0, len(contours)):
    if (i % 2 == 0):
        cnt = contours[i]
        #mask = np.zeros(im2.shape,np.uint8)
        #cv2.drawContours(mask,[cnt],0,255,-1)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(invert,(x,y),(x+w,y+h),(0,255,0),1)



#cv2.drawContours(invert, contours, -1, (255,0,0), 1 )

cv2.imshow('image', invert)
0xFF & cv2.waitKey()
cv2.destroyAllWindows()




'''
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)

#################      Now finding Contours         ###################


contours0, hierarchy = cv2.findContours( im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

def update(levels):
    vis = np.zeros((cvImg.height, cvImg.width, 3), np.uint8)
    levels = levels - 3
    cv2.drawContours( vis, contours, (-1, 3)[levels <= 0], (128,255,255),
        3, cv2.CV_AA, hierarchy, abs(levels) )
    cv2.imshow('contours', vis)
    
update(3)
cv2.createTrackbar( "levels+3", "contours", 3, 7, update )
cv2.imshow('image', img)
0xFF & cv2.waitKey()
cv2.destroyAllWindows()
'''
'''
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]

print len(contours)

for cnt in contours:
    if cv2.contourArea(cnt)>50:
        [x,y,w,h] = cv2.boundingRect(cnt)

        if  h>28:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            cv2.imshow('norm',im)
            key = cv2.waitKey(0)

            if key == 27:
                sys.exit()
            elif key in keys:
                responses.append(int(chr(key)))
                sample = roismall.reshape((1,100))
                samples = np.append(samples,sample,0)
        else:
            print "boho"

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print("training complete")

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)
'''
