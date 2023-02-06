from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.qxn9vle.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


# 서버 구동하고, 브라우저에서 localhost:5000 열면 바로 여는 페이지
# 각 페이지 연결 작업을 아직 못해서 각 페이지 기능 점검할 때 아래 3개 중 하나를 활성화해서 썼어요.
@app.route('/')
def home():
    # return render_template('b_detail.html')
    # return render_template('write.html')
    return render_template('index_test.html')


# 글쓰기 페이지에서 등록 버튼을 누르고, 클라이언트에서 save_write() 펑션 실행 되면 서버의 여기로 넘어옴 - db저장
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

    doc = {'num': num, 'category': category, 'role': role, 'region': region, 'name': name, 'title': title,
           'content': content,
           'file': file, 'time': time}
    db.genius.insert_one(doc)
    return jsonify({'msg': '등록완료'})


# db에서 모든 값을 가져와서 클라이언트로 보내주기
@app.route("/board", methods=["GET"])
def board_get():
    # DB에서 모든 정보를 가져와서 변수 comments에 넣어 주기
    details = list(db.genius.find({}, {'_id': False}))
    # print(details)
    # details 안의 값을 클라이언트에 전송하기
    return jsonify({'details': details})


# db에서 지정된 글의 내용을 가져와서 클라이언트(상세페이지)로 보내주기
# 채원 님, 밑에 detail = db.genius.find_one({'num':'4'}, {'_id': False}) 보면, 제가 글번호(num)이 4인 글을 가져오게 해 놨어요.
# 추후에 작성한 글, 클릭한 글의 num을 받아와서 넣어줄 수 있게 작업해야 해요. 같이 연구해 보아요.
@app.route("/detail", methods=["GET"])
def detail_get():
    num = request.args.get("num")
    print("넘버는" + num)
    # DB에서 해당 정보를 가져와서 변수 comments에 넣어 주기
    detail = db.genius.find_one({'num': num}, {'_id': False})
    # print(type(detail)) - class 'dict'
    print(detail)
    # 여기까지 실행 됨
    # return render_template('b_detail.html', detail=detail)
    return jsonify({'detail': detail})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)