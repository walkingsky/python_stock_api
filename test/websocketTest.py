from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit
import json
import redis
import sys
sys.path.append('..')
from config import REDIS_HOST,REDIS_PORT


redisClient = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=0,decode_responses=True)

app = Flask(__name__,template_folder='./')
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,logger=True)

@app.route('/')
def index():
    return render_template('index.html',async_mode=socketio.async_mode)

@socketio.on('connect')
def connect_handler():
    # global stopTreading
    emit('my_response', {'data': 'Connected'})
    print('Client (%s) connected'%(request.sid))
    redisClient.sadd('connect_ids',str(request.sid))

@socketio.on('disconnect')
def disconnect_handler():
    print('Client (%s) disconnected'%(request.sid))
    if(redisClient.sismember('connect_ids',str(request.sid))):
        redisClient.srem('connect_ids',str(request.sid))
    redisClient.delete(str(request.sid))

@socketio.on('SetCode')
def on_set_code(codes):
    print('print received message[my event]: ' + str(codes))    
    #redisClient.rpush(str(request.sid)+'_codes',str(codes))
    redisClient.set(str(request.sid),str(codes))
  
@socketio.on('Stop')
def on_stop():
    print('print received message[my event]: ' )
    if(redisClient.sismember('connect_ids',str(request.sid))):
        redisClient.srem('connect_ids',str(request.sid))
    redisClient.delete(str(request.sid))
'''
@socketio.on('json')
def handle_json(data):
    print('print received message[json]: ' + str(data))
    emit('emit received message[json]: ' + str( data))
'''
@socketio.on('GetData')
def handle_message():
    print('db name :'+ str(request.sid) + '_msg')
    message = redisClient.lpop(str(request.sid) + '_msg')
    print(message)
    if message:
        socketio.emit('stocks_data',json.loads(message))

def background_thread():          

    while True:
        socketio.sleep(1)  # 每隔1秒发送一次数据
        message = redisClient.lpop(str(request.sid) + '_msg')
        if message:
            socketio.emit('stocks_data',json.load(message))
        

if __name__ == '__main__':
    # socketio.start_background_task(background_thread)
    socketio.run(app,host='127.0.0.1',port=5001,debug=True)