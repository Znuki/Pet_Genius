from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:sparta@cluster0.xlfvugi.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta

# 지수님 db
client = MongoClient('mongodb+srv://test:sparta@cluster0.qxn9vle.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# # db_test
# all = list(db.comments.find({'b_num':1}))
# print(all)

@app.route('/test')
def test():
    return render_template('index_heejin.html')

@app.route('/write')
def write():
    return render_template('write.html')

# 메인페이지 가기
@app.route('/')
def home():
    return render_template('comment.html') # render_template : 해당 html 파일이 보여짐

# 댓글 내용 가져오기
@app.route('/comment', methods=['GET'])
def comment_get():
    # num = request.args.get("b_num")
    # print("b_num = " + num)
    cmt_list = list(db.comments.find({'b_num':'1'}, {'_id' : False}))
    print(cmt_list)
    return jsonify({'cmt_list': cmt_list})

# 댓글 내용 저장하기
@app.route('/comment', methods=['POST'])
def comment_post():
    b_num_receive = request.form['b_num_give']
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    date_receive = request.form['date_give']
    doc = {
        'b_num' : b_num_receive,
        'name' : name_receive,
        'comment' : comment_receive,
        'created_date' : date_receive
    }
    db.comments.insert_one(doc)
    return jsonify({'msg': '댓글이 등록되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)