****************************�̵꽨��***Django******Python3***********Virtual Environment**********************

1. <<<<<<<<<<<<<<<<*************��װpython3��pip3*************>>>>>>>>>>>>>>>>>>>

wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz

tar -xvzf Python-3.6.2.tgz

cd Python-3.6.2

./configure --enable-shared --enable-optimizations --with-threads --prefix=/usr/local/python3

make

make install

ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3   #���ӵ�python3

export LD_LIBRARY_PATH=/usr/local/python3/lib  #���Խ����libpython3.6m.so.1.0�Ҳ���������

��װpip3��

wget --no-check-certificate https://github.com/pypa/pip/archive/9.0.1.tar.gz

tar -zvxf 9.0.1 -C pip-9.0.1

cd pip-9.0.1

python3 setup.py install

ln -s /usr/local/python3/bin/pip /usr/bin/pip3

pip install --upgrade pip   #����pip

�ڶ��ַ�������IUS��װ��(����)

yum -y install https://centos7.iuscommunity.org/ius-release.rpm

yum install python36u

yum install python36u-devel

ln -s /usr/bin/python3.6 /usr/bin/python3    (#�õ��������� symbolic link  �൱��windows�Ŀ�ݷ�ʽ�� )

(#ȥ��-s ����Ӳ�����ˣ�hard linkֱ��ָ���ļ��ڵ㡣)

��װpip3

yum install python36u-pip

----------------------------------------------------------------------

2. ����virtualenv using python3

virtualenv env3 -p /usr/bin/python3.6    #pip3 ���Զ���װ�õ�

pip install pillow

pip install django

pip install requests

pip install mysqlclient

pip install python-slugify

pip install selenium

pip install pyquery

pip install mod_wsgi

----------------------------------------------------------------------

3. ��װMariaDB

yum install mariadb mariadb-server

systemctl start mariadb

systemctl enable mariadb

yum install httpd

yum install httpd-devel gcc

--------------------------------------------------------------------

4. ����database��user��password��

create database ozfriend default charset=utf8;

grant all on ozfriend.* to ozfriend@'localhost' identified by 'ozfriend'; '%'��ʾ������ַ���������ʡ�

flush privileges;

--------------------------------------------------------------------

5. ����django���̣�������settings

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
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #���ƹ���ģ���λ��
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',  #ÿ�εݽ������µ�processor
            ],
        },
    },
]

TIME_ZONE = 'Australia/Sydney'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
CART_SESSION_ID = 'cart'  #ÿ�������û�������һ����cart����
---------------------------------------------------------------------------------

6. ���python3��MariaDB/MySQL��Django֮��ͨ��
����Ŀ�ļ��£�settings ͬĿ¼����__init__.py����ӣ�
import pymysql
pymysql.install_as_MySQLdb()

����������Django�����Ƽ���
yum install mariadb-devel ����mysql-devel���Զ�����mariadb-devel��
pip install mysqlclient
-------------------------------------------------------------------------------

7. python�µ�slug ��
pip install python-slugify
from slugify import slugify
ʹ�÷�����
txt = "This is a test ---"
r = slugify(txt)   #  'this-is-a-test'
-------------------------------------------------------------------------

8.0  ɾ���Լ���appĿ¼��migrationĿ¼�µĳ���__init__.py����������ļ�
    #׼����Ӧ�ı�
    python manage.py makemigrations
    python manage.py migrate
    #����֮ǰ������
    python manage.py loaddata data-backup-16SEP-ourdata-all.json
---------------------------------------------------------------------------
8. ������������Django1.11.4+Apache2.4+CentOS7+MariaDB

8.1 ��װApache, MariaDB(��3)

8.2 ��װmod_wsgi��***************
    cd env3/
    source bin/active
    pip install mod_wsgi
    (��Ҫ��yum install httpd-devel gcc)

