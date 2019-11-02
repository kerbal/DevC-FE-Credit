import sys
import json
import importlib
import ocrProcess
import os

if __name__ == "__main__":
  try:
    IDCardImageURL = sys.argv[1]
    SelfieImageURL = sys.argv[2]
    ocr = ocrProcess.ocrProcess(IDCardImageURL)
    print(ocr)
  except Exception as e:
    print(str(e))