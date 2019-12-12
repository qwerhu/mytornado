import tornado.web
import os
from pycket.session import SessionMixin
from utiles.orm import OrmHandler
from models.db import Session
from models.auth import User, Post, LikePost
from utiles.photo import UploadImage


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('username_session')

    def initialize(self):
        self.db_session = Session()
        self.orm = OrmHandler(self.db_session)

    def on_finish(self):
        self.db_session.close()


class IndexHandler(BaseHandler):
    """
    系统首页,所关注的用户图片流  /   IndexHandler
    """
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        user = self.db_session.query(User).filter_by(username=username).first()
        power_id = user.power
        users = self.orm.get_all_users()
        posts = self.db_session.query(Post).filter(Post.user_id != None).order_by(-Post.id).all()
        quotes_one = self.orm.get_one_quotes()
        list_three_user, list_three_size = self.orm.get_three_user()
        self.render('index.html', username=username, power_id=power_id,\
                    users=users, posts=posts, quotes_one=quotes_one,\
                    list_three_user=list_three_user, list_three_size=list_three_size )


class ExploreHandler(BaseHandler):
    """
    发现或最近上传的图片页面 /explore  ExploreHandler
    """
    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument('page', '1'))
        pg = self.orm.get_all_posts(page)
        username = self.current_user
        user = self.db_session.query(User).filter_by(username=username).first()
        power_id = user.power
        self.render('explore.html', pg=pg, username=username, power_id=power_id, page=page)

    def post(self):
        pass


class AdministratorHandler(BaseHandler):
    """
    管理员界面
    """
    @tornado.web.authenticated
    def get(self):
       users = self.orm.get_all_users()
       username = self.current_user
       user = self.db_session.query(User).filter_by(username=username).first()
       post_id = user.id
       self.render('user/information.html', users=users, username=username, post_id=post_id)

    def post(self):
        pass


class PostHandler(BaseHandler):
    """
    个人上传图片详情页面  /post/id   PostHandler
    """
    @tornado.web.authenticated
    def get(self, post_id):

        user = self.db_session.query(User).filter_by(username=self.current_user).first()
        power_id = user.power
        if post_id == str(user.id):
            posts = self.db_session.query(Post).filter_by(user_id=post_id).all()
            self.render('post.html', post_id=post_id, posts=posts, username=self.current_user,power_id=power_id)
        else:
            self.redirect('/upload')


class One_pictureHandler(BaseHandler):
    """
       单个图片详情页面  /one_picture/id   One_pictureHandler
    """
    def get(self, post_id):
         post_one = self.db_session.query(Post).filter_by(id=post_id).first()
         upload_user_id = self.db_session.query(Post.user_id).filter_by(id=post_id).first()[0]
         upload_user = self.db_session.query(User.username).filter_by(id=int(upload_user_id)).first()[0]
         uploaded_pictures_list = self.db_session.query(Post).filter_by(user_id=upload_user_id).all()
         like_number_list = self.db_session.query(LikePost).filter_by(post_id=post_id).all()
         current_user_id = self.db_session.query(User.id).filter_by(username=self.current_user).first()[0]
         list_post_id1 = self.db_session.query(LikePost.post_id).filter_by(user_id=current_user_id).all()
         list_post_id = []
         for i in list_post_id1:
             list_post_id.append(i[0])
         value = {'msg': None}
         if int(post_id) in list_post_id:
             value['msg'] = "good"
         else:
             value['msg'] = "fail"
         self.render('one_picture.html', post=post_one,\
         username=self.current_user, upload_user=upload_user,\
         uploaded_pictures_count=len(uploaded_pictures_list),\
         like_number=len(like_number_list), current_user_id=current_user_id,\
                     value=value)


class UploadHandler(BaseHandler):
    """
    用户上传图片信息
    """
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        single_length, no_like_post_id =self.orm.get_liked_posts(username)
        list_data = self.orm.get_no_like_posts(no_like_post_id)
        user = self.db_session.query(User).filter_by(username=username).first()
        user_id = user.id
        power_id = user.power
        like_posts = self.db_session.query(LikePost).filter_by(user_id=user_id).all()
        posts = self.db_session.query(Post).filter_by(user_id=user_id).all()
        self.render('user/upload.html', username=username, power_id=power_id,\
                    user_id=user_id, posts=posts, like_posts=like_posts,\
         single_length=single_length, list_data=list_data)

    @tornado.web.authenticated
    def post(self):
        try:
            files = self.request.files['picture']#list类型中包含一个字典
            if files[0]:
                dict_img = files[0]
                filename = dict_img['filename']
                print(filename)
                print(dict_img['content_type'])
                content = dict_img['body']
                _, ext = os.path.splitext(filename)
                upload_im = UploadImage(ext, self.application.settings['static_path'])
                upload_im.save_content(content)
                upload_im.make_thumb()
                post_id = self.orm.add_post(self.current_user, upload_im.image_url, upload_im.thumb_url)
                if post_id:
                    self.redirect('/post/{}'.format(str(post_id)))
            else:
                self.write("上传失败，系统不听话")
        except Exception as e:
            print(e)
            self.redirect('/upload')


