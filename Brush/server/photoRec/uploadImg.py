import base64
import os
from django.http import HttpResponse


#图片存储/读取  输入：request的name，图片  输出：是否成功
def upload_image(page_id, img):
    data = {'success': 0, 'path': ''}
    if img != "":
        img = base64.b64decode(img)
        cur = os.path.abspath(".")
        save_path = os.path.join(cur, "Brush\\webPageImg\\" + page_id)
        with open(save_path, "wb") as file:
            file.write(img)
        data['success'] = 1
        data['path'] = save_path
        return data