8.3 ����mod_wsgi:
    mod_wsgi-express module-config > /etc/httpd/conf.modules.d/00-wsgi.conf
    ���ɵ�����Ϊ��
    LoadModule wsgi_module "/root/env3/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
    WSGIPythonHome "/root/env3"
    Ҫ��Ŀ¼/etc/http/conf.modules.d/* �� /etc/http/conf.d/* ���ļ�/etc/http/conf/httpd.conf �У�
    ����LoadModule wsgi_module������У�Ҫ��#���ε���
    systemctl restart httpd

8.4 ����Apache���:(��Apache������м�ض˿ڣ�ָ��static��mediaĿ¼��WSGI���̣�ָ�����⻷���е�python)
Listen 8001
<VirtualHost 0.0.0.0:8001>
    Alias /static /root/env3/ozfriend/static
    <Directory /root/env3/ozfriend/static>
        Options Indexes MultiViews FollowSymLinks  #ʵ��������������Ӧ�ø������Ȩ��
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

8.5 ��װ��������
    pip install pillow
    pip install django
    pip install mysqlclient

8.6 ���ԣ�
    cd /root/env3/ozfriend
    source ../bin/active
    python manage.py collectstatic  #�ռ���̬�ļ�
    python manage runserver 0:8080
    ��ҳ�������ʣ�˵��django���������û���⡣ 

8.7 Ȩ������ (û�н��д������ã�Ĭ�ϵ�������ִ��Ȩ��)
    usermod -a -G �û� apache   # ��apache���뵽���û���ͬ�顣
    chmod 710 /home/�û�   #������СȨ��
    #�������
    groups �鿴��ǰ�û�����
    groups apache �鿴apache������
    cat /etc/group �鿴������

8.8 �����������ԣ�
    ����8001�˿�������˵����������������ϡ�

8.9 ���ݿ⵼�뼰����(δ�����������)
----------------------------------------------------------------------

O.1:����������django�е�id������
python manage.py dbshell
mysql> ALTER TABLE <table_name> AUTO_INCREMENT = 1;
---------------------------------------------------------------------------

O.2: ����վץȡ���ݣ�����product��
import os
import django
import datetime
import random
import re
import slugify
from selenium import webdriver
from pyquery import PyQuery as pq
#��������
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

#��Excel�ļ��ж���ausomg����ַ�б�
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
O.3 admin������ȶ��ƣ�
    ozfriend/settings������admin templates. (��5)
    ��change_form.html���Ƶ�ozfriend/templates/orders/admin/�У������js��������ļ�
    �Լ�д��js�ļ�������ʵ�֣�Order������������ͬ����orders/static/orders/js/pagesync.js
/* Written by Xiaoming Zheng on 30AUG for my Lover */
(function($) {
    $("tbody").change(function(){
        var aud=0;
        var rmb=0;
        $("tbody tr.has_original").each(function(index,e){
            rmb+=$(this).children(".field-price").children("input").val()*$(this).children(".field-quantity").children("input").val();  /*��ȡ������*/
            aud+=$(this).children(".field-expense").children("input").val()*$(this).children(".field-quantity").children("input").val();
        });
        $("#id_total_price").val(rmb.toFixed(2));
        $("#id_total_expense").val(aud.toFixed(2));
        });
})(django.jQuery);
    change_form.html�޸����ݣ�(ע�⣬��ʽ�������õ���ͨjquery���ã�Ϊ�����ռ䴿����)
{% block admin_change_form_document_ready %}
   <script type="text/javascript"
            id="django-admin-form-add-constants"
            src="{% static 'admin/js/change_form.js' %}"
            {% if adminform and add %}
                data-model-name="{{ opts.model_name }}"
            {% endif %}>
    </script>
    <script type="text/javascript" src="{% static 'js/pagesync.js' %}">  ����Ϊ�������
    </script>
{% endblock %}
------------------------------------------------------------------------------

o.4 admin�޸����⣺
    ozfriend/urls.py����ӣ�
    admin.site.site_header = "OZFriend Management System"
    admin.site.site_title = "OZFriendAdmin"
-----------------------------------------------------------------------------------

