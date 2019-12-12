import tornado.websocket
import tornado.web
import datetime,time
import uuid
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado import httputil
import tornado.escape #对json数据进行解码操作
from models.auth import User, Post, LikePost
from Handlers.main import BaseHandler


class RoomWebSocket(tornado.websocket.WebSocketHandler, BaseHandler):
    waiters = set()
    history = []
    history_size =15

    def open(self):
        print("{}对象打开了WebSocket通信".format(self))
        RoomWebSocket.waiters.add(self) #添加相应的连接对象

    def on_close(self):
        print("{}对象关闭了了WebSocket通信".format(self))
        RoomWebSocket.waiters.remove(self)

    def on_message(self, message):
        # print("{}:{}".format(self, message))
        parsed = tornado.escape.json_decode(message)
        # if parsed['body'].startswith('http://'):
        #     client = AsyncHTTPClient()
        #     client.fetch(parsed['body'])
        #     api_url = 'http://127.0.0.1:8080/save?save_url={}'.format(parsed['body'])
        #     IOLoop.current().spawn_callback(client.fetch, api_url)
        #     msg = parsed['body']
        # else:
        #     msg = parsed['body']
        chat = {
            'id': uuid.uuid4().hex,
            'username': self.current_user,
            'created': time.strftime("%y年%m月%d日 %H时%M分"),
            'body': parsed['body']
        }
        chat['html'] = tornado.escape.to_basestring(self.render_string('chat/message.html', chat=chat))
        RoomWebSocket.update_history(chat['html'])
        RoomWebSocket.send_msg(chat)

    @classmethod
    def send_msg(cls, chat):
        for w in RoomWebSocket.waiters:
            w.write_message(chat)

    @classmethod
    def update_history(cls, html):
        RoomWebSocket.history.append(html)
        if len(RoomWebSocket.history) > 0:
            RoomWebSocket.history = RoomWebSocket.history[-20:]


class RoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        user = self.db_session.query(User).filter_by(username=username).first()
        power_id = user.power
        self.render('chat/room.html', username=username, power_id=power_id, msgs=RoomWebSocket.history)




