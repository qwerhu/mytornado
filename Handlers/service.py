import requests
import tornado.web,tornado.gen
from tornado.httpclient import AsyncHTTPClient
import time
import logging
from utiles.photo import UploadImage
from Handlers.main import BaseHandler

logger = logging.getLogger('xiaolong.log')


class SynSaveHandler(BaseHandler):
    """
    主要是不通过上传图片来达到图片抓取的效果，代替了上传的功能
    （同步的方式进行）
    """
    @tornado.web.authenticated
    def get(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)
        resp = requests.get(save_url)
        # time.sleep(30),等待过程
        if resp.status_code is 200:
            up_img = UploadImage('.jpg', self.settings['static_path'])
            up_img.save_content(resp.content)
            up_img.make_thumb()
            post_id = self.orm.add_post(self.current_user, up_img.image_url, up_img.thumb_url)
            if post_id:
                self.redirect('/post/{}'.format(str(post_id)))
        else:
            self.write('错误')


class SaveHandler(BaseHandler):
    """
    主要是不通过上传图片来达到图片抓取的效果，代替了上传的功能
    （异步的方式进行,异步函数一定要有yield关键字来表示）
    """
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)
        client = AsyncHTTPClient()
        resp = yield client.fetch(save_url, request_timeout=400)
        logger.info("开启阻塞模式")
        yield tornado.gen.sleep(2)
        logger.info("关闭阻塞模式")
        logger.info(resp.code)
        if resp.code is 200:
            up_img = UploadImage('.jpg', self.settings['static_path'])
            up_img.save_content(resp.body)
            up_img.make_thumb()
            post_id = self.orm.add_post(self.current_user, up_img.image_url,\
                                        up_img.thumb_url)
            if post_id:
                self.redirect('/post/{}'.format(str(post_id)))
        else:
            self.write('错误')

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)
        client = AsyncHTTPClient()
        resp = yield client.fetch(save_url, request_timeout=400)
        logger.info("开启阻塞模式")
        yield tornado.gen.sleep(2)
        logger.info("关闭阻塞模式")
        logger.info(resp.code)
        if resp.code is 200:
            up_img = UploadImage('.jpg', self.settings['static_path'])
            up_img.save_content(resp.body)
            up_img.make_thumb()
            post_id = self.orm.add_post(self.current_user, up_img.image_url, \
                                        up_img.thumb_url)
            if post_id:
                self.redirect('/post/{}'.format(str(post_id)))
        else:
            self.write('错误')