class RegisterHandler(BaseHandler):
    """
    用户注册
    """
    def get(self):
        self.render('user/register.html')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')
        gender = self.get_argument('gender', '')
        age = self.get_argument('age', ' ')
        if not self.db_session.query(User.username).filter(User.username == username).first():
            value = self.orm.add_user(username, password, email, age, gender)
            if value == 'ok':
                self.session.set("username_session", username)
                self.redirect('/')
            else:
                self.write("不好意思哦，注册失败！！！！")
        else:
            self.write('用户名已经存在！！！')


class LoginHandler(BaseHandler):
    def get(self):
        next_url = self.get_argument('next', '/')
        print(next_url)
        if self.current_user:
            print("此时的session对应的值为{}".format(self.current_user))
            self.redirect(next_url)
        else:
            self.render('user/login.html', next_url=next_url,msg="暂时无问题！！")
        # if self.get_cookie("define_cookie"):
        #     username = self.get_cookie("define_cookie")
        #     session = Session()
        #     users = session.query(User.id, User.username, User.gender, User.age, User.creatime, User.emial,).all()
        #     self.render('user/information.html', username=username, users=users)
        # else:
        #     self.render('user/login.html')

    def post(self):
        next_url = self.get_argument('next_url', '/')
        username = self.get_argument("username", '')
        password = self.get_argument("password", '')
        ret = self.orm.user_login(username, password)
        if ret is not None:
            # if not self.get_cookie("define_cookie"):
            #     self.set_cookie("define_cookie", username)
            #     if  value == True:
            #         session = Session()
            #         users = session.query(User.id, User.username, User.gender, User.age, User.creatime, User.emial,).all()
            #         self.render('user/information.html', users=users, username =username)
            #     else:
            #         self.write('出现{}'.format(value))
            if not self.session.get('username_session'):
                if ret['result'] == True:
                    self.session.set("username_session", username)
                    # session = Session()
                    # users = session.query(User.id, User.username, User.gender, User.age, User.creatime, User.emial,).all()
                    # self.render('user/information.html', users=users, username=username)
                    self.redirect(next_url)
                else:
                    self.render('user/login.html', next_url=next_url, msg=ret['msg'])
        else:
            self.render('user/login.html', next_url=next_url, msg='用户名不存在')


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.session.delete('username_session')
        next_url = self.get_argument('next', '/')
        self.render('user/login.html', msg="退出成功！！", next_url=next_url)


class CheckHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.db_session.query(User).filter_by(username=self.current_user).first()
        post_id = user.id
        self.redirect('/post/{}'.format(str(post_id)))


class Collect_pictureHandler(BaseHandler):
    """
    收藏图片操作
    """
    @tornado.web.authenticated
    def get(self, user_id, post_id):
        msg =self.orm.collect_picture(user_id, post_id)
        if msg =='收藏成功':
            self.redirect('/one_picture/{}'.format(str(post_id)))


class CanclepictureHandler(BaseHandler):
    def get(self, user_id, post_id):
        self.orm.cancle_picture(user_id)
        self.redirect('/one_picture/{}'.format(str(post_id)))


class ProfileHandler(BaseHandler):
    """
    查看个人和各个用户的上传图片和收藏的图片
    """
    @tornado.web.authenticated
    def get(self):
        username1 = self.get_argument('username', '')
        user = self.orm.get_user(username1)
        username_current = self.current_user
        user_id = self.db_session.query(User.id).filter_by(username=username1).first()[0]
        post_ids = self.db_session.query(LikePost.post_id).filter_by(user_id=user_id).all()
        list_post = []
        if post_ids:
            for post_id in post_ids:
                   every_post = self.db_session.query(Post).filter_by(id=post_id[0]).first()
                   list_post.append(every_post)
        else:
            list_post = []
        self.render('profile.html', user=user, like_post=list_post, username=username_current)


class CollectCenterHandler(BaseHandler):
    """
    查看个人收藏图片的个人中心
    """
    @tornado.web.authenticated
    def get(self):
        username = self.get_argument('username', '')
        user_id = self.db_session.query(User.id).filter_by(username=username).first()[0]
        post_ids = self.db_session.query(LikePost.post_id).filter_by(user_id=user_id).all()
        list_post = []
        if post_ids:
            for post_id in post_ids:
                   every_post = self.db_session.query(Post).filter_by(id=post_id[0]).first()
                   list_post.append(every_post)
            self.render('user/collectcenter.html', list_post=list_post, username=self.current_user, user_id=user_id, msg='有喜欢图片')
        else:
            self.render('user/collectcenter.html', msg="无喜欢图片", username=self.current_user)






