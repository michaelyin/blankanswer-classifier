
'''
program to process one image and find out its attributes.
'''
import cv2
import json

img_base_dir = '/home/michael/Documents/hope-equation-ocr/blank_answers/blankarea/' #'/document/ocr/im2text/images/'
img_name = '02260148.jpg' #'1491361705634_1.png'
img_name = '02262249.jpg'
img_name = '0990alb.jpg'
img = cv2.imread(img_base_dir + img_name)

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret2,th2 = cv2.threshold(gray_image,0,255,cv2.THRESH_OTSU)
print ret2
mask_inv = cv2.bitwise_not(th2)

# calculate moments of binary image
M = cv2.moments(mask_inv)
#print M

# calculate x,y coordinate of center
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

print cX, cY
print "nu02", M["nu02"]

# put text and highlight the center
cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
cv2.putText(img, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# calculate x,y coordinate of center

cv2.imshow('orig', img)

cv2.imshow('gray', gray_image)

cv2.imshow('bin', th2)

cv2.waitKey(0)
cv2.destroyAllWindows()