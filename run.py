from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from jsonschema import validate, ValidationError
from labels.validation.request_validation import get_label_schema
from labels.logic.conversion import get_label

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'labels'
mongo = PyMongo(app)


@app.route('/label/<string:type>', methods=['POST'])
def get(type):
    # try:
        # validate(request.json, get_label_schema)
    # except ValidationError:
        # return jsonify({"error": "Error de validacion"})
    response = {'field': get_label(mongo, type)}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
