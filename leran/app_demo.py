import random
import time
from hashlib import md5
from PIL import Image
import tornado.web
import tornado.ioloop
from pycket.session import SessionMixin
from tornado.options import options, define, parse_command_line
import utils.ui_methods
import utils.ui_modules
from leran.upload_liat import new_list_img, new_list_thumb


define('port', default=8080, help="运行端口")


class BaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        # return self.get_secure_cookie("define_cookie")
        return self.session.get('username_session')


class FirstHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user:
            print("此时的cookie键所对应的值为{}".format(self.current_user))
            self.render("8welcome.html", username=self.current_user)


class PictureHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<html><body><img src='/static/images/1.jpg'></body></html>")
        #这里satic前面加上/（正斜杆）是代表绝对路径，如果不加，则代表相对路径，但是在多个路由的时候就会报错。

    def initialize(self):
        print('对象{}被创建了'.format(self))


class TemplateHandler(tornado.web.RequestHandler):
    def get(self):
        username = '小龙'
        items = ["Item 1", "Item 2", "Item 3"]
        line = "====="*6
        time_now = time.time()
        atga = "<a href='http://www.baidu.com' target='_blank'>_百度_</a><br>"
        student_list = [
            {'name': '小红', 'age': 18, 'hobby': '打篮球', 'web': 'http://www.baidu.com'},
            {'name': '小明', 'age': 16, 'hobby': '打篮球', 'web': 'http://www.jianshu.com'},
            {'name': '小浩', 'age': 20, 'hobby': '打羽毛球', 'web': 'http://www.baidu.com'},
        ]
        self.render('1demo.html', username=username, title="基础模板", items=items, students=student_list, line=line, time=time_now, atga=atga)

    def post(self):
        username = self.get_argument('name', 'no')
        number = int(random.random()*100 + 1)
        self.render('2demo.html', username=username, num=number)


class Calculation():
    def sum(self, a, b):
        return a+b


class ExtendsHandler(tornado.web.RequestHandler):
    def get(self):
        username ='小明'
        self.render('3extends.html', username=username, hu=self.hu, Calculation=Calculation)

    def hu(self):
        return 'this is class and way be transfered by the modle'


class SubmitHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('5submit.html')

    def post(self):
        username = self.get_argument('name', None)
        # self.write('名字为:{}'.format(username))
        self.redirect('/template?username={}'.format(username))


def hash(text):
    return md5('{}+{}'.format(text, 'jiayan').encode()).hexdigest()


USER_DATA = {
 '小龙': hash('123'),
'xiaolong111':hash('123')
}


def auth(username, password):
    if username and password:

        return USER_DATA.get(username, None) == hash(password)
    else:
        return False


class LoginHandler(BaseHandler):
    def get(self):
        next_url = self.get_argument('next', '/template')
        if self.current_user:
            print("此时的cookie键所对应的值为{}".format(self.current_user))
            # self.render("8welcome.html", username=self.current_user)
            self.redirect(next_url)
        else:
            self.render('7login.html', next_url=next_url)

    def post(self):
        next_url = self.get_argument('next_url', '/template')
        username = self.get_argument("username")
        password = self.get_argument("password")
        if auth(username, password):
            print(hash(password))
            self.session.set("username_session", username)
            self.write("Your cookie was not set yet!"+"在此之后就会被设置")
            # self.render('8welcome.html', username=username)
            self.redirect(next_url)
        else:
            self.write("密码或者用户名出错,还有绝对不可以为空哦")


class UploadHandler(BaseHandler):

    def get(self):
        self.render('9upload.html')

    def post(self):
        try:
            files = self.request.files['picture']#list类型中包含一个字典
            if files[0]:
                dict_img = files[0]
                filename = dict_img['filename']
                print(filename)
                print(dict_img['content_type'])
                save_path = 'static/upload/{}'.format(filename)
                with open(save_path, 'wb') as f:
                    f.write(dict_img['body'])
                im = Image.open(save_path)
                im.thumbnail((200, 200))
                im.save('static/thumbs/thumb_{}'.format(filename))
                self.render('10upload_success.html', filename=files[0]['filename'], list_img=new_list_img, new_list_thumb=new_list_thumb)
            else:
                self.write("上传失败，系统不听话")
        except Exception as e:
            print(e)
            self.write("上传失败，上传的图片不可以为空")


def make_app():
    handlers = [
        (r'/', FirstHandler),
        (r'/picture', PictureHandler),
        (r'/template', TemplateHandler),
        (r'/extends', ExtendsHandler),
        (r'/submit', SubmitHandler),
        (r'/login', LoginHandler),
        (r'/upload', UploadHandler)
    ]

    settings = \
        {'debug': True,
         'static_path': 'static',
         'template_path': 'templates',
         'ui_methods': utils.ui_methods,
         'ui_modules': utils.ui_modules,
         'cookie_secret': "12323",
         "login_url": "/login",
         'pycket': {
             'engine': 'redis',
             'storage': {
                 'host': '192.168.212.131',
                 'port': 6379,
                 # 'password': '',
                 'db_sessions': 5,  # redis db index
                 'db_notifications': 11,
                 'max_connections': 2 ** 30,
             },
             'cookies': {
                 'expires_days': 30,
             },
         }
         }#直接写staic这里是相对路径，这是相对与这个脚本的路径而言的
    app = tornado.web.Application(handlers=handlers, **settings)
    return app


if __name__ == '__main__':
    app = make_app()
    # app.listen(8000)
    parse_command_line()
    port_new = options.port
    app.listen(port_new)
    print(type(port_new))
    print("Tornado server running at %s port" % port_new)
    tornado.ioloop.IOLoop.current().start()

