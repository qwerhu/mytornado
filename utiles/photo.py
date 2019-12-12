import uuid
import os
from PIL import Image


class UploadImage(object):
    """
    辅助保存用户上传的图片，生成对应的缩略图，记录图片相关的url，保存到数据库中
    """
    upload_dir = 'upload'
    thumb_dir = 'thumbs'
    thumb_size = (200, 200)

    def __init__(self, ext, static_path):
        self.ext = ext #文件的后缀名
        self.new_name = self.get_new_name() + self.ext #形成新的文件名
        self.static_path = static_path  #获取settings中的static_path的值

    def get_new_name(self):
        return uuid.uuid4().hex  #用 uuid 库生成的字符串使上传图片的名字变得唯一

    @property
    def image_url(self):
        return os.path.join(self.upload_dir, self.new_name)#保存到数据库中的图片路径

    @property
    def save_to(self):
        return os.path.join(self.static_path, self.image_url)#将上传的图片保存到相关的路径中

    def save_content(self, content):
        with open(self.save_to, 'wb') as f:
            f.write(content)

    @property
    def thumb_url(self):
        name, ext = os.path.splitext(self.new_name)#获取扩展名，这是一个元组对象
        thumb_name = '{}_{}X{}{}'.format(name, self.thumb_size[0], self.thumb_size[1], ext)
        return os.path.join(self.thumb_dir, thumb_name)

    def make_thumb(self):
        im = Image.open(self.save_to)           #生成相应的缩略图,第一步打开图片获取其内容
        im.thumbnail(self.thumb_size)
        path = os.path.join(self.static_path, self.thumb_url)
        im.save(path)




