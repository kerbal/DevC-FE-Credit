import cv2
import numpy as np 
import services.filter as filter

def findContour(image):
  edged = cv2.Canny(image, 35, 55)
  cnts, h = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
  screenCnt = None
  for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    if len(approx) == 4:
      screenCnt = approx
      break
  return screenCnt

def orderPoints(pts):
  rect = np.zeros((4, 2), dtype="float32")

  s = pts.sum(axis=1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]

  diff = np.diff(pts, axis=1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]

  return rect

def fourPointTransform(image, pts):
  rect = orderPoints(pts)
  (tl, tr, br, bl) = rect
  
  widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  maxWidth = max(int(widthA), int(widthB))

  heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
  maxHeight = max(int(heightA), int(heightB))

  dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]], dtype="float32")

  M = cv2.getPerspectiveTransform(rect, dst)
  warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
  return warped

def cropContour(image):
  tmp = image.copy()
  tmp = filter.denoise(tmp)
  tmp = filter.advancedEqualizeHist(tmp)
  tmp = filter.denoiseGray(tmp)

  try:
    contour = findContour(tmp)
    points = np.array(contour.reshape(4, 2) * 1)
    image = fourPointTransform(image, points)

    # image = image[int(image.shape[0] * 0.225) : image.shape[0], 
    #               int(image.shape[1] * 0.3) : image.shape[1]]
    return image, True
  except:
    print('Find contour failed!!!')
    return image, False