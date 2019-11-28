from services.contour import findContour, fourPointTransform, orderPoints
import services.filter as filter
from services.imageReader import displayImage
import numpy as np 
from services.googleVision import OCR
import json

def isValidNumber(number):
  if len(number) != 9:
    return False
  try:
    number = int(number)
    return True
  except:
    return False

def isValidName(name):
  return ''.join(name.split()).isalpha()

def isLeapYear(year):
  return (year % 4 ==0 and year % 100 != 0) and year % 400 == 0

def isValidDate(day, month, year):
  monthDay = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  if isLeapYear(year):
    monthDay[2] = 29
  if year <= 1900 or month < 1 or month > 12 or day <= 0 or day > monthDay[month]:
    return False
  return True

def isValidCountry(country):
  countryData = '{"LtsItem":[{"Type":1,"SolrID":"/tien-giang","ID":1,"Title":"Tiền Giang","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":10606},{"Type":1,"SolrID":"/hung-yen","ID":2,"Title":"Hưng Yên","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":11850},{"Type":1,"SolrID":"/ha-noi","ID":3,"Title":"Hà Nội","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":275229},{"Type":1,"SolrID":"/tp-ho-chi-minh","ID":4,"Title":"TP Hồ Chí Minh","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":455810},{"Type":1,"SolrID":"/ca-mau","ID":5,"Title":"Cà Mau","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":10652},{"Type":1,"SolrID":"/dac-lac","ID":6,"Title":"Đắc Lắc","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":11160},{"Type":1,"SolrID":"/nam-dinh","ID":7,"Title":"Nam Định","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":11812},{"Type":1,"SolrID":"/quang-ninh","ID":8,"Title":"Quảng Ninh","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":19284},{"Type":1,"SolrID":"/dak-nong","ID":9,"Title":"Đắk Nông","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":5239},{"Type":1,"SolrID":"/da-nang","ID":10,"Title":"Đà Nẵng","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":39822},{"Type":1,"SolrID":"/hai-duong","ID":11,"Title":"Hải Dương","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":16434},{"Type":1,"SolrID":"/long-an","ID":12,"Title":"Long An","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":18689},{"Type":1,"SolrID":"/ben-tre","ID":13,"Title":"Bến Tre","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":8166},{"Type":1,"SolrID":"/dong-thap","ID":14,"Title":"Đồng Tháp","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":10373},{"Type":1,"SolrID":"/vinh-long","ID":15,"Title":"Vĩnh Long","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":7159},{"Type":1,"SolrID":"/kien-giang","ID":16,"Title":"Kiên Giang","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":17002},{"Type":1,"SolrID":"/tra-vinh","ID":17,"Title":"Trà Vinh","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":5534},{"Type":1,"SolrID":"/soc-trang","ID":18,"Title":"Sóc Trăng","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":6291},{"Type":1,"SolrID":"/bac-ninh","ID":19,"Title":"Bắc Ninh","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":16658},{"Type":1,"SolrID":"/thanh-hoa","ID":20,"Title":"Thanh Hoá","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":23874},{"Type":1,"SolrID":"/vung-tau","ID":21,"Title":"Vũng Tàu","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":18582},{"Type":1,"SolrID":"/dong-nai","ID":22,"Title":"Đồng Nai","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":41294},{"Type":1,"SolrID":"/binh-duong","ID":23,"Title":"Bình Dương","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":42658},{"Type":1,"SolrID":"/thai-nguyen","ID":24,"Title":"Thái Nguyên","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":9423},{"Type":1,"SolrID":"/thai-binh","ID":25,"Title":"Thái Bình","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":10709},{"Type":1,"SolrID":"/can-tho","ID":26,"Title":"Cần Thơ","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":19353},{"Type":1,"SolrID":"/nghe-an","ID":27,"Title":"Nghệ An","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":22504},{"Type":1,"SolrID":"/hue","ID":28,"Title":"Huế","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":9928},{"Type":1,"SolrID":"/binh-phuoc","ID":29,"Title":"Bình Phước","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":10714},{"Type":1,"SolrID":"/quang-nam","ID":30,"Title":"Quảng Nam","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":13675},{"Type":1,"SolrID":"/quang-ngai","ID":31,"Title":"Quảng Ngãi","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":10309},{"Type":1,"SolrID":"/ninh-thuan","ID":32,"Title":"Ninh Thuận","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":4818},{"Type":1,"SolrID":"/lao-cai","ID":33,"Title":"Lào Cai","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":6530},{"Type":1,"SolrID":"/hai-phong","ID":34,"Title":"Hải Phòng","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":43884},{"Type":1,"SolrID":"/an-giang","ID":35,"Title":"An Giang","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":12781},{"Type":1,"SolrID":"/phu-tho","ID":36,"Title":"Phú Thọ","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":9592},{"Type":1,"SolrID":"/tay-ninh","ID":37,"Title":"Tây Ninh","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":11094},{"Type":1,"SolrID":"/khanh-hoa","ID":38,"Title":"Khánh Hòa","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":22032},{"Type":1,"SolrID":"/phu-yen","ID":39,"Title":"Phú Yên","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":6437},{"Type":1,"SolrID":"/hoa-binh","ID":40,"Title":"Hòa Bình","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":6289},{"Type":1,"SolrID":"/tuyen-quang","ID":41,"Title":"Tuyên Quang","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":3662},{"Type":1,"SolrID":"/lai-chau","ID":42,"Title":"Lai Châu","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":3067},{"Type":1,"SolrID":"/hau-giang","ID":43,"Title":"Hậu Giang","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":5474},{"Type":1,"SolrID":"/lam-dong","ID":44,"Title":"Lâm Đồng","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":15083},{"Type":1,"SolrID":"/lang-son","ID":45,"Title":"Lạng Sơn","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":5647},{"Type":1,"SolrID":"/ha-nam","ID":46,"Title":"Hà Nam","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":6970},{"Type":1,"SolrID":"/bac-can","ID":47,"Title":"Bắc Cạn","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":2335},{"Type":1,"SolrID":"/binh-dinh","ID":48,"Title":"Bình Định","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":13845},{"Type":1,"SolrID":"/cao-bang","ID":49,"Title":"Cao Bằng","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":3532},{"Type":1,"SolrID":"/son-la","ID":50,"Title":"Sơn La","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":5323},{"Type":1,"SolrID":"/quang-binh","ID":51,"Title":"Quảng Bình","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":8288},{"Type":1,"SolrID":"/quang-tri","ID":52,"Title":"Quảng Trị","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":6851},{"Type":1,"SolrID":"/gia-lai","ID":53,"Title":"Gia Lai","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":9383},{"Type":1,"SolrID":"/bac-giang","ID":54,"Title":"Bắc Giang","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":11428},{"Type":1,"SolrID":"/ha-tinh","ID":55,"Title":"Hà Tĩnh","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":10561},{"Type":1,"SolrID":"/ninh-binh","ID":56,"Title":"Ninh Bình","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":7840},{"Type":1,"SolrID":"/binh-thuan","ID":57,"Title":"Bình Thuận","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":11143},{"Type":1,"SolrID":"/kon-tum","ID":58,"Title":"Kon Tum","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":4660},{"Type":1,"SolrID":"/vinh-phuc","ID":59,"Title":"Vĩnh Phúc","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":12651},{"Type":1,"SolrID":"/bac-lieu","ID":60,"Title":"Bạc Liêu","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":5378},{"Type":1,"SolrID":"/yen-bai","ID":61,"Title":"Yên Bái","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":4816},{"Type":1,"SolrID":"/dien-bien","ID":62,"Title":"Điện Biên","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":3150},{"Type":1,"SolrID":"/ha-giang","ID":63,"Title":"Hà Giang","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":4546},{"Type":1,"SolrID":"/chua-ro","ID":64,"Title":"Chưa rõ","STT":0,"Created":null,"Updated":null,"TotalDoanhNghiep":61844}],"TotalDoanhNghiep":1548049}'
  countries = json.loads(countryData)['LtsItem']
  for country in countries:
    if country['Title'].lower() == country.split(',')[-1].strip():
      return True
  return False

