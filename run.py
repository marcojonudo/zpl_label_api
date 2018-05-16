from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from jsonschema import validate, ValidationError
from labels.validation.request_validation import get_label_schema
from labels.logic.conversion import get_label
from labels.structure.giftbox_label import GiftboxLabel

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'labels'
mongo = PyMongo(app)


@app.route('/label/<string:type>', methods=['POST'])
def get(type):
    try:
        validate(request.json, get_label_schema)
    except ValidationError:
        return jsonify({"error": "Error de validacion"})

    label_info = GiftboxLabel(request.json)
    zpl_code = get_label(mongo, type, label_info)
    response = {'field': zpl_code}  # get_label(mongo, type, label)}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
