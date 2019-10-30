import cv2
import numpy as np

# def removeNoiseAndSmooth(image):
#   img = image
#   filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 41)
#   kernel = np.ones((1, 1), np.uint8)
#   opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
#   closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
#   img = image_smoothening(img)
#   or_image = cv2.bitwise_or(img, closing)
#   return or_image

def blurImage(image):
  clear = cv2.fastNlMeansDenoisingColored(image,None,20,10,7,21)
  return clear

def blurGrayImage(image):
  clear = cv2.fastNlMeansDenoising(image,None,20,10,7,21)
  return clear

def convert_to_binary(img_grayscale, thresh=100):
  #   img_binary = cv2.adaptiveThreshold(img_grayscale, 
  #                                      maxValue=255, 
  #                                      adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
  #                                      thresholdType=cv2.THRESH_BINARY,
  #                                      blockSize=15,
  #                                      C=8)
  rect, img_binary = cv2.threshold(img_grayscale,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  return img_binary

def sharpeningImage(image):
  kernel_sharpening = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])
  sharpened = cv2.filter2D(image, -1, kernel_sharpening)
  return sharpened

def grayImage(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  return gray