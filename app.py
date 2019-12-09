from flask import Flask, jsonify, Response, request
from services.main import main
from services.imageReader import readFromPath
import services.database as db
import sys

app = Flask(__name__)

@app.route("/")
def home():
  return "Hello, World!"
    
@app.route("/register", methods=['POST'])
def test():
  try:
    print('REGISTERING...')
    IdCardURL = request.json['IDCardImage']
    SelfieURL = request.json['SelfieImage']

    info = {
      'Fullname': request.json['Fullname'],
      'IdentityNumber': request.json['IdentityNumber'],
      'Birthday': request.json['Birthday'],
      'Hometown': request.json['Hometown'],
      'Province': request.json['Province'],
      'District': request.json['District'],
      'PhoneNumber': request.json['PhoneNumber']
    }

    response = main(IdCardURL, SelfieURL, info)
    success = response['success']

    if success == True: 
      return jsonify({
        "UserId": str(response['userId'])
      }), 200
    else:
      return jsonify({
        "Message": str(response['message'])
      }), 400
  except Exception as e:
    return jsonify({
      'Message': str(e)
    }), 400

@app.route("/forms")
def getForms():
  try:
    response = db.getUserResult()
    return jsonify({
      'Forms': response
    }), 200
  except Exception as e:
    print(e)
    return jsonify({
      'Forms': []
    }), 400

@app.route("/status", methods=['GET'])
def getStatus():
  try:
    response = db.getVerificationStatus(request.args.get('id'))
    return jsonify({
      'Status': response
    }), 200
  except Exception as e:
    print(e)
    return jsonify({
      'Status': False
    }), 400

@app.route("/status", methods=['PUT'])
def setStatus():
  try:
    db.setVerificationStatus(request.args.get('id'), int(request.args.get('value')))
    return jsonify({
      'message': 'okey'
    }), 200
  except Exception as e:
    return jsonify({
      'message': str(e)
    }), 400

@app.route("/form")
def getForm():
  try:
    id = request.args.get('id')
    response = db.getUserResultById(id)
    return jsonify({
      'Form': response
    }), 200
  except Exception as e:
    print(e)
    return jsonify({
      'Form': None
    }), 400

if __name__ == "__main__":
  app.run(debug=True)
