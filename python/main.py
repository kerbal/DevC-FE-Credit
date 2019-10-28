import sys
import json

def sum(a, b):
  return a + b

if __name__ == "__main__":
  response = {
    'sum': sum(int(sys.argv[1]), int(sys.argv[2]))
  }
  print(json.dumps(response))