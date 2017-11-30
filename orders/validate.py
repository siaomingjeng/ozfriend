import random
import base64
import io
from PIL import Image, ImageFont, ImageDraw
from django.conf import settings


def get_validate_img(req):
    def rndtxtcolor2():  # 字体颜色
        return (random.randint(32, 127), random.randint(32, 127),
                random.randint(32, 127))

    def rndbgcolor():  # 背景颜色
        return (random.randint(64, 255), random.randint(64, 255),
                random.randint(64, 255))

    def rndtxt():
        txt_list = []
        # txt_list.extend([i for i in range(65, 90)])  # 大写字母
        # txt_list.extend([i for i in range(97, 123)])  # 小写字母
        # txt_list.extend([i for i in range(50, 57)])  # 数字
        txt_list.extend([i for i in range(33, 123)])  # ALL
        return chr(txt_list[random.randint(0, len(txt_list)-1)])

    width = 250
    hight = 60
    image = Image.new('RGB', (width, hight), (255, 255, 255))
    # 注意字体文件的位置。
    # font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans.ttf', 36)
    font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationSans-Regular.ttf',36)
    draw = ImageDraw.Draw(image)
    for x in range(width):  # 填充背景颜色
        for y in range(hight):
            draw.point((x, y), fill=rndbgcolor())
    verify = ""
    for t in range(6):  # 生成随机验证码
        rndchr = rndtxt()
        verify += rndchr
        draw.text((40 * t + 10, 10), rndchr, font=font, fill=rndtxtcolor2())
    req.session[settings.VALIDATE_SESSION_ID] = verify
    return image


def validated(req, digit=2):
    if 'verify' in req.POST.keys():
        return req.session[settings.VALIDATE_SESSION_ID][:digit]\
               == req.POST["verify"][:digit]
    else:
        return False
