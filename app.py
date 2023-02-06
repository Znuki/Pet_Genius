from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient

# client = MongoClient('mongodb+srv://znuki:znuki@cluster0.mo5ena6.mongodb.net/?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://test:sparta@cluster0.qxn9vle.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


# doc = {
#     'num': 1,
#     'category': '도와주세요',
#     'job':'펫시터',
#     'region':'서울시',
#     'name':'강진욱'
# }
#
# db.users.insert_one(doc)


# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route("/board", methods=["GET"])
# def board_get():
details = list(db.genius.find({}, {'_id': False}))
print(details)
    # return jsonify({'details':details})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