def extractInfo(text):
  text = text.lower()
  for c in ['|', '.', ':', '\n', '=', '…']:
    text = text.strip().replace(c, ' ').strip()
  text = ' '.join(text.split())
  
  while text[-1].isalpha() == False:
    text = text[: -1]

  text = text.replace('đkhđ', 'đkhk')
  text = text.replace('đkhd', 'đkhk')
  text = text.replace('đkhh', 'đkhk')

  print(text)
  begin_number = text.find('số')
  begin_name = text.find('họ tên')
  begin_bd = text.find('sinh ngày')
  begin_address1 = text.find('nguyên quán')
  begin_address2 = text.find('nơi đkhk thường trú')
  number = text[begin_number + 2 : begin_name].strip().replace(' ', '')
  name = text[begin_name + 6 : begin_bd].strip().replace('-', '').replace('  ', ' ')
  bd = text[begin_bd + 9: begin_address1].strip()
  hometown = text[begin_address1 + 11 : begin_address2].strip().split(',')[-1].strip().replace('-', '').replace('  ', ' ')
  province = text[begin_address2 + 19 : ].strip().split(',')[-1].strip().replace('-', '').replace('  ', ' ')
  district = text[begin_address2 + 19 : ].strip().split(',')[-2].strip().replace('tp', '').strip().replace('-', '').replace('  ', ' ')

  return {
    'IdentityNumber': number,
    'Fullname': name.title(),
    'Birthday': bd,
    'Hometown': hometown.title(),
    'Province': province.title(),
    'District': district.title()
  }

def ocr(image, registerInfo):
  image = filter.denoise(image)
  image = filter.grayScale(image)
  image = filter.denoiseGray(image)
  # image = filter.sharpen(image)
  # displayImage(image)

  info = extractInfo(OCR(image))

  print(info)
  verify = {
    'FullnameResult': info['Fullname'].lower() == registerInfo['Fullname'].lower(),
    'IdentityNumberResult': info['IdentityNumber'] == registerInfo['IdentityNumber'],
    'BirthdayResult': info['Birthday'] == registerInfo['Birthday'],
    'HometownResult': info['Hometown'].lower() == registerInfo['Hometown'].lower(),
    'ProvinceResult': info['Province'].lower() == registerInfo['Province'].lower(),
    'DistrictResult': info['District'].lower() == registerInfo['District'].lower()
  }

  verify['OCRResult'] = verify['FullnameResult'] and verify['IdentityNumberResult'] and verify['BirthdayResult'] and verify['HometownResult'] and verify['ProvinceResult'] and verify['DistrictResult']

  return info, verify