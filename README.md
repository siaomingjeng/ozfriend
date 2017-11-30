****************************商店建设***Django******Python3***********Virtual Environment**********************

1. <<<<<<<<<<<<<<<<*************安装python3和pip3*************>>>>>>>>>>>>>>>>>>>

wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz

tar -xvzf Python-3.6.2.tgz

cd Python-3.6.2

./configure --enable-shared --enable-optimizations --with-threads --prefix=/usr/local/python3

make

make install

ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3   #链接到python3

export LD_LIBRARY_PATH=/usr/local/python3/lib  #可以解决库libpython3.6m.so.1.0找不到的问题

安装pip3：

wget --no-check-certificate https://github.com/pypa/pip/archive/9.0.1.tar.gz

tar -zvxf 9.0.1 -C pip-9.0.1

cd pip-9.0.1

python3 setup.py install

ln -s /usr/local/python3/bin/pip /usr/bin/pip3

pip install --upgrade pip   #升级pip

第二种方法：从IUS安装：(建议)

yum -y install https://centos7.iuscommunity.org/ius-release.rpm

yum install python36u

yum install python36u-devel

ln -s /usr/bin/python3.6 /usr/bin/python3    (#用的是软连接 symbolic link  相当于windows的快捷方式。 )

(#去掉-s 就是硬链接了，hard link直接指向文件节点。)

安装pip3

yum install python36u-pip

----------------------------------------------------------------------

2. 创建virtualenv using python3

virtualenv env3 -p /usr/bin/python3.6    #pip3 会自动安装好的

pip install pillow

pip install django

pip install requests

pip install mysqlclient

pip install python-slugify

pip install selenium

pip install pyquery

pip install mod_wsgi

----------------------------------------------------------------------

3. 安装MariaDB

yum install mariadb mariadb-server

systemctl start mariadb

systemctl enable mariadb

yum install httpd

yum install httpd-devel gcc

--------------------------------------------------------------------

4. 创建database，user，password：

create database ozfriend default charset=utf8;

grant all on ozfriend.* to ozfriend@'localhost' identified by 'ozfriend'; '%'表示任意网址可以来访问。

flush privileges;

--------------------------------------------------------------------

5. 创建django工程，并配置settings

ALLOWED_HOSTS = ['192.168.1.253']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ozfriend',
        'USER': 'ozfriend',
        'PASSWORD': 'ozfriend',
        'HOST': '',
        'PORT': '',
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #定制管理模板的位置
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',  #每次递交都更新的processor
            ],
        },
    },
]

TIME_ZONE = 'Australia/Sydney'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
CART_SESSION_ID = 'cart'  #每个访问用户都会有一个‘cart’。
---------------------------------------------------------------------------------

6. 解决python3与MariaDB/MySQL和Django之间通信
在项目文件下（settings 同目录）的__init__.py中添加：
import pymysql
pymysql.install_as_MySQLdb()

方法二：（Django官网推荐）
yum install mariadb-devel （用mysql-devel会自动跳到mariadb-devel）
pip install mysqlclient
-------------------------------------------------------------------------------

7. python下的slug 包
pip install python-slugify
from slugify import slugify
使用范例：
txt = "This is a test ---"
r = slugify(txt)   #  'this-is-a-test'
-------------------------------------------------------------------------

8.0  删除自己的app目录的migration目录下的除了__init__.py以外的所有文件
    #准备相应的表
    python manage.py makemigrations
    python manage.py migrate
    #导入之前的数据
    python manage.py loaddata data-backup-16SEP-ourdata-all.json
---------------------------------------------------------------------------
8. 生产环境部署Django1.11.4+Apache2.4+CentOS7+MariaDB

8.1 安装Apache, MariaDB(见3)

8.2 安装mod_wsgi：***************
    cd env3/
    source bin/active
    pip install mod_wsgi
    (需要：yum install httpd-devel gcc)

8.3 配置mod_wsgi:
    mod_wsgi-express module-config > /etc/httpd/conf.modules.d/00-wsgi.conf
    生成的内容为：
    LoadModule wsgi_module "/root/env3/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
    WSGIPythonHome "/root/env3"
    要在目录/etc/http/conf.modules.d/* 和 /etc/http/conf.d/* 及文件/etc/http/conf/httpd.conf 中，
    查找LoadModule wsgi_module，如果有，要用#屏蔽掉。
    systemctl restart httpd

8.4 配置Apache虚机:(在Apache虚拟机中监控端口，指定static和media目录和WSGI进程，指定虚拟环境中的python)
Listen 8001
<VirtualHost 0.0.0.0:8001>
    Alias /static /root/env3/ozfriend/static
    <Directory /root/env3/ozfriend/static>
        Options Indexes MultiViews FollowSymLinks  #实际生产环境，不应该给出这个权限
        Require all granted
    </Directory>
    Alias /media /root/env3/ozfriend/media
    <Directory /root/env3/ozfriend/media>
        Options Indexes MultiViews FollowSymLinks
        Require all granted
    </Directory>
    <Directory /root/env3/ozfriend/ozfriend>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    WSGIDaemonProcess ozfriend python-path=/root/env3/ozfriend:/root/env3/lib/python3.6/site-packages
    WSGIProcessGroup ozfriend
    WSGIScriptAlias / /root/env3/ozfriend/ozfriend/wsgi.py
</VirtualHost>

8.5 安装依赖包：
    pip install pillow
    pip install django
    pip install mysqlclient

8.6 测试：
    cd /root/env3/ozfriend
    source ../bin/active
    python manage.py collectstatic  #收集静态文件
    python manage runserver 0:8080
    网页正常访问，说明django代码和依赖没问题。 

8.7 权限配置 (没有进行此项设置，默认第三方有执行权限)
    usermod -a -G 用户 apache   # 将apache加入到‘用户’同组。
    chmod 710 /home/用户   #配置最小权限
    #常用命令：
    groups 查看当前用户的组
    groups apache 查看apache所在组
    cat /etc/group 查看所有组

8.8 生产环境测试：
    访问8001端口正常，说明生产环境部署完毕。

8.9 数据库导入及备份(未完待续！！！)
----------------------------------------------------------------------

O.1:《《《重置django中的id》》》
python manage.py dbshell
mysql> ALTER TABLE <table_name> AUTO_INCREMENT = 1;
---------------------------------------------------------------------------

O.2: 从网站抓取数据，存入product中
import os
import django
import datetime
import random
import re
import slugify
from selenium import webdriver
from pyquery import PyQuery as pq
#环境设置
os.chdir('/root/env3/ozfriend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ozfriend.settings")
django.setup()

def fetch_autosomg(url):
    path = "/myapp/phantomjs/bin/phantomjs"
    phantomjs = webdriver.PhantomJS(executable_path=path)
    phantomjs.get(url)
    weight=cost=0
    try:
        w = phantomjs.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[3]/span').text
        c = phantomjs.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div[3]/span[1]').text
        weight = int(re.search(r'\d+',w).group())
        cost = float(re.search(r'\d+\.\d+',c).group())
    except Exception as e:
        print(e)
    price=(cost+10+weight/1000*4)*5.5
    chinese=phantomjs.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/h1/a').text
    href=phantomjs.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/h1/a').get_attribute('href')
    description=phantomjs.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/div[2]/ul').text.split('****')[0]

    if 'coles' in href:
        phantomjs2 = webdriver.PhantomJS(executable_path=path)
        phantomjs2.get(href)
        ico=phantomjs2.find_element_by_xpath('//*[@id="main-content-inside"]/div[2]/div/section/header/div[2]/img').get_attribute('src')
        name=phantomjs2.find_element_by_xpath('//*[@id="pdp-product-title"]/span/span[3]').text
        image = ""
        slug=slugify.slugify(name)
        tail=ico.split('.')[-1]
        sysstr='wget '+ico+' -O '+'./TmpImg/ICO_'+slug+'.'+tail
        os.system(sysstr)
	ico = './TmpImg/ICO_'+slug+'.'+tail
    elif 'chemistwarehouse' in href:
        d = pq(url=href)
        name = d('div.product-name h1').text()
        ico = d('a.image_enlarger img').attr('src2')
        image = d('a.image_enlarger').attr('href')
        slug=slugify.slugify(name)
        tail=image.split('.')[-1]
        sysstr='wget '+image+' -O '+'./TmpImg/IMAGE_'+slug+'.'+tail
        os.system(sysstr)
        tail=ico.split('.')[-1]
        sysstr='wget '+ico+' -O '+'./TmpImg/ICO_'+slug+'.'+tail
        os.system(sysstr)
	image = './TmpImg/IMAGE_'+slug+'.'+tail
	ico = './TmpImg/ICO_'+slug+'.'+tail
    else:
        seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa=[random.choice(seed) for i in range(6)]
        name = ''.join(sa)+slugify.slugify(str((datetime.datetime.now())))
        image = ""
        slug=slugify.slugify(name)
        ico = phantomjs.find_element_by_xpath("/html/body/div[4]/div[2]/div[1]/div[1]/ul/li/img").get_attribute('src')
        tail=ico.split('.')[-1]
        sysstr='wget '+ico+' -O '+'./TmpImg/ICO_'+slug+'.'+tail
        os.system(sysstr)
	ico = './TmpImg/ICO_'+slug+'.'+tail

    return {'chinese':chinese, 'name':name, 'slug':slug, 'weight':weight, 'cost':cost,
            'price':price, 'reference':url, 'description':description, 'image':image, 'ico':ico}

#从Excel文件中读入ausomg的网址列表
from openpyxl import load_workbook
def fetch_url_list(filename="daigoulist.xlsx", sheetname="Sheet1"):
    values = []
    wb = load_workbook(filename=filename)
    sheet = wb[sheetname]
    for i in range(2, sheet.max_row):
        if sheet['b' + str(i)].value:
            values.append(sheet['b' + str(i)].value)
    return values
-------------------------------------------------------------------------------
O.3 admin界面深度定制：
    ozfriend/settings中配置admin templates. (见5)
    将change_form.html复制到ozfriend/templates/orders/admin/中，并添加js代码或者文件
    自己写的js文件，用以实现，Order管理界面的数据同步：orders/static/orders/js/pagesync.js
/* Written by Xiaoming Zheng on 30AUG for my Lover */
(function($) {
    $("tbody").change(function(){
        var aud=0;
        var rmb=0;
        $("tbody tr.has_original").each(function(index,e){
            rmb+=$(this).children(".field-price").children("input").val()*$(this).children(".field-quantity").children("input").val();  /*获取表单数据*/
            aud+=$(this).children(".field-expense").children("input").val()*$(this).children(".field-quantity").children("input").val();
        });
        $("#id_total_price").val(rmb.toFixed(2));
        $("#id_total_expense").val(aud.toFixed(2));
        });
})(django.jQuery);
    change_form.html修改内容：(注意，格式，不是用的普通jquery引用，为命名空间纯净。)
{% block admin_change_form_document_ready %}
   <script type="text/javascript"
            id="django-admin-form-add-constants"
            src="{% static 'admin/js/change_form.js' %}"
            {% if adminform and add %}
                data-model-name="{{ opts.model_name }}"
            {% endif %}>
    </script>
    <script type="text/javascript" src="{% static 'js/pagesync.js' %}">  此行为添加内容
    </script>
{% endblock %}
------------------------------------------------------------------------------

o.4 admin修改主题：
    ozfriend/urls.py中添加：
    admin.site.site_header = "OZFriend Management System"
    admin.site.site_title = "OZFriendAdmin"
-----------------------------------------------------------------------------------

o.5 admin中加入自己的页面：
    #<<<admin主页中添加自己的网页链接，做成和原有一样：>>>
    #创建模板：reports/templates/reports/ozfriend_report_list.html 
<div class="app-reports module">
    <table>
        <caption>
            <a href="/admin/reports/" class="section">Statistic Reports</a>
        </caption>
        <tr class="model-reports">
            <th scope="row"><a href="/admin/reports/annual">Annual Report</a></th>
            <td><a href="" class="addlink">Add</a></td>
            <td><a href="" class="changelink">Change</td>
        </tr>
        <tr class="model-reports">
            <th colspan=1 scope="row"><a href="/admin/reports/monthly">Monthly Report</a></th>
            <td><a href="" class="addlink">Add</a></td>
            <td><a href="" class="changelink">Change</td>
        </tr>
        <tr class="model-reports">
            <th colspan=1 scope="row"><a href="/admin/reports/payer">Payer Report</a></th>
            <td><a href="" class="addlink">Add</a></td>
            <td><a href="" class="changelink">Change</td>
        </tr>
    </table>
</div>
    #复制index.html模板到:ozfreind/templates/admin/index.html 并在
    {% block content %}
    <div id="content-main">????</div>
    {% endblock %}中的最后部分添加：
{% block ozfriendreport %}
{% include "reports/ozfriend_report_list.html" %}
{% endblock %}
    #<<<保证其他程序不会受到影响，需要如下修改，以使前面刚刚加入的代码不影响原有的程序>>>
    #复制app_index.html到ozfriend/templates/admin/app_index.html
    #在{% block sidebar %}{% endblock %}之前添加：{% block ozfriendreport%}{% endblock %}
   --------------------------------------
	

    #创建自己加入的程序的相关链接和页面
    python manage.py startapp reports
    #ozfriend/urls.py中添加如下的url：
    url(r'^admin/reports/', include('reports.urls', namespace='reports')),
    #reports/urls.py中内容:
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.report_list, name='report_list'),
    url(r'^annual$', views.annual_report, name='annual_report'),
    url(r'^monthly$', views.monthly_report, name='monthly_report'),
    url(r'^payer$', views.payer_report, name='payer_report'),
]
    #仿程序列表页面模板：
    #延续了admin/app_index.html这个admin模板
    #ozfrend/reports/templates/reports/report_index.html内容：
{% extends "admin/app_index.html" %}
{% block content %}
    {% include "reports/ozfriend_report_list.html" %}
    {% block ozfriendreport %}{{ block.super }}{% endblock %}
{% endblock %}
{% block sidebar %}
{% if marry_count %}<h1 color="#417690;">{{ marry_count }}</h1>{% endif %}
{% endblock %}
    #统计报表使用的模板（部分）：(为了使用时间选择的控件)
    #延续了admin/app_index.html这个admin模板，但是重写了{% block extrastyle %}，以消除原有的dashboard.css的影响。
{% extends "admin/app_index.html" %}

{% load static %}

{% block extrahead %}{{ block.super }}
<script src="{% static 'admin/js/core.js' %}"></script>
<script src="/admin/jsi18n/"></script>
<script src="{% static 'admin/js/vendor/jquery/jquery.js' %}"></script>
<script src="{% static 'admin/js/jquery.init.js' %}"></script>
<script src="{% static 'admin/js/calendar.js' %}"></script>
<script src="{% static 'admin/js/admin/DateTimeShortcuts.js' %}"></script>
{% endblock %}

{% block extrastyle %}
<link rel="stylesheet" type="text/css" href="{% static 'admin/css/base.css' %}" />
<link rel="stylesheet" type="text/css" href="{% static 'admin/css/forms.css' %}" />
<link rel="stylesheet" type="text/css" href="{% static 'reports/css/reports.css' %}" />
{% endblock %}



{% block breadcrumbs %}
<div class="breadcrumbs">
<a href="{% url 'admin:index' %}">Home</a>
&rsaquo; <a href="{% url 'reports:report_list' %}">Report</a>
&rsaquo; {{ report_type }}
</div>
{% endblock %}
{% block content %}
...
{% endblock %}
{% block sidebar %}
...
{% endblock %}

    #如果想脱离admin 单独使用时间，日期控件， 则要本模板多添加：
<script type="text/javascript">window.__admin_media_prefix__ = "{% filterescapejs %}{% static 'admin/' %}{% endfilter %}";</script>
    #并且在ozfriend/urls.py中添加：
 def i18n_javascript(request): return admin.site.i18n_javascript(request) patterns = [ ... url(r'^admin/jsi18n', i18n_javascript),  #必须在admin 之前。
------------------------------------------------------------------------------

O.6 让页面需要管理员权限才能访问：
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
------------------------------------------------------------------------------

O.7 让页面不收memcaceh缓冲影响：
from django.views.decorators.cache import never_cache  # use @never_cache
目前测试，还是不管用。本身也没有出现缓冲。取当前时间，要在函数/方法中取，否则会受影响。
------------------------------------------------------------------------------
O.8 计算我们结婚后 几年几月几天的程序， 不是具体的天数。Y-Y，M-M， D-D不够减时向前面一位借。
def YMD():
    def get_days_of_month(Y,M):
        D=[31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if M==2:
            return 27 if Y%4 else 28
        else:
            return D[M]
    from datetime import datetime
    now=datetime.now()
    dy=now.year-2016
    dm=now.month-3
    dd=now.day-25
    if dm<0:
        dy-=1
        dm+=12
    if dd<0:
        dm-=1
        dd+=get_days_of_month(now.year,now.month)
    return (dy,dm,dd)
---------------------------------------------------------------------------

O.9 Django 数据库备份：
    python manage.py dumpdata > db.json  #备份所有
    python manage.py dumpdata admin > db.json  #备份admin 这个app
    python manage.py dumpdata admin.logentry > db.json  #备份admin 这个app的logentry这个表
--------------------------------------------------------------------------------------

o.10 Django 添加自己的filter
    在程序中穿件templatetags目录
    在templatetags中touch __init__.py  #来告诉python这个是module，可以引入。
    创建ozfrend_tags.py #里面添加自己的filter函数，本例内容如下：
from django import template
register = template.Library()

@register.filter
def add_minus(value):
    return float(value) * -1

@register.filter
def show_aud(value):
    return "-$%.2f"%(-1*value) if value < 0 else "$%.2f"%value

@register.filter
def show_rmb(value):
    return "-￥%.2f"%(-1*value) if value < 0 else "￥%.2f"%value
---------------------------------------------------------------------------

o.11 改写model中的save方法，实现model中属性的default value设定为绑定外键的属性。

------------------------------------------------------------------------

o.12  Django Ajax POST 解决csrftoken问题
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
//下面的内容可以用在$.post(url,data,function(res){})的data字典中添加 'csrfmiddlewaretoken':csrftoken 来取代。
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
-----------------------------------------------------------------------------------------------

o.13 解决Mac OS下的附加属性问题@
    ls -al   #查看附加属性
    xattr -l  文件名   # 查看详细附加属性
    xattr -c  文件名   # 彻底删除附加属性

-------------------------------------------------------------------------------------------

o.14 生成验证码
#!/usr/bin/env python3
import random, base64, io
from PIL import Image,ImageFont,ImageDraw
from django.conf import settings


def get_validate_img(req):
    def rndtxtcolor2():  # 字体颜色
        return (random.randint(32,127),random.randint(32,127),random.randint(32,127))
    def rndbgcolor():  # 背景颜色
        return (random.randint(64,255),random.randint(64,255),random.randint(64,255))
    def rndtxt():
        txt_list = []
        #txt_list.extend([i for i in range(65,90)])  # 大写字母
        #txt_list.extend([i for i in range(97,123)])  # 小写字母
        #txt_list.extend([i for i in range(50,57)])  # 数字
        txt_list.extend([i for i in range(33,123)])  # ALL
        return chr(txt_list[random.randint(0,len(txt_list)-1)])

    weight = 250
    hight = 60
    image = Image.new('RGB',(weight,hight),(255,255,255))
    font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans.ttf',36) #CentOS7 注意字体文件的位置。
    #font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationSans-Regular.ttf',36) # RHEL 系统
    draw = ImageDraw.Draw(image)
    for x in range(weight):  # 填充背景颜色
        for y in range(hight):
            draw.point((x,y),fill=rndbgcolor())
    verify = ""
    for t in range(6):  # 生成随机验证码
        rndchr = rndtxt()
        verify += rndchr
        draw.text((40 * t + 10,10),rndchr,font=font,fill=rndtxtcolor2())
    req.session[settings.VALIDATE_SESSION_ID]=verify
    return image

def validated(req, digit=2):
    if 'verify' in req.POST.keys():
        return req.session[settings.VALIDATE_SESSION_ID][:digit] == req.POST["verify"][:digit]
    else:
        return False
#在orders/views.py中添加一个view：
def order_validate_img(req):
    image = get_validate_img(req)
    res = HttpResponse(content_type='image/png')
    image.save(res, 'png')
    return res
#对应的url中添加此view的地址:
url(r'^validate/$', views.order_validate_img, name='order_validate_img'),
#对应的模板中引用此网址{% url "orders:order_validate_img" %}
-------------------------------------------------------------------------------------------------
o.12 《《《《《《<<<<在django project 目录以外的地方，初始化django环境，调用django的功能>>>>》》》》》》》》》
方法一：
import os,sys,django
sys.path.append('/root/env3/ozfriend')  #讲工程目录加入环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ozfriend.settings")
os.chdir('/root/env3/ozfriend')
django.setup()
方法二：(其实就一种方法)
def __setup_django(project_path, settings):
    import os,sys,django
    os.chdir(project_path)
    sys.path.append(project_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ozfriend.settings")
    #above=os.environ['DJANGO_SETTINGS_MODULE'] = settings
    django.setup()
__setup_django('/root/env3/ozfriend','ozfriend.settings')


-------------------------------------------------------------------------------------------------


o.13 图像识别代码环境准备：
pip install pillow
pip install pytesseract   (or tesserocr)

yum install leptonica-devel, tesseract-devel
#参考资料https://pypi.python.org/pypi/tesserocr

import pytesseract
from PIL import Image
image = Image.open('vcode.png')
vcode = pytesseract.image_to_string(image)
print (vcode)
#以上只能识别背景不复杂的图片（不好用，没用这个）

---------------------------------------------------------------------------------------------

o.14 自己写的图像识别----基于hamming距离

phantomjs.get("http://ykjcx.yundasys.com/go.php?wen=998300395200")
img=phantomjs.find_element_by_css_selector('#wrapper > div.left > div:nth-child(2) > img')
img.screenshot('raw.png')


def initTable(threshold=140, flag=0):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(abs(flag-0))
        else:
            table.append(abs(flag-1))
    return table
#图片x轴的投影，如果有数据（黑色像素点）值为1否则为0
def get_projection_x(image):
    p_x = [0 for x in range(image.size[0])]
    for w in range(image.size[1]):
        for h in range(image.size[0]):
            if image.getpixel((h,w)) == 0:
                p_x[h] = 1
    return p_x

#图片y轴的投影，如果有数据（黑色像素点）值为1否则为0
def get_projection_y(image):
    p_y = [0 for y in range(image.size[1])] #Height
    for h in range(image.size[0]):  #width
        for w in range(image.size[1]):
            if image.getpixel((h,w)) == 0:
                p_y[w] = 1
    return p_y

def get_split_seq(projection_x,refine=False):
    res = []
    for idx in range(len(projection_x) - 1):
        p1 = projection_x[idx]
        p2 = projection_x[idx + 1]
        if p1 == 1 and idx == 0:
            res.append([idx, 1])
        elif p1 == 0 and p2 == 0:
            continue
        elif p1 == 1 and p2 == 1:
            res[-1][1] += 1
        elif p1 == 0 and p2 == 1:
            res.append([idx + 1, 1])
        elif p1 == 1 and p2 == 0:
            continue
    if refine:
        for i in range(len(res)-1):
            if res[i][1]>12:
                left=res[i][1]-10
                res[i][1]=10
                res.insert(i+1,[res[i][0]+11,left])
    return res

def get_images(bi, X, y):
    res=[]
    for i in range(len(X)):
        x=X[i]
        res.append(bi.crop(box=(x[0],y[0],x[0]+x[1],y[0]+y[1])))
    return res

image = Image.open('raw.png')
L=180
T=270
R=250
B=310
#im = image.crop(box=(192,279,243,294))
#预截图，获取边框的位置，为第二次精确截图获取数字做准备
im = image.crop(box=(L,T,R,B))
bl=im.convert('L') # 转灰度图
bi = bl.point(initTable(140,0), '1') #转二值图
bix=get_projection_x(bi)
biy=get_projection_y(bi)
bixr=get_split_seq(bix, True)  # 两个图片链接在一起的时候，以10个像素分割
biyr=get_split_seq(biy)

LL=L+bixr[0][0]+2
TT=T+biyr[0][0]+2
RR=LL+bixr[0][1]-4
BB=TT+biyr[0][1]-4
im = image.crop(box=(LL,TT,RR,BB))
bl=im.convert('L') # 转灰度图
bi = bl.point(initTable(140,1), '1') #转二值图
bix=get_projection_x(bi)
biy=get_projection_y(bi)
bixr=get_split_seq(bix, True)  # 两个图片链接在一起的时候，以10个像素分割
biyr=get_split_seq(biy)
im_got=get_images(bi, bixr[:3], biyr[0])
#准备样本,读进来的是0或者255， 要formalize 到0，1
digits=[]
for i in range(10):
    digits.append(Image.open('lib-{}.png'.format(i)).point(initTable(140,0), '1'))

signs=[]
for s in ['multiply', 'plus']:
    signs.append(Image.open('lib-{}.png'.format(s)).point(initTable(140,0), '1'))

def recognize(bi, digits=digits, sign=False):
    def hamming(bi, d):
        ham=0
        W=min(bi.size[0],d.size[0])
        H=min(bi.size[1],d.size[1])
        for w in range(W):
            for h in range(H):
                ham += bi.getpixel((w,h))^d.getpixel((w,h))
        return ham
    res=[]
    for d in digits:
        res.append(hamming(bi, d))
    if sign:
        return '*' if res[0]<res[1] else '+'
    else:
        return(str(res.index(min(res))))

def close_lib(source=digits+signs):
    sat=1
    for s in source:
        s.close()
    sat=0
    return sat

validate= recognize(im_got[0])+recognize(im_got[1],digits=signs,sign=True)+recognize(im_got[2]) 
if close_lib():
    print("Close Image Error")

#数字图片比对，运算符号比对

inp=phantomjs.find_element_by_css_selector('#yzm')
inp.send_keys(eval(validate[:3]))
button=phantomjs.find_element_by_css_selector('#wrapper > div.right > input[type="submit"]')
button.click()
status=phantomjs.find_element_by_css_selector('#fet > tbody > tr:last-child').text

-------------------------------------------------------------------------------
0.15 Django Admin change页面添加按钮，执行自定义操作（讲要删除的orderitem添加到新Order中）
1） 重写submit_line.html,以便添加按钮：
    重写工程目录下，templates/admin/submit_line.html， 添加如下：
    # 只在model：Order的管理界面中出现。
{% if opts.verbose_name == 'order' %}<input type="submit" value="{% trans 'Delete to new' %}" name="_delete2new" />{% endif %}  
2） 在orders/admin.py中，OrderAdmin(admin.ModelAdmin) 类中 重写change_view函数。
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['payer']
    list_display = ['id', 'payer', 'receiver', 'paid', 'delivered',
                    'track_result', 'created']
    readonly_fields = ('original',)
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline, PhotoInline]
    fields = (('payer', 'paid', 'original'), ('receiver', 'phone'), 'address', 'message',
              ('courier', 'delivered', 'delivered_date'),
              ('track', 'track_result'),
              ('total_price_rmb', 'total_expense_aud',
               'total_price_aud', 'total_expense_rmb'))
    def change_view(self, request, obj, form_url='',extra_context=None):
        if '_delete2new' in request.POST:
            res = split_save(request, obj)
            if res['status'] == 'success':
                messages.success(request, res['msg'])
                return HttpResponseRedirect(request.path)
            else:
                messages.error(request, res['msg'])
                return HttpResponseRedirect(request.path)
        else:
            return super().change_view(request, obj, form_url, extra_context)
admin.site.register(Order, OrderAdmin)
--------------------------------------------------------------------------------

o.16 如果重写admin的模板，不生效， 那么一定要检查INSTALLED_APPS 中app的顺序。自己的app 放在admin之前，才能是改写生效！！！
--------------------------------------------------------------------------------

o.17 Django 数据库重置：
  1） 不要数据了：a. 删除数据库中的所有的表； b. 删除所有app migrations目录下除了__init__.py以外的所有文件；c. 执行：
    python manage.py makemigrations 和 python manage.py migrate

  2)  保留数据库中的数据。
  a. 首先要保证,目前的migration文件和数据库是同步的，通过执行
# python manage.py makemigrations 
     如果看到 这样的提示: No changes detected，则可以继续接下来的步骤.
  b. 通过执行：
# python manage.py showmigrations 
     结果，可以看到当前项目，所有的app及对应的已经生效的migration文件如：
 shop
 [X] 0001_initial
 [x] 0002_add_model
  c. Clear the migration history:
$ python manage.py migrate --fake <app> zero
  d. 之后再执行 python manage.pu showmigrations，你会发现 文件前的 [x] 变成了[]
  e. 删除app下的migrations模块中 除 __init__.py 之外的所有文件。
  f. $ python manage.py makemigrations
  g. $ python manage.py migrate –fake-inital
–fake-inital 会在数据库中的 migrations表中记录当前这个app 执行到 0001_initial.py ，但是它不会真的执行该文件中的 代码。 
这样就做到了，既不对现有的数据库改动，而又可以重置 migraion 文件，妈妈再也不用在 migration模块中看到一推文件了。

  3)删除了migrations 做修复。
  a. Empty the django_migrations table:
> delete from django_migrations;
  b. For every app, delete everything except __init__.py in app migrations folder;
  c. Reset the migrations for the "built-in" apps: 
# python manage.py migrate --fake
  d. For each app run: 
# python manage.py makemigrations <app>. 
    Take care of dependencies (models with ForeignKey's should run after their parent model).
  e. Finally: python manage.py migrate --fake-initial
    After that I ran the last command without the --fake-initial flag, just to make sure.
    Now everything works and I can use the migrations system normally.
auth app @ /root/env3/lib/python3.6/site-packages/django/contrib/auth/migrations
注意：注意App 之间的相互依赖关系。
--------------------------------------------------------------------------------
o.18 AWS 部署注意问题
    1. orders/validate.py 中的字体位置
    2. media目录的权限，要$ chmod -R 775 media
    3. httpd的配置，要指定虚拟环境中的python
--------------------------------------------------------------------------------
o.19 CSS禁止页面选择：
    添加：
-moz-user-select: none; 
-webkit-user-select: none; 
-ms-user-select: none; 
-khtml-user-select: none; 
user-select: none; 
--------------------------------------------------------------------------------

o.20 禁止页面右键：
通过设置body属性来禁用复制功能代码如下：
<body oncontextmenu="return false" onselectstart="return false"
ondragstart="return false" oncopy="return false"
oncut="return false;></body>
--------------------------------------------------------------------------------














