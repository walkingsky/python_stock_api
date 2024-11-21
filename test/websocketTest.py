from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import requests
import threading


headers ={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'qgqp_b_id=04d98930562bb8f118b93bd3745149ec; st_pvi=28821874947718; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sp=2020-08-20%2011%3A39%3A47',
    'Host':'88.push2.eastmoney.com',
    'Pragma':'no-cache',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'none',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

stopTreading = False;

app = Flask(__name__,template_folder='./')
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,logger=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect_handler():
    global stopTreading
    emit('my_response', {'data': 'Connected'})
    #emit('Client'+ sid + 'connected')
    stopTreading = True

@socketio.on('disconnect')
def disconnect_handler():
    print('Client disconnected')

@socketio.on('GetData')
def handle_my_custom_event(data):
    print('print received message[my event]: ' + str(data))
    global stopTreading
    stopTreading = True
    time.sleep(1)    
    threadingGetData = threading.Thread(target=getDataThread,name=data,args=(data,))
    stopTreading = False
    threadingGetData.start() 
    threadingGetData.join()

@socketio.on('json')
def handle_json(data):
    print('print received message[json]: ' + str(data))
    emit('emit received message[json]: ' + str( data))
'''
@socketio.on('message')
def handle_message(message):
    print('print received message: ' + str(message))
    emit('emit received message: ' + str(message))
'''
def background_thread():
    count = 0

    # delimiter 分隔符，decode_unicode
    # for line in r.iter_lines(chunk_size=1024,delimiter="\n",decode_unicode=True):
    #    if line:
    #        socketio.emit('my_response', {'data': 'Count: ' + str(count)})            

    while True:
        socketio.sleep(1)  # 每隔1秒发送一次数据
        #count = count + 1
        #socketio.emit('my_response',{'data':'count:' + str(count) })
        
def getDataThread(code):
    global stopTreading
    url='https://88.push2.eastmoney.com/api/qt/ulist/sse?' +\
        'secids=' + str(code) +\
        '&fields=f12,f13,f14,f19,f139,f148,f2,f4,f1,f125,f18,f3,f152,f5,f30,f31,f32,f6,f8,f7,f10,f22,f9,f112,f100' +\
        '&invt=3&ut=fa5fd1943c7b386f172d6893dbfba10b&fid=&po=1&pi=0&pz=30&mpi=6000&dect=1'
        # '&invt=3&ut=fa5fd1943c7b386f172d6893dbfba10b&fid=&po=1&pi=0&pz=30&mpi=6000&dect=1'
        # 'secids=0.002902,1.600833,0.003031,0.300274' +\

    session = requests.session()
    r = session.get(url,stream=True,headers=headers)
    # delimiter 分隔符，decode_unicode
    for line in r.iter_lines(chunk_size=1024,delimiter="\n",decode_unicode=True):
        if line:
            print('1')
            socketio.emit('dataMsg',line)
        if stopTreading:
            print('2 stop')
            session.close()
            stopTreading = False
            return
    
    cnt = 0
    while not stopTreading:
        print(cnt)
        cnt = cnt + 1
        time.sleep(1)


if __name__ == '__main__':
    socketio.start_background_task(background_thread)
    socketio.run(app,host='127.0.0.1',port=5001,debug=True)