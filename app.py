from flask import Flask, jsonify, Response, request
from services.main import main
from services.imageReader import readFromPath
import sys

app = Flask(__name__)

@app.route("/")
def home():
  return "Hello, World!"
    
@app.route("/test", methods=['POST'])
def test():
  try:
    IdCardURL = request.json['IDCardImage']
    SelfieURL = request.json['SelfieImage']

    info = {
      'Fullname': request.json['Fullname'],
      'IdentityNumber': request.json['IdentityNumber'],
      'Birthday': request.json['Birthday'],
      'Hometown': request.json['Hometown'],
      'Province': request.json['Province'],
      'District': request.json['District']
    }

    response = main(IdCardURL, SelfieURL, info)
    return jsonify(response), 200
  except Exception as e:
    return jsonify({
      'message': str(e)
    }), 400

if __name__ == "__main__":
  print(sys.argv)
  app.run(debug=True)