import random
from models.auth import User, Post, LikePost, Quotes
from hashlib import md5
from sqlalchemy_pagination import paginate



def hash(text):
    return md5('{}+{}'.format(text, 'jiayan').encode()).hexdigest()


class OrmHandler:
    """
    配合RequestHandler实例化的session一起使用
    """
    def __init__(self, session):
        self.session = session

    def get_all_posts(self, page=1):
        """
        获取所有图片
        """
        data_all = self.session.query(Post).filter(Post.user_id != None).order_by(-Post.id)
        pg = paginate(data_all, page, 14)
        return pg

    # def get_all_posts_index(self, page=1):
    #     """
    #     获取所有图片
    #     """
    #     data_all = self.session.query(Post).order_by(-Post.id)
    #     pg = paginate(data_all, page, 9)
    #     return pg

    def get_all_users(self):
        """
        获取所有用户的信息
        :return:
        """
        users = self.session.query(User.id, User.username, User.gender, User.age, User.creatime, User.emial,User.power).all()
        return users

    def add_user(self, username, password, email, age, gender,):
        """
        进行用户注册
        :param username:
        :param password:
        :param email:
        :return:
        """
        if username and password:
            user = User(username=username, password=password, emial=email, age=age, gender=gender, )
            self.session.add(user)
            self.session.commit()
            return 'ok'
        else:
            return 'false'

    def add_post(self, username, image_url, thumb_url):
        user = self.session.query(User).filter_by(username=username).first()
        post = Post(user_id=user.id, image_url=image_url, thumb_url=thumb_url)
        self.session.add(post)
        self.session.commit()
        post_id = post.user_id
        return post_id

    def user_login(self, username, password):
        """
        用户登录模块
        :param username:
        :param password:
        :return:
        """
        try:
            ret = {'result': False}
            if username and password:
                user = self.session.query(User).filter_by(username=username).first()
                # if hash(session.query(User.password).filter(User.username == username).first()[0]) == hash(password):
                if hash(user.password) == hash(password):
                    ret['result'] = True
                else:
                    ret['msg'] = '密码错误'
            else:
                ret['msg'] = '用户名和密码不能为空'
            return ret
        except:
            pass

    def collect_picture(self, user_id, post_id):
        if user_id and post_id:
            like_post = LikePost(user_id=user_id, post_id=post_id)
            self.session.add(like_post)
            self.session.commit()
            msg = "收藏成功"
            return msg

    def cancle_picture(self, user_id):
        self.session.query(LikePost).filter_by(user_id=user_id).update({LikePost.user_id: None, LikePost.post_id: None})
        self.session.commit()

    def get_user(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        return user

    def get_one_quotes(self):
        list_id = []
        quotes_all_id = self.session.query(Quotes.id).all()
        for id1 in quotes_all_id:
            list_id.append(id1[0])
        quotes_id = random.choice(list_id)
        quotes_one = self.session.query(Quotes).filter_by(id=quotes_id).first()
        return quotes_one

    def get_three_user(self):
        user_all_id = self.session.query(User.id).all()
        # print(user_all_id)
        list_user_all_id = []
        for user_id in user_all_id:
            list_user_all_id.append(user_id[0])
        # print(list_user_all_id)

        list_user_id = []
        list_post_size = []
        list_post_number = []
        for user_id in list_user_all_id:
            value = self.session.query(Post).filter_by(user_id=user_id).all()
            list_post_size.append(len(value))
        # print(list_post_size)
        for i in range(0, 3):
            index = list_post_size.index(max(list_post_size))
            list_user_id.append(list_user_all_id[index])
            list_post_number.append(list_post_size[index])
            del list_post_size[index]
            del list_user_all_id[index]

        # print(list_user_id)
        final_user = []
        for value1 in list_user_id:
            final_user.append(self.session.query(User).filter_by(id=value1).first())
        final_value = [final_user, list_post_number]
        return final_value

    def get_liked_posts(self, username):
        user_id = self.session.query(User.id).filter_by(username=username).first()[0]
        posts_id = self.session.query(Post.id).filter_by(user_id=user_id).all()
        list_posts_id = []
        for post_id in posts_id:
            list_posts_id.append(post_id[0])
        single_length = []
        no_like_post_id = []
        for post_id in list_posts_id:
            data = self.session.query(LikePost).filter_by(post_id=post_id).all()
            if len(data) > 0:
                single_length.append(len(data))
            else:
                no_like_post_id.append(post_id)
        list_data = [single_length,no_like_post_id]
        return list_data

    def get_no_like_posts(self, list_data):
        no_like_posts_data = []
        for no_like_post in list_data:
            data = self.session.query(Post).filter_by(id=no_like_post).all()
            no_like_posts_data.append(data)
        return no_like_posts_data

    def add_quotes(self, author, country, content):
        rows = Quotes(author=author,country=country,quotes_content=content)
        self.session.add(rows)
        self.session.commit()

    def delete_post(self, post_id):
        self.session.query(Post).filter_by(id=post_id).update({Post.user_id: None})
        self.session.query(LikePost).filter_by(post_id=post_id).update({LikePost.post_id: None, LikePost.user_id: None})
        self.session.commit()

    def get_user_password(self, username):
        value = self.session.query(User.password).filter_by(username=username).first()
        if value:
            return_msg = value[0]
            return return_msg
        else:
            return_msg = '用户不存在,无密码'
            return return_msg




