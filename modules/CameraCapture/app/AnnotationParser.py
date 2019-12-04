# To make python 2 and python 3 compatible code
from __future__ import absolute_import

# Returns rectangle boundaries in the CV2 format (topLeftX, topLeftY, bottomRightX, bottomRightY) given by a processing service


class AnnotationParser:
    def getCV2RectanglesFromProcessingService1(self, response):
        try:
            listOfCV2Rectangles = []
            for item in response["regions"]:
                for decoration in item:
                    if "box" in decoration.lower():
                        rectList = item[decoration].split(",")
                        top = int(rectList[0])
                        left = int(rectList[1])
                        width = int(rectList[2])
                        height = int(rectList[3])
                        for decorationProperty in item[decoration]:
                            if "top" in decorationProperty.lower():
                                top = int(item[decoration][decorationProperty])
                            if "left" in decorationProperty.lower():
                                left = int(item[decoration]
                                           [decorationProperty])
                            if "width" in decorationProperty.lower():
                                width = int(item[decoration]
                                            [decorationProperty])
                            if "height" in decorationProperty.lower():
                                height = int(item[decoration]
                                             [decorationProperty])
                        if top is not None and left is not None and width is not None and height is not None:
                            topLeftX = left
                            topLeftY = top
                            bottomRightX = left + width
                            bottomRightY = top + height
                            listOfCV2Rectangles.append(
                                [topLeftX, topLeftY, bottomRightX, bottomRightY])
            return listOfCV2Rectangles
        except:
            # Ignoring exceptions for now so that video can be read and analyzed without post-processing in case of errors
            pass

    def getCV2RectanglesFromProcessingService2(self, response):
        try:
            listOfCV2Rectangles = []
            for item in response:
                for decoration in item:
                    if "rect" in decoration.lower():
                        for decorationProperty in item[decoration]:
                            if "top" in decorationProperty.lower():
                                top = int(item[decoration][decorationProperty])
                            if "left" in decorationProperty.lower():
                                left = int(item[decoration]
                                           [decorationProperty])
                            if "width" in decorationProperty.lower():
                                width = int(item[decoration]
                                            [decorationProperty])
                            if "height" in decorationProperty.lower():
                                height = int(item[decoration]
                                             [decorationProperty])
                        if top is not None and left is not None and width is not None and height is not None:
                            topLeftX = left
                            topLeftY = top
                            bottomRightX = left + width
                            bottomRightY = top + height
                            listOfCV2Rectangles.append(
                                [topLeftX, topLeftY, bottomRightX, bottomRightY])
            return listOfCV2Rectangles
        except:
            # Ignoring exceptions for now so that video can be read and analyzed without post-processing in case of errors
            pass
