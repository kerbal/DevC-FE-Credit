import cv2
import urllib
import numpy as np
from google.colab.patches import cv2_imshow

def URLtoImage(url):
  resp = urllib.request.urlopen(url)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  return image

def displayImage(image):
  cv2_imshow(image)