import imageIO
import filter
import contour
import numpy as np
import googleVision

def ocrProcess(image_url):
  image = imageIO.URLtoImage(image_url)
  image_cpy = image.copy()
  screenCnt = contour.findContour(image_cpy)

  pts = np.array(screenCnt.reshape(4, 2) * 1)
  contour.order_points(pts)

  straighten = contour.four_point_transform(image, pts)
  cropped = straighten[0:straighten.shape[0], int(straighten.shape[1] * 0.3) : 764]

  clear = filter.blurImage(cropped)
  gray = filter.grayImage(clear)
  sharp = filter.sharpeningImage(gray)

  return googleVision.OCR(sharp)
