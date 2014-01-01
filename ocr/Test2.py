import cv2
import os
import numpy as np
import cPickle

CVCONTOUR_APPROX_LEVEL = 2
CVCLOSE_ITR = 1

def main():
    mask = cv2.imread('/Users/asafvaladarsky/Documents/pic3.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    findConnectedComponents(mask)

def findConnectedComponents(mask,
                            poly1Hull0 = 1,
                            perimScale = 4,
                            num = None,
                            bbs = None,
                            centers = None):
    cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.array(0), iterations=CVCLOSE_ITR)
    cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.array(0), iterations=CVCLOSE_ITR)
    
    contours,hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(mask, contours, -1, (255,0,0), 1 )
    
    #the Pickle trick solves some strange type errors
    tmp = cPickle.dumps(contours)
    contours = cPickle.loads(tmp)



    for contour in contours:
        perimeter = cv2.arcLength(contour, True)

if __name__ == '__main__':
    main()
    print 'done'



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