o.5 admin�м����Լ���ҳ�棺
    #<<<admin��ҳ������Լ�����ҳ���ӣ����ɺ�ԭ��һ����>>>
    #����ģ�壺reports/templates/reports/ozfriend_report_list.html 
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
    #����index.htmlģ�嵽:ozfreind/templates/admin/index.html ����
    {% block content %}
    <div id="content-main">????</div>
    {% endblock %}�е���󲿷���ӣ�
{% block ozfriendreport %}
{% include "reports/ozfriend_report_list.html" %}
{% endblock %}
    #<<<��֤�������򲻻��ܵ�Ӱ�죬��Ҫ�����޸ģ���ʹǰ��ոռ���Ĵ��벻Ӱ��ԭ�еĳ���>>>
    #����app_index.html��ozfriend/templates/admin/app_index.html
    #��{% block sidebar %}{% endblock %}֮ǰ��ӣ�{% block ozfriendreport%}{% endblock %}
   --------------------------------------
	

    #�����Լ�����ĳ����������Ӻ�ҳ��
    python manage.py startapp reports
    #ozfriend/urls.py��������µ�url��
    url(r'^admin/reports/', include('reports.urls', namespace='reports')),
    #reports/urls.py������:
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.report_list, name='report_list'),
    url(r'^annual$', views.annual_report, name='annual_report'),
    url(r'^monthly$', views.monthly_report, name='monthly_report'),
    url(r'^payer$', views.payer_report, name='payer_report'),
]
    #�³����б�ҳ��ģ�壺
    #������admin/app_index.html���adminģ��
    #ozfrend/reports/templates/reports/report_index.html���ݣ�
{% extends "admin/app_index.html" %}
{% block content %}
    {% include "reports/ozfriend_report_list.html" %}
    {% block ozfriendreport %}{{ block.super }}{% endblock %}
{% endblock %}
{% block sidebar %}
{% if marry_count %}<h1 color="#417690;">{{ marry_count }}</h1>{% endif %}
{% endblock %}
    #ͳ�Ʊ���ʹ�õ�ģ�壨���֣���(Ϊ��ʹ��ʱ��ѡ��Ŀؼ�)
    #������admin/app_index.html���adminģ�壬������д��{% block extrastyle %}��������ԭ�е�dashboard.css��Ӱ�졣
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

    #���������admin ����ʹ��ʱ�䣬���ڿؼ��� ��Ҫ��ģ�����ӣ�
