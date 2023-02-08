from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import Binary
#  You need to convert binary image data to a base64 encoded string, then use that string to set the source of an img tag in HTML.
import base64

app = Flask(__name__, template_folder='templates')
# app = Flask(__name__)
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
    # return render_template('detail.html')
    # return render_template('write.html')
    return render_template('index.html')
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
        'content': content, 'time': time, "file": file.filename
    })
    # 실제 이미지 파일은 g_imgs 콜렉션에 저장
    db.g_imgs.insert_one({'num': num, "img": binary_data})
    return jsonify({'msg': '등록완료'})
    # return render_template('detail.html', msg='등록완료')


# db에서 모든 값을 가져와서 클라이언트로 보내주기
@app.route("/board", methods=["GET"])
def board_get():
    details = list(db.genius.find({}, {'_id': False}))
    img_binary_list = list(db.g_imgs.find({}, {'_id': False}))
    img_string_list = []
    for i in range(len(details)):
        img_binary = img_binary_list[i]
        img_string = base64.b64encode(img_binary['img']).decode("utf-8")
        img_string_list.append(img_string)
    if details == '' or img_string_list == '':
        print("보드의 디테일즈 이미지스트링리스트 값없음")
    else:
        print("디테일, 인코디드 값 있음")
    return jsonify({'details': details, 'img_string_list': img_string_list})
    # return render_template('index.html', details=details, img_string_list=img_string_list)


@app.route("/detail", methods=["GET"])
def detail_get():
    num = request.args.get("num")
    print("디테일2 서버가 받은 넘버는 " + num)
    detail = db.genius.find_one({'num': num}, {'_id': False})
    # print(detail)
    img_binary = db.g_imgs.find_one({'num': num}, {'_id': False})
    encoded_string = base64.b64encode(img_binary['img']).decode("utf-8")
    if detail == '' or encoded_string == '':
        print("detail2의 디테일 인코디드 스트링 값없음")
    else:
        print("디테일, 인코디드 값 있음")
    # return jsonify({'detail': detail, 'encoded_string': encoded_string})
    # return jsonify({'detail': detail, 'encoded_string': encoded_string})
    # return render_template('detail.html', detail=detail)
    return render_template('detail.html', detail=detail, encoded_string=encoded_string)
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
