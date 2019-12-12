from glob import glob
list_imgs = glob('static/upload/*')
new_list_img = []
for list_img in list_imgs:
    new1 = list_img.replace('static/upload/', 'upload/')
    new_list_img.append(new1)

list_thumbs = glob('static/thumbs/*')
new_list_thumb = []
for list_thumb in list_thumbs:
    new1 = list_thumb.replace('static/thumbs/', 'thumbs/')
    new_list_thumb.append(new1)
print(new_list_thumb)

