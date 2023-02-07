from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import Binary
#  You need to convert binary image data to a base64 encoded string, then use that string to set the source of an img tag in HTML.
import base64

app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['TEMPLATES_FOLDER'] = 'templates'


# connect to MongoDB
client = MongoClient('mongodb+srv://test:sparta@cluster0.qxn9vle.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


# collection = db.genius

# # open image or video file
# with open("image.jpg", "rb") as image_file:
#     binary_data = image_file.read()

# insert binary data into MongoDB
# result = collection.insert_one({"image": binary_data})

# retrieve binary data from MongoDB
# binary_data = collection.find_one({"_id": result.inserted_id})["image"]

# save binary data to file
# with open("new_image.jpg", "wb") as new_image_file:
#     new_image_file.write(binary_data)


# 서버 구동하고, 브라우저에서 localhost:5000 열면 바로 여는 페이지
# 각 페이지 연결 작업을 아직 못해서 각 페이지 기능 점검할 때 아래 3개 중 하나를 활성화해서 썼어요.
@app.route('/')
def home():
    # return render_template('b_detail.html')
    return render_template('write.html')
    # return render_template('index.html')
    # return render_template('comment.html')


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
    time = request.form['time']
    # get the uploaded file from the HTML form
    file = request.files['file']
    binary_data = Binary(file.read())

    # insert the binary data and other information into MongoDB
    db.genius.insert_one({
        'num': num, 'category': category, 'role': role, 'region': region, 'name': name, 'title': title,
        'content': content, 'time': time, "filename": file.filename
    })
    # 실제 이미지 파일은 g_imgs 콜렉션에 저장
    db.g_imgs.insert_one({'num': num, "file": binary_data})
    return jsonify({'msg': '등록완료'})


# db에서 모든 값을 가져와서 클라이언트로 보내주기
@app.route("/board", methods=["GET"])
def board_get():
    # DB에서 모든 정보를 가져와서 변수 details에 넣어 주기
    details = list(db.genius.find({}, {'_id': False}))

    # for i in range(len(details)):
    #     # encoded_string = base64.b64encode(details[i]['file']).decode("utf-8")
    #     encoded_string = details[i]['file'].encode("utf-8")
    #     details[i]['file'] = encoded_string
    # print(details)
    # details 안의 값을 클라이언트에 전송하기
    return jsonify({'details': details})


# db에서 지정된 글의 내용을 가져와서 클라이언트(상세페이지)로 보내주기
# 채원 님, 밑에 detail = db.genius.find_one({'num':'4'}, {'_id': False}) 보면, 제가 글번호(num)이 4인 글을 가져오게 해 놨어요.
# 추후에 작성한 글, 클릭한 글의 num을 받아와서 넣어줄 수 있게 작업해야 해요. 같이 연구해 보아요.
@app.route("/detail", methods=["GET"])
def detail_get():
    num = request.args.get("num")
    print("서버가 받은 넘버는 " + num)
    # DB에서 해당 정보를 가져와서 변수 comments에 넣어 주기
    detail = db.genius.find_one({'num': num}, {'_id': False})
    print(detail)
    # print(type(detail)) - class 'dict'
    img_file = db.g_imgs.find_one({'num': num}, {'_id': False})
    # print(type(detail)) - class 'dict'

    encoded_string = base64.b64encode(img_file['file']).decode("utf-8")
    # detail에 file이라는 필드를 만들어 encoded_string을 넣기. 다른 데이터랑 같이 클라이언트에 넘길 수 있게
    # detail['file'] = encoded_string
    print("encoded_string:" + encoded_string)
    return render_template('b_detail.html')
    # return render_template('b_detail.html', detail=detail, encoded_string=encoded_string)
    # return jsonify({'detail': detail})


# 댓글 내용 가져오기
@app.route('/comment', methods=['GET'])
def comment_get():
    # num = request.args.get("b_num")
    # print("b_num = " + num)
    all_cmt = list(db.comments.find({}, {'_id': False}))
    # print(all_cmt)
    return jsonify({'cmt_list': all_cmt})


# 댓글 내용 저장하기
@app.route('/comment', methods=['POST'])
def comment_post():
    b_num_receive = request.form['b_num_give']
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    date_receive = request.form['date_give']
    doc = {
        'b_num': b_num_receive,
        'name': name_receive,
        'comment': comment_receive,
        'create_date': date_receive
    }
    db.comments.insert_one(doc)
    return jsonify({'msg': '댓글이 등록되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
