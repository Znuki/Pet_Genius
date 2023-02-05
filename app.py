from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.qxn9vle.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    # return render_template('b_detail.html')
    # return render_template('write.html')
    return render_template('index.html')

# @app.route("/write")
# def openWrite():
#     return render_template('write.html')


@app.route("/write", methods=["POST"])
def write_save():
    # 클라이언트가 보낸 값을 받아 오기
    # cat = request.form['cat']
    num = request.form['num']
    category = request.form['category']
    role = request.form['role']
    region = request.form['region']
    name = request.form['name']
    title = request.form['title']
    content = request.form['content']
    file = request.form['file']
    time = request.form['time']

    doc = {'num':num, 'category': category, 'role': role, 'region': region, 'name': name, 'title': title, 'content': content,
           'file': file, 'time':time}
    db.genius.insert_one(doc)
    return jsonify({'msg': '등록완료'})


@app.route("/board", methods=["GET"])
def board_get():
    # DB에서 모든 정보를 가져와서 변수 comments에 넣어 주기
    details = list(db.genius.find({}, {'_id': False}))
    # print(details)
    # details 안의 값을 클라이언트에 전송하기
    return jsonify({'details': details})


@app.route("/detail", methods=["GET"])
def detail_get():
    # DB에서 해당 정보를 가져와서 변수 comments에 넣어 주기
    # user = db.users.find_one({'name': 'bobby'})

    detail = db.genius.find_one({'num':'4'}, {'_id': False})
    print(detail)
    # details 안의 값을 클라이언트에 전송하기

    return jsonify({'detail': detail})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
