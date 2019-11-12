import cv2
import urllib
import numpy as np
from io import StringIO
import base64
from PIL import Image

def readURL(url):
  resp = urllib.request.urlopen(url)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  return image

def readFromPath(path):
  image = cv2.imread(path)

def readb64(base64_string):
  sbuf = StringIO()
  sbuf.write(base64.b64decode(base64_string))
  pimg = Image.open(sbuf)
  return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

def toBase64Byte(image):
    success, encoded_image = cv2.imencode('.png', image)
    return base64.decodebytes(base64.b64encode(encoded_image))