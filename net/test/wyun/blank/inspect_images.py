from net.wyun.blankanswer.loader import DataSetLoader
import cv2

'''
program to check all images in the imageDir folder
and find out which images has no answer in it
'''

imageDir = "/home/michael/Documents/hope-equation-ocr/blank_answers"
dsl = DataSetLoader.DataSetLoader(None)
from imutils import paths
imagePaths = list(paths.list_images(imageDir))

#dsl.stats(imagePaths)
images, labels = dsl.load(imagePaths)

Threshold = 1.55765263459e-05

blank_list = []

for (i, img) in enumerate(images):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret2, th2 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
    print ret2
    mask_inv = cv2.bitwise_not(th2)

    # calculate moments of binary image
    M = cv2.moments(mask_inv)
    # print M

    # calculate x,y coordinate of center
    if M["m00"] == 0:
        print "m00 is 0", labels[i]
        continue

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    print cX, cY
    nu02 = M["nu02"]
    print "nu02", nu02
    if nu02 < Threshold:
        blank_list.append(labels[i])
        print "blank answer: ", i, labels[i]

for ipath in blank_list:
    print ipath