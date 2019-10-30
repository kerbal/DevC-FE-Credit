import sys
import json
import importlib
import googleVision
import os

if __name__ == "__main__":
  try:
    response = googleVision.OCR(sys.argv[1])
    print(response)
  except Exception as e:
    print(str(e))