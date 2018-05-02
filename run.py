from flask import Flask, jsonify
from flask_pymongo import PyMongo
from labels.logic.conversion import get_label

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'labels'
mongo = PyMongo(app)


@app.route('/label/<string:type>', methods=['GET'])
def save(type):
    response = {'field': get_label(mongo, type)}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
