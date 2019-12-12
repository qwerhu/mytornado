import tornado.web
from pycket.session import SessionMixin
from models.db import Session
from models.auth import User, Quotes, Post
from .main import BaseHandler


class UpdateUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        self.render('user/update.html', user=user)

    @tornado.web.authenticated
    def post(self, user_id):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')
        gender = self.get_argument('gender', '')
        age = self.get_argument('age', ' ')
        power = self.get_argument('power', '')
        session =Session()
        session.query(User).filter_by(id=int(user_id)).update({User.username: username, User.password: password, User.emial: email, User.gender: gender, User.age: age,User.power: int(power)})
        session.commit()
        self.redirect('/administrator')


class DeleteUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        session = Session()
        rows = session.query(User).filter_by(id=user_id).first()
        session.delete(rows)
        session.commit()
        session.close()
        self.redirect('/administrator')


class QuotesHandler(BaseHandler):
    """
    所有的格言数据
    """
    @tornado.web.authenticated
    def get(self):
        quotes_all = self.db_session.query(Quotes).all()
        username = self.current_user
        user = self.db_session.query(User).filter_by(username=username).first()
        post_id = user.id
        self.render('quote/quotes.html', username=username, post_id=post_id, quotes_all=quotes_all)


class UpdateQuotesHandler(BaseHandler):
    """
    修改格言信息
    """
    @tornado.web.authenticated
    def get(self, quote_id):
        quote_data = self.db_session.query(Quotes).filter_by(id=quote_id).first()
        self.render('quote/quote_update.html', quote_data=quote_data)

    @tornado.web.authenticated
    def post(self, quote_id):
        author = self.get_argument('author', '')
        country = self.get_argument('country', '')
        content = self.get_argument('content', '')
        session = Session()
        session.query(Quotes).filter_by(id=int(quote_id)).update({Quotes.author: author, Quotes.country: country,Quotes.quotes_content: content})
        session.commit()
        self.redirect('/quotes')


class DeleteQuoteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, quote_id):
        session = Session()
        rows = session.query(Quotes).filter_by(id=quote_id).first()
        session.delete(rows)
        session.commit()
        session.close()
        self.redirect('/quotes')


class UploadQuoteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('quote/quote_upload.html')

    @tornado.web.authenticated
    def post(self):
        author = self.get_argument('author', '')
        country = self.get_argument('country', '')
        content = self.get_argument('content', '')
        self.orm.add_quotes(author, country, content)
        self.redirect('/quotes')


class SelfUserInformationUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.get_argument('username', '')
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        self.render('user/selfupdate.html', user=user, username=username)

    @tornado.web.authenticated
    def post(self):
        username = self.get_argument('username', '')
        username1 = self.get_argument('username1', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')
        gender = self.get_argument('gender', '')
        age = self.get_argument('age', ' ')
        session = Session()
        dict_data = {User.username:username1,User.password:password, User.emial:email,User.gender:gender,User.age:age}
        session.query(User).filter_by(username=username).update(dict_data)
        session.commit()
        self.redirect('/')


class SelfPostManagementHandler(BaseHandler):
    """
    个人图片的管理
    """
    @tornado.web.authenticated
    def get(self):
        username = self.get_argument('username', '')
        user_id = self.db_session.query(User.id).filter_by(username=username).first()[0]
        posts = self.db_session.query(Post).filter_by(user_id=user_id).all()
        self.render('user/selfpost.html', posts=posts, username=username)


class DeletePostHandler(BaseHandler):
    def get(self, post_id):
        self.orm.delete_post(post_id)
        self.redirect('/selfpost?username={}'.format(self.current_user))


class FindPassword(BaseHandler):
    def get(self):
        msg = '无'
        self.render('user/findpwd.html', msg=msg)

    def post(self):
        username = self.get_argument('username', '')
        msg = "密码为："+str(self.orm.get_user_password(username))
        self.render('user/findpwd.html', msg=msg)






