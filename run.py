from flask import Flask, jsonify
from labels.logic.conversion import test

app = Flask(__name__)


@app.route('/label/<string:type>', methods=['GET'])
def save(type):
    response = {'field': test()}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
