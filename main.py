from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

url = "mongodb://jincheol:work930417@ds149593.mlab.com:49593/heroku_k0cr1wdd?retryWrites=false"
client = MongoClient(url)
db = client['heroku_k0cr1wdd']


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# POST : Input 데이터 얻은 후 / DB에 저장
@app.route('/order', methods=['POST'])
def write_order():
    cur_userName = request.form['userName']
    cur_num = request.form['num']
    cur_address = request.form['address']
    cur_phoneNumber = request.form['phoneNumber']


    order = {
              'userName': cur_userName,
              'num': cur_num,
              'address': cur_address,
              'phoneNumber': cur_phoneNumber 
              }

    db.order.insert_one(order)
    return jsonify({'result': 'success', 'msg': '주문이 정상적으로 처리되었습니다.'})

# GET : DB 데이터 얻은 후 / 업데이트
@app.route('/order', methods=['GET'])
def get_order():
    # {'_id':0}) 의미는 불러드일 때 id항목은 넣지 않겠다는 것
    # 아래의 코드는 어차피 html 에서 사전형으로 일일히 불러들일꺼므로 잘 안슴
    # 전에 했더니 제대로 코드가 작동안됨.
    # 그래서 임시로 씀

    orders = list( db.order.find({}, {'_id':0}) )
    # orders = list( db.order.find({} ) )
    return jsonify({'result': 'success', 'orders': orders})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)