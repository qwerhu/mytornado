import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")#在相应的网页上打印出相应的内容


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),#相当与django的路由
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)#请求端口
    tornado.ioloop.IOLoop.current().start()#启动tornado服务

