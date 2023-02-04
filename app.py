from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://znuki:znuki@cluster0.mo5ena6.mongodb.net/?retryWrites=true&w=majority')
db = client.pet_genius


# doc = {
#     'num': 1,
#     'category': '도와주세요',
#     'job':'펫시터',
#     'region':'서울시',
#     'name':'강진욱'
# }
#
# db.users.insert_one(doc)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/board", methods=["POST"])
def write_post():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'POST 연결 완료!'})


@app.route("/board", methods=["GET"])
def write_get():
    write_list = list(db.writes.find({}, {'_id': False}))
    return jsonify({'boards':write_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
