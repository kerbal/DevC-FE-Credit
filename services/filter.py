import cv2
import numpy as np

def grayScale(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  return gray

def denoise(image):
  clear = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
  return clear  

def sharpen(image):
  kernel_sharpening = np.array([[-1,-1,-1], 
                                [-1, 9,-1],
                                [-1,-1,-1]])
  sharpened = cv2.filter2D(image, -1, kernel_sharpening)
  return sharpened

def denoiseGray(gray):
  return cv2.GaussianBlur(gray, (5, 5), 0)

def binarize(img_grayscale, thresh=100):
  img_binary = cv2.adaptiveThreshold(img_grayscale, 
                                    maxValue=255, 
                                    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    thresholdType=cv2.THRESH_BINARY,
                                    blockSize=15,
                                    C=8)
  return img_binary

def advancedEqualizeHist(image):
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4,4))
  cl1 = clahe.apply(grayScale(image))
  return cl1

def resizeImage(image, scalePercent):
  width = int(image.shape[1] * scalePercent / 100)
  height = int(image.shape[0] * scalePercent / 100)
  dim = (width, height)
  return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)