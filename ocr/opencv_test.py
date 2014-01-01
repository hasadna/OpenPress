from cv2.cv import *
image = LoadImage("/Users/asafvaladarsky/Documents/pic.png")
NamedWindow("opencv")
ShowImage("opencv",image)
WaitKey(0)