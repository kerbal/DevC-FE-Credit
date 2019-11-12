from flask import Flask, jsonify, Response, request
from services.main import main
from services.imageReader import readFromPath

app = Flask(__name__)

@app.route("/")
def home():
  return "Hello, World!"
    
@app.route("/test", methods=['POST'])
def test():
  try:
    IdCardURL = request.json['IDCardImageURL']
    SelfieURL = request.json['SelfieImageURL']

    response = main(IdCardURL, SelfieURL)
    return jsonify(response), 200
  except Exception as e:
    return jsonify({
      'message': str(e)
    }), 400

if __name__ == "__main__":
  app.run(debug=True)