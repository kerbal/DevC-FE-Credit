import cv2
import urllib
import numpy as np
from io import StringIO
import base64
from PIL import Image
import io
from services.filter import resizeImage
import random

def readURL(url):
  resp = urllib.request.urlopen(url)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  return image

def readFromPath(path):
  image = cv2.imread(path)
  if image.shape[1] > 1920:
    return resizeImage(image, 1920 / image.shape[1] * 100)
  else:
    return image

def readb64(base64_string):
  imgdata = base64.b64decode(str(base64_string))
  image = Image.open(io.BytesIO(imgdata))
  image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

  if image.shape[1] > 1920:
    return resizeImage(image, 1920 / image.shape[1] * 100)
  else:
    return image

def toBase64Byte(image):
  success, encoded_image = cv2.imencode('.png', image)
  return base64.decodebytes(base64.b64encode(encoded_image))

def displayImage(image):
  cv2.imwrite('./{}.jpg'.format(random.randint(0, 1000)), image)

def toBase64(image):
  a, b = cv2.imencode('.jpg', image)
  image = base64.b64encode(b)
  return image