import datetime
import random
from models.db import session
from models.auth import User,Quotes,Post,LikePost

#1、增加操作
# person = User(username='小龙', password='qwe123')
# session.add(person)
# session.commit()
# session.add_all([User(username='tuple', password='123'),  User(username='which', password='1234')])
# session.commit()

# #2、查找操作
# rows5 = session.query(User.password).filter(User.username == 'admin').first()[0]
# print(rows5)
# print(session.query(User.id, User.username, User.emial).all())

#3、修改操作
# rows = session.query(User).filter(User.username == '小龙').update({User.password: 3})
# print(rows)
# session.commit()

#4、删除
# rows = session.query(User).filter(User.username=='小龙')[0]
# print(rows)
# session.delete(rows)
# session.commit()

# quotes_all = session.query(Quotes).all()
# print(len(quotes_all))
# quotes_id = random.randint(1, len(quotes_all))
# print(quotes_id)
# list_id = []
# quotes_all_id = session.query(Quotes.id).all()
# for id1 in quotes_all_id:
#     list_id.append(id1[0])
# print(list_id)
# quotes_id = random.choice(list_id)
# print(quotes_id)
# user_all_id = session.query(User.id).all()
# print(user_all_id)
# list_user_all_id = []
# for user_id in user_all_id:
#     list_user_all_id.append(user_id[0])
# print(list_user_all_id)
#
# list_user_id = []
# list_post_size = []
# list_post_number = []
# for user_id in list_user_all_id:
#     value = session.query(Post).filter_by(user_id=user_id).all()
#     list_post_size.append(len(value))
# print(list_post_size)
# for i in range(0, 3):
#     index = list_post_size.index(max(list_post_size))
#     list_user_id.append(list_user_all_id[index])
#     list_post_number.append(list_post_size[index])
#     del list_post_size[index]
#     del list_user_all_id[index]
#
# final_user = []
# for value1 in list_user_id:
#     final_user.append(session.query(User).filter_by(id=value1).first())
#
#
# list_value = [final_user, list_post_number]
# v1, v2 = list_value
# print(v1, v2)

#
# user_id = session.query(User.id).filter_by(username='曹佳乐').first()[0]
# print(user_id)
# posts_id = session.query(Post.id).filter_by(user_id=user_id).all()
# print(posts_id)
# list_posts_id = []
# for post_id in posts_id:
#     list_posts_id.append(post_id[0])
# print(list_posts_id)
#
# single_length = []
# no_like_post_id = []
# for post_id in list_posts_id:
#     data = session.query(LikePost).filter_by(post_id=post_id).all()
#     if len(data) > 0:
#         single_length.append(len(data))
#     else:
#         no_like_post_id.append(post_id)
#
# print(single_length)
# print(no_like_post_id)
# print(sum(single_length))
# no_like_posts_data = []
# for no_like_post in no_like_post_id:
#     data = session.query(Post).filter_by(id=no_like_post).all()
#     no_like_posts_data.append(data)
# print(no_like_posts_data)

# l1 = session.query(User.id, User.username).filter(User.username.like('曹%')).all()
# l2 = session.query(User.id, User.username).filter(User.username.notlike('曹%')).all()
# print(l1)
# print(l2)
# l3 = session.query(User.id).filter(User.username.in_(['曹佳乐', '李小白'])).all()
# l4 = session.query(User.id).filter(User.username.notin_(['曹佳乐', '李小白'])).all()
# print(l3)
# print(l4)
# from sqlalchemy import desc
# l1 = session.query(User.username).filter(User.username!='曹佳乐').slice(1, 3).all()
# print(l1)
# l2 = session.query(User.username).filter(User.username!='曹佳乐').offset(1).all()
# print(l2)
# l3=session.query(User.username).filter(User.username!='曹佳乐').order_by(User.id).all()
# print(l3)
# l4 = session.query(User.username).filter(User.username!='曹佳乐').order_by(desc(User.id)).all()
# print(l4)

# l5 = session.query(User.username).filter(User.username!='曹庆').order_by(User.age).all()
# print(l5)
# from sqlalchemy import extract, func
# l6 = session.query(User.password, func.count(User.id)).group_by(User.password).all()
# print(l6)
# l7 = session.query(User.password, func.count(User.id)).group_by(User.password).having(func.count(User.id)>1).all()
# print(l7)
# l8 = session.query(User.age, func.sum(User.id)).group_by(User.age).all()
# print(l8)

# from sqlalchemy import extract, func, or_
# l9 = session.query(User.age, func.max(User.id)).group_by(User.age).all()
# print(l9)
# l10 = session.query(User.password, func.min(User.id)).group_by(User.password).all()
# print(l10)
# l11 = session.query(extract('minute',User.creatime).label('minute'), func.count(User.id)).group_by('minute').all()
# print(l11)
# l12 = session.query(User.username).filter(or_(User.username != 'admin', User.password!='admin')).all()
# print(l12)
# l13 = session.query(User.username, Post.id).join(Post,Post.user_id==User.id)
# print(l13)
# l14 = session.query(User.username, Post.id).join(Post,Post.user_id==User.id).all()
# print(l14)






