<script type="text/javascript">window.__admin_media_prefix__ = "{% filterescapejs %}{% static 'admin/' %}{% endfilter %}";</script>
    #������ozfriend/urls.py����ӣ�
 def i18n_javascript(request): return admin.site.i18n_javascript(request) patterns = [ ... url(r'^admin/jsi18n', i18n_javascript),  #������admin ֮ǰ��
------------------------------------------------------------------------------

O.6 ��ҳ����Ҫ����ԱȨ�޲��ܷ��ʣ�
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
------------------------------------------------------------------------------

O.7 ��ҳ�治��memcaceh����Ӱ�죺
from django.views.decorators.cache import never_cache  # use @never_cache
Ŀǰ���ԣ����ǲ����á�����Ҳû�г��ֻ��塣ȡ��ǰʱ�䣬Ҫ�ں���/������ȡ���������Ӱ�졣
------------------------------------------------------------------------------
O.8 �������ǽ��� ���꼸�¼���ĳ��� ���Ǿ����������Y-Y��M-M�� D-D������ʱ��ǰ��һλ�衣
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

O.9 Django ���ݿⱸ�ݣ�
    python manage.py dumpdata > db.json  #��������
    python manage.py dumpdata admin > db.json  #����admin ���app
    python manage.py dumpdata admin.logentry > db.json  #����admin ���app��logentry�����
--------------------------------------------------------------------------------------

o.10 Django ����Լ���filter
    �ڳ����д���templatetagsĿ¼
    ��templatetags��touch __init__.py  #������python�����module���������롣
    ����ozfrend_tags.py #��������Լ���filter�����������������£�
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
    return "-��%.2f"%(-1*value) if value < 0 else "��%.2f"%value
---------------------------------------------------------------------------

o.11 ��дmodel�е�save������ʵ��model�����Ե�default value�趨Ϊ����������ԡ�

------------------------------------------------------------------------

o.12  Django Ajax POST ���csrftoken����
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
//��������ݿ�������$.post(url,data,function(res){})��data�ֵ������ 'csrfmiddlewaretoken':csrftoken ��ȡ����
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

o.13 ���Mac OS�µĸ�����������@
    ls -al   #�鿴��������
    xattr -l  �ļ���   # �鿴��ϸ��������
    xattr -c  �ļ���   # ����ɾ����������

-------------------------------------------------------------------------------------------

o.14 ������֤��
#!/usr/bin/env python3
import random, base64, io
from PIL import Image,ImageFont,ImageDraw
from django.conf import settings


def get_validate_img(req):
    def rndtxtcolor2():  # ������ɫ
        return (random.randint(32,127),random.randint(32,127),random.randint(32,127))
    def rndbgcolor():  # ������ɫ
        return (random.randint(64,255),random.randint(64,255),random.randint(64,255))
    def rndtxt():
        txt_list = []
        #txt_list.extend([i for i in range(65,90)])  # ��д��ĸ
        #txt_list.extend([i for i in range(97,123)])  # Сд��ĸ
        #txt_list.extend([i for i in range(50,57)])  # ����
        txt_list.extend([i for i in range(33,123)])  # ALL
        return chr(txt_list[random.randint(0,len(txt_list)-1)])

    weight = 250
    hight = 60
    image = Image.new('RGB',(weight,hight),(255,255,255))
    font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans.ttf',36) #CentOS7 ע�������ļ���λ�á�
    #font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationSans-Regular.ttf',36) # RHEL ϵͳ
    draw = ImageDraw.Draw(image)
    for x in range(weight):  # ��䱳����ɫ
        for y in range(hight):
            draw.point((x,y),fill=rndbgcolor())
    verify = ""
    for t in range(6):  # ���������֤��
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
#��orders/views.py�����һ��view��
def order_validate_img(req):
    image = get_validate_img(req)
    res = HttpResponse(content_type='image/png')
    image.save(res, 'png')
    return res
#��Ӧ��url����Ӵ�view�ĵ�ַ:
url(r'^validate/$', views.order_validate_img, name='order_validate_img'),
#��Ӧ��ģ�������ô���ַ{% url "orders:order_validate_img" %}
-------------------------------------------------------------------------------------------------
o.12 ������������<<<<��django project Ŀ¼����ĵط�����ʼ��django����������django�Ĺ���>>>>������������������
����һ��
import os,sys,django
sys.path.append('/root/env3/ozfriend')  #������Ŀ¼���뻷������
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ozfriend.settings")
os.chdir('/root/env3/ozfriend')
django.setup()
��������(��ʵ��һ�ַ���)
def __setup_django(project_path, settings):
    import os,sys,django
    os.chdir(project_path)
    sys.path.append(project_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ozfriend.settings")
    #above=os.environ['DJANGO_SETTINGS_MODULE'] = settings
    django.setup()
__setup_django('/root/env3/ozfriend','ozfriend.settings')


-------------------------------------------------------------------------------------------------


o.13 ͼ��ʶ����뻷��׼����
pip install pillow
pip install pytesseract   (or tesserocr)

yum install leptonica-devel, tesseract-devel
#�ο�����https://pypi.python.org/pypi/tesserocr

import pytesseract
from PIL import Image
image = Image.open('vcode.png')
vcode = pytesseract.image_to_string(image)
print (vcode)
#����ֻ��ʶ�𱳾������ӵ�ͼƬ�������ã�û�������

---------------------------------------------------------------------------------------------

o.14 �Լ�д��ͼ��ʶ��----����hamming����

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
#ͼƬx���ͶӰ����������ݣ���ɫ���ص㣩ֵΪ1����Ϊ0
def get_projection_x(image):
    p_x = [0 for x in range(image.size[0])]
    for w in range(image.size[1]):
        for h in range(image.size[0]):
            if image.getpixel((h,w)) == 0:
                p_x[h] = 1
    return p_x

#ͼƬy���ͶӰ����������ݣ���ɫ���ص㣩ֵΪ1����Ϊ0
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
#Ԥ��ͼ����ȡ�߿��λ�ã�Ϊ�ڶ��ξ�ȷ��ͼ��ȡ������׼��
im = image.crop(box=(L,T,R,B))
bl=im.convert('L') # ת�Ҷ�ͼ
bi = bl.point(initTable(140,0), '1') #ת��ֵͼ
bix=get_projection_x(bi)
biy=get_projection_y(bi)
bixr=get_split_seq(bix, True)  # ����ͼƬ������һ���ʱ����10�����طָ�
biyr=get_split_seq(biy)

LL=L+bixr[0][0]+2
TT=T+biyr[0][0]+2
RR=LL+bixr[0][1]-4
BB=TT+biyr[0][1]-4
im = image.crop(box=(LL,TT,RR,BB))
bl=im.convert('L') # ת�Ҷ�ͼ
bi = bl.point(initTable(140,1), '1') #ת��ֵͼ
bix=get_projection_x(bi)
biy=get_projection_y(bi)
bixr=get_split_seq(bix, True)  # ����ͼƬ������һ���ʱ����10�����طָ�
biyr=get_split_seq(biy)
im_got=get_images(bi, bixr[:3], biyr[0])
#׼������,����������0����255�� Ҫformalize ��0��1
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

#����ͼƬ�ȶԣ�������űȶ�

inp=phantomjs.find_element_by_css_selector('#yzm')
inp.send_keys(eval(validate[:3]))
button=phantomjs.find_element_by_css_selector('#wrapper > div.right > input[type="submit"]')
button.click()
status=phantomjs.find_element_by_css_selector('#fet > tbody > tr:last-child').text

-------------------------------------------------------------------------------
0.15 Django Admin changeҳ����Ӱ�ť��ִ���Զ����������Ҫɾ����orderitem��ӵ���Order�У�
1�� ��дsubmit_line.html,�Ա���Ӱ�ť��
    ��д����Ŀ¼�£�templates/admin/submit_line.html�� ������£�
    # ֻ��model��Order�Ĺ�������г��֡�
{% if opts.verbose_name == 'order' %}<input type="submit" value="{% trans 'Delete to new' %}" name="_delete2new" />{% endif %}  
2�� ��orders/admin.py�У�OrderAdmin(admin.ModelAdmin) ���� ��дchange_view������
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

o.16 �����дadmin��ģ�壬����Ч�� ��ôһ��Ҫ���INSTALLED_APPS ��app��˳���Լ���app ����admin֮ǰ�������Ǹ�д��Ч������
--------------------------------------------------------------------------------

o.17 Django ���ݿ����ã�
  1�� ��Ҫ�����ˣ�a. ɾ�����ݿ��е����еı� b. ɾ������app migrationsĿ¼�³���__init__.py����������ļ���c. ִ�У�
    python manage.py makemigrations �� python manage.py migrate

  2)  �������ݿ��е����ݡ�
  a. ����Ҫ��֤,Ŀǰ��migration�ļ������ݿ���ͬ���ģ�ͨ��ִ��
# python manage.py makemigrations 
     ������� ��������ʾ: No changes detected������Լ����������Ĳ���.
  b. ͨ��ִ�У�
# python manage.py showmigrations 
     ��������Կ�����ǰ��Ŀ�����е�app����Ӧ���Ѿ���Ч��migration�ļ��磺
 shop
 [X] 0001_initial
 [x] 0002_add_model
  c. Clear the migration history:
$ python manage.py migrate --fake <app> zero
  d. ֮����ִ�� python manage.pu showmigrations����ᷢ�� �ļ�ǰ�� [x] �����[]
  e. ɾ��app�µ�migrationsģ���� �� __init__.py ֮��������ļ���
  f. $ python manage.py makemigrations
  g. $ python manage.py migrate �Cfake-inital
�Cfake-inital �������ݿ��е� migrations���м�¼��ǰ���app ִ�е� 0001_initial.py ���������������ִ�и��ļ��е� ���롣 
�����������ˣ��Ȳ������е����ݿ�Ķ������ֿ������� migraion �ļ���������Ҳ������ migrationģ���п���һ���ļ��ˡ�

  3)ɾ����migrations ���޸���
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
ע�⣺ע��App ֮����໥������ϵ��
--------------------------------------------------------------------------------
o.18 AWS ����ע������
    1. orders/validate.py �е�����λ��
    2. mediaĿ¼��Ȩ�ޣ�Ҫ$ chmod -R 775 media
    3. httpd�����ã�Ҫָ�����⻷���е�python
--------------------------------------------------------------------------------
o.19 CSS��ֹҳ��ѡ��
    ��ӣ�
-moz-user-select: none; 
-webkit-user-select: none; 
-ms-user-select: none; 
-khtml-user-select: none; 
user-select: none; 
--------------------------------------------------------------------------------

o.20 ��ֹҳ���Ҽ���
ͨ������body���������ø��ƹ��ܴ������£�
<body oncontextmenu="return false" onselectstart="return false"
ondragstart="return false" oncopy="return false"
oncut="return false;></body>
--------------------------------------------------------------------------------














