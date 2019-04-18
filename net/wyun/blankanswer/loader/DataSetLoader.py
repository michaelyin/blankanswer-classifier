import numpy as np
import cv2
import os
from net.wyun.blankanswer.stats import statsutil

class DataSetLoader:
    def __init__(self, preprocessors=None):
        self.preprocessors = preprocessors

        if self.preprocessors is None:
            self.preprocessors = []

    def load(self, imagePaths, verbose=-1):
        data = []
        labels = []
        # loop over the input images
        for (i, imagePath) in enumerate(imagePaths):
            print 'loading ', imagePath
            image = cv2.imread(imagePath)
            label = 1

            if self.preprocessors is not None:
                for p in self.preprocessors:
                    image = p.preprocess(image)

            data.append(image)
            labels.append(imagePath)

        #return (np.array(data), np.array(labels))
        return (data, labels)

    def stats(self, imagePaths):
        images, labels = self.load(imagePaths)

        heights = []
        widths = []
        print 'total images: ', len(images)
        for image in images:
            height, width, depth =  image.shape
            if width >= height:
                heights.append(height)
                widths.append(width)
                if height > 200:
                    print height, width

        # print out statistics
        print 'height stats: '
        statsutil.print_stats(heights)
        print 'width stats: '
        statsutil.print_stats(widths)


