import tornado.web
from tornado.options import options, define, parse_command_line
import tornado.ioloop
from Handlers import main, main_option, chat, service

define('port', default=8080, help="运行端口")


def make_app():
    handlers = [
        (r'/explore', main.ExploreHandler),
        (r'/', main.IndexHandler),
        (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
        (r'/upload', main.UploadHandler),
        (r'/uploadquote', main_option.UploadQuoteHandler),
        (r'/register', main.RegisterHandler),
        (r'/login', main.LoginHandler),
        (r'/logout', main.LogoutHandler),
        (r'/check', main.CheckHandler),
        (r'/one_picture/(?P<post_id>[0-9]+)', main.One_pictureHandler),
        (r'/updateuser/(?P<user_id>[0-9]+)', main_option.UpdateUserHandler),
        (r'/delete/(?P<user_id>[0-9]+)', main_option.DeleteUserHandler),
        (r'/updatequote/(?P<quote_id>[0-9]+)', main_option.UpdateQuotesHandler),
        (r'/deletequote/(?P<quote_id>[0-9]+)', main_option.DeleteQuoteHandler),
        (r'/collect/(?P<user_id>[0-9]+)/(?P<post_id>[0-9]+)', main.Collect_pictureHandler),
        (r'/collectcenter', main.CollectCenterHandler),
        (r'/profile', main.ProfileHandler),
        (r'/administrator', main.AdministratorHandler),
        (r'/quotes', main_option.QuotesHandler),
        (r'/selfupdate', main_option.SelfUserInformationUpdateHandler),
        (r'/selfpost', main_option.SelfPostManagementHandler),
        (r'/deletepost/(?P<post_id>[0-9]+)', main_option.DeletePostHandler),
        (r'/canclecollect/(?P<user_id>[0-9]+)/(?P<post_id>[0-9]+)', main.CanclepictureHandler),
        (r'/findpwd', main_option.FindPassword),
        (r'/ws', chat.RoomWebSocket),
        (r'/room', chat.RoomHandler),
        (r'/save', service.SaveHandler)
    ]

    setting1 = {
        'debug': True,
         'static_path': 'static',
         'template_path': 'templates',
         "login_url": "/login",
        'cookie_secret': "12323",
         'pycket': {
             'engine': 'redis',
             'storage': {
                 'host': '192.168.212.131',
                 'port': 6379,
                 'db_sessions': 5,  # redis db index
                 'db_notifications': 11,
                 'max_connections': 2 ** 30,
             },
             'cookies': {
                 'expires_days': 30,
             },
         }
         }#直接写staic这里是相对路径，这是相对与这个脚本的路径而言的

    app = tornado.web.Application(handlers=handlers, **setting1)
    return app


if __name__ == '__main__':
    app = make_app()
    parse_command_line()
    port_new = options.port
    app.listen(int(port_new))
    print(type(port_new))
    print("Tornado server running at %s port" % port_new)
    tornado.ioloop.IOLoop.current().start()
