from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


client = MongoClient('mongodb+srv://test:sparta@cluster0.qxn9vle.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('board_detail.html')


@app.route("/detail", methods=["GET"])
def detail_get():
    num = "3"
    # num = request.args.get("num")
    # DB에서 정보를 가져와서 변수 comments에 넣어 주기
    detail = db.genius.find_one({'num': num}, {'_id': False})
    # ob_id = str(detail[0])
    # print(ob_id)
    print(detail)
    # detail 안의 값을 클라이언트에 전송하기
    return jsonify({'detail': detail})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5500, debug=True)
