import cv2
import services.filter as filter
from services.imageReader import readFromPath, displayImage
import numpy as np
from services.googleVision import OCR

def get_quochuy(img):
  h = img.shape[0]
  w = img.shape[1]
  quochuy = img[round((0.9/15)*h):round((5.6/15)*h), round((1/15)*w):round((4.2/15)*w)]
  quochuy = crop_quoc_huy(quochuy)
  return quochuy

def crop_quoc_huy(img):
  temp = filter.denoise(img.copy())
  temp = filter.advancedEqualizeHistForQ(temp)
  temp = filter.denoiseGray(temp)
  temp = filter.binarize(temp)
  retval, temp = cv2.threshold(temp, thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)
  contours, hierarchy = cv2.findContours(temp, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  # cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

  mx = (0, 0, 0, 0)
  mx_area = 0
  for cont in contours:
    x, y, w, h = cv2.boundingRect(cont)
    area = w * h
    if area > mx_area:
      mx = x, y, w, h
      mx_area = area
  x, y, w, h = mx
  roi = img[y : y + h, x : x + w]
  return roi

def unsharp_mask_quochuy(image, kernel_size=(5, 5), sigma=2.0, amount=5, threshold=0):
  blurred = cv2.GaussianBlur(image, kernel_size, sigma)
  sharpened = float(amount + 1) * image - float(amount) * blurred
  sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
  sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
  sharpened = sharpened.round().astype(np.uint8)
  if threshold > 0:
    low_contrast_mask = np.absolute(image - blurred) < threshold
    np.copyto(sharpened, image, where=low_contrast_mask)
  return sharpened

def template_match(img, template):
  img2 = img.copy()
  h = template.shape[0]
  w = template.shape[1]
  methods = ['cv2.TM_CCOEFF_NORMED']

  for meth in methods:
      img = img2.copy()
      method = eval(meth)
  
  res = cv2.matchTemplate(img,template,method)
  
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
  
  return max_val

def compare_quochuy(img1):
  img1 = filter.resizeImage(img1, 1323 / img1.shape[1] * 100)
  img1 = get_quochuy(img1)
  img1 = unsharp_mask_quochuy(img1)
  img1 = filter.denoise(img1)
  #Quốc huy chuẩn
  quochuygoc = readFromPath('./pictures/quoc huy.png')
  # quochuygoc = cv2.cvtColor(quochuygoc, cv2.COLOR_BGR2RGB)
  h = quochuygoc.shape[0]
  w = quochuygoc.shape[1]

  #Resize quốc huy CMND bằng hoặc lớn hơn quốc huy chuẩn
  img1 = cv2.resize(img1, (w,h), interpolation = cv2.INTER_AREA)
  
  confidenceSum = 0 #Tổng tỉ lệ
  sum = 0 #Tổng

  #Nếu template match toàn bộ quốc huy <0.5 thì dừng, trả về
  temp = template_match(img1, quochuygoc)
  if (temp < 0.5):
    return temp

  #Template matching theo grid m
  m = 3
  for x in range(0,m):
    for y in range(0,m):
      crop1 = quochuygoc[round((x/m)*h):round((x/m)*h) + round((1/m)*h), round((y/m)*w):round((y/m)*w) + round((1/m)*w)]
      crop2 = img1[round((x/m)*h):round((x/m)*h) + round((1/m)*h), round((y/m)*w):round((y/m)*w) + round((1/m)*w)]
      temp = template_match(crop2, crop1)

    

      if (temp < 0.5 and temp > 0.4):
        sum += 2
        confidenceSum += temp
      elif (temp < 0.4 and temp > 0.3):
        sum += 4
        confidenceSum += temp
      elif (temp < 0.3 and temp > 0.2):
        sum += 8
        confidenceSum += temp
      elif (temp < 0.2 and temp > 0.1):
        sum += 16
        confidenceSum += temp
      elif (temp < 0.1):
        sum += 32
        confidenceSum += temp
      else :
        sum += 1
        confidenceSum += temp

  # displayImage(img1)
  return confidenceSum / sum, img1

def compare_tieude(img):
  img = filter.resizeImage(img, 1323 / img.shape[1] * 100)
  #preprocess
  img_ocr = img[int(img.shape[0] * 0.01) : int(img.shape[0] * 0.25), int(img.shape[1] * 0.3) : int(img.shape[1] * 0.98)]
  img_ocr = filter.denoise(img_ocr)

  cmnd = img_ocr
  # cmnd = cv2.cvtColor(cmnd, cv2.COLOR_BGR2RGB)

  img_ocr = filter.advancedEqualizeHist(img_ocr)
  img_ocr = filter.denoiseGray(img_ocr)
  img_ocr = filter.sharpen(img_ocr)
  
  confidenceSum = 0
  sum = 0
    
  texts = OCR(img_ocr, True)

  quocngu_ocr = ''

  k = 1
  for i in range(k, len(texts)):
    if (texts[i].description == "CỘNG"):
      k = i
      break
  
  for i in range(k, k + 8):
    quocngu_ocr += texts[i].description
  # print(quocngu_ocr)
  if (quocngu_ocr != "CỘNGHÒAXÃHỘICHỦNGHĨAVIỆTNAM"):
    confidenceQuocngu = 0

  else:
    # print(texts[k].bounding_poly.vertices[0].y, texts[k+7].bounding_poly.vertices[2].y, texts[k].bounding_poly.vertices[0].x, texts[k+7].bounding_poly.vertices[2].x)
    quocngu_crop = cmnd[texts[k].bounding_poly.vertices[0].y: texts[k+7].bounding_poly.vertices[2].y, texts[k].bounding_poly.vertices[0].x:texts[k+7].bounding_poly.vertices[2].x]
    # displayImage(quocngu_crop)
    #Lấy quốc ngữ chuẩn và các chữ trong quốc ngữ
    # print(quocngu_crop)
    quocngu_goc = readFromPath('./pictures/quoc ngu.jpg')
    quocngu_words = []
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], 0:int(quocngu_goc.shape[1]*0.19)])
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], int(quocngu_goc.shape[1]*0.19):int(quocngu_goc.shape[1]*0.3)])
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], int(quocngu_goc.shape[1]*0.3):int(quocngu_goc.shape[1]*0.37)])
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], int(quocngu_goc.shape[1]*0.37):int(quocngu_goc.shape[1]*0.47)])
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], int(quocngu_goc.shape[1]*0.47):int(quocngu_goc.shape[1]*0.57)])
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], int(quocngu_goc.shape[1]*0.57):int(quocngu_goc.shape[1]*0.73)])
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], int(quocngu_goc.shape[1]*0.73):int(quocngu_goc.shape[1]*0.85)])
    quocngu_words.append(quocngu_goc[0:quocngu_goc.shape[0], int(quocngu_goc.shape[1]*0.85):quocngu_goc.shape[1]])
    
    for i in range(k, k + 8):
      top_left_x = texts[i].bounding_poly.vertices[0].x
      top_left_y = texts[i].bounding_poly.vertices[0].y

      bot_right_x = texts[i].bounding_poly.vertices[2].x
      bot_right_y = texts[i].bounding_poly.vertices[2].y

      word = cmnd[top_left_y: bot_right_y, top_left_x: bot_right_x]
      # displayImage(word)
      if (quocngu_words[i-k].shape[0] < word.shape[0] or quocngu_words[i-k].shape[1] < word.shape[1]):
        temp = 0
      else:
        temp = template_match(quocngu_words[i - k], word)

      # print(temp)
      if temp < 0.5:
        cv2.rectangle(cmnd,(top_left_x,top_left_y),(bot_right_x,bot_right_y),(0,0,255),1)
        
      if (temp < 0.5 and temp > 0.4):
        sum += 2
        confidenceSum += temp
      elif (temp < 0.4 and temp > 0.3):
        sum += 4
        confidenceSum += temp
      elif (temp < 0.3 and temp > 0.2):
        sum += 8
        confidenceSum += temp
      elif (temp < 0.2 and temp > 0.1):
        sum += 16
        confidenceSum += temp
      elif (temp < 0.1):
        sum += 32
        confidenceSum += temp
      else :
        sum += 1
        confidenceSum += temp
      
    confidenceQuocngu = confidenceSum/sum

  # print('Quoc ngu: ', confidenceQuocngu)
  confidenceSum = 0
  sum = 0

  #Tiêu ngữ __________________________________________

  tieungu_ocr = ''

  for i in range(k, len(texts)):
    if(texts[i].description == "Độc"):
      k = i
      break
  
  for i in range(k, k + 8):
    tieungu_ocr += texts[i].description

  if (tieungu_ocr != "Độclập-Tựdo-Hạnhphúc"):
    confidenceTieungu = 0
  else:
    tieungu_crop = cmnd[texts[k].bounding_poly.vertices[0].y: texts[k+7].bounding_poly.vertices[2].y, texts[k].bounding_poly.vertices[0].x:texts[k+7].bounding_poly.vertices[2].x]

    #Lấy tiêu ngữ chuẩn và các chữ trong tiêu ngữ

    tieungu_goc = readFromPath('./pictures/tieu ngu.jpg')
    tieungu_words = []
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], 0:int(tieungu_goc.shape[1]*0.17)])
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], int(tieungu_goc.shape[1]*0.17):int(tieungu_goc.shape[1]*0.29)])
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], int(tieungu_goc.shape[1]*0.29):int(tieungu_goc.shape[1]*0.34)])
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], int(tieungu_goc.shape[1]*0.34):int(tieungu_goc.shape[1]*0.45)])
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], int(tieungu_goc.shape[1]*0.45):int(tieungu_goc.shape[1]*0.55)])
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], int(tieungu_goc.shape[1]*0.55):int(tieungu_goc.shape[1]*0.6)])
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], int(tieungu_goc.shape[1]*0.6):int(tieungu_goc.shape[1]*0.8)])
    tieungu_words.append(tieungu_goc[0:tieungu_goc.shape[0], int(tieungu_goc.shape[1]*0.8):tieungu_goc.shape[1]])

    for i in range(k, k + 8):

      top_left_x = texts[i].bounding_poly.vertices[0].x
      top_left_y = texts[i].bounding_poly.vertices[0].y

      bot_right_x = texts[i].bounding_poly.vertices[2].x
      bot_right_y = texts[i].bounding_poly.vertices[2].y

      word = cmnd[top_left_y: bot_right_y, top_left_x: bot_right_x]

      if (tieungu_words[i-k].shape[0] < word.shape[0] or tieungu_words[i-k].shape[1] < word.shape[1]):
        temp = 0
      else:
        temp = template_match(tieungu_words[i - k], word)

      if temp < 0.5:
        cv2.rectangle(cmnd,(top_left_x,top_left_y),(bot_right_x,bot_right_y),(0,0,255),1)

      if (temp < 0.5 and temp > 0.4):
        sum += 2
        confidenceSum += temp
      elif (temp < 0.4 and temp > 0.3):
        sum += 4
        confidenceSum += temp
      elif (temp < 0.3 and temp > 0.2):
        sum += 8
        confidenceSum += temp
      elif (temp < 0.2 and temp > 0.1):
        sum += 16
        confidenceSum += temp
      elif (temp < 0.1):
        sum += 32
        confidenceSum += temp
      else :
        sum += 1
        confidenceSum += temp
      
    confidenceTieungu = confidenceSum/sum

  # print('Final tieu ngu:', confidenceTieungu)

  confidenceSum = 0
  sum = 0

  #Giấy CMND __________________________________________

  cmnd_ocr = ''

  for i in range(k, len(texts)):
    if(texts[i].description == "GIẤY"):
      k = i
      break
  
  for i in range(k, k + 5):
    cmnd_ocr += texts[i].description

  if (cmnd_ocr != "GIẤYCHỨNGMINHNHÂNDÂN"):
    confidenceTengiay = 0
  else:

    tengiay_crop = cmnd[texts[k].bounding_poly.vertices[0].y: texts[k+4].bounding_poly.vertices[2].y, texts[k].bounding_poly.vertices[0].x:texts[k+4].bounding_poly.vertices[2].x]

    #Lấy tiêu ngữ chuẩn và các chữ trong tiêu ngữ

    tengiay_goc = readFromPath('./pictures/tieu de.jpg')
    tengiay_goc = cv2.cvtColor(tengiay_goc, cv2.COLOR_BGR2RGB)
    
    tengiay_words = []
    tengiay_words.append(tengiay_goc[0:tengiay_goc.shape[0], 0:int(tengiay_goc.shape[1]*0.2)])
    tengiay_words.append(tengiay_goc[0:tengiay_goc.shape[0], int(tengiay_goc.shape[1]*0.2):int(tengiay_goc.shape[1]*0.43)])
    tengiay_words.append(tengiay_goc[0:tengiay_goc.shape[0], int(tengiay_goc.shape[1]*0.43):int(tengiay_goc.shape[1]*0.62)])
    tengiay_words.append(tengiay_goc[0:tengiay_goc.shape[0], int(tengiay_goc.shape[1]*0.62):int(tengiay_goc.shape[1]*0.81)])
    tengiay_words.append(tengiay_goc[0:tengiay_goc.shape[0], int(tengiay_goc.shape[1]*0.81):tengiay_goc.shape[1]])

    for i in range(k, k + 5):
      top_left_x = texts[i].bounding_poly.vertices[0].x
      top_left_y = texts[i].bounding_poly.vertices[0].y

      bot_right_x = texts[i].bounding_poly.vertices[2].x
      bot_right_y = texts[i].bounding_poly.vertices[2].y
      
      word = cmnd[top_left_y: bot_right_y, top_left_x: bot_right_x]

      if (tengiay_words[i-k].shape[0] < word.shape[0] or tengiay_words[i-k].shape[1] < word.shape[1]):
        temp = 0
      else:
        temp = template_match(tengiay_words[i - k], word)

      # print(temp)
      if temp < 0.5:
        cv2.rectangle(cmnd,(top_left_x,top_left_y),(bot_right_x,bot_right_y),(0,0,255),1)

      if (temp < 0.5 and temp > 0.4):
        sum += 2
        confidenceSum += temp
      elif (temp < 0.4 and temp > 0.3):
        sum += 4
        confidenceSum += temp
      elif (temp < 0.3 and temp > 0.2):
        sum += 8
        confidenceSum += temp
      elif (temp < 0.2 and temp > 0.1):
        sum += 16
        confidenceSum += temp
      elif (temp < 0.1):
        sum += 32
        confidenceSum += temp
      else :
        sum += 1
        confidenceSum += temp
        
    confidenceTengiay = confidenceSum/sum
  displayImage(cmnd)
  return confidenceQuocngu, confidenceTengiay, confidenceTieungu, cmnd