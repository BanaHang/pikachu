from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from index import views
import pymysql
import time
# Create your views here.


CURRENT_PAGE = 1     # 页码初始值
SIZE = 10        # 帖子页长默认值
FOLLOW_SIZE = 18    # 评论页长默认值


def plate_html(request):
    meta_data = get_all_plate()

    data = meta_data[0: SIZE]

    global CURRENT_PAGE

    if 'page' in request.GET:
        result = views.Page_Divider(request.GET['page'], meta_data, SIZE, CURRENT_PAGE)
        data = result['data']
        CURRENT_PAGE = result['page']

    if 'title' in request.GET:
        if request.GET['title'] != ' ' and request.GET['nickname'] != ' ' and request.GET['content'] != ' ':
            title = str(request.GET['title'])
            writer = str(request.GET['nickname'])
            content = str(request.GET['content'])
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            add_new_comment(title, writer, content, datetime)
            return redirect('http://www.ipikachu.cn/plate/')
        else:
            return HttpResponse("<script>alert('请不要输入单个空格！')</script>")

    return render(request, "plate.html", {'data': data, 'current_page': CURRENT_PAGE, })


def content_html(request):
    meta_data = list()
    info = list()

    if 'plateid' in request.GET:
        pid = request.GET["plateid"]
        info = list(get_plate_info(pid))
        meta_data = list(get_all_follows(pid))

    follows = meta_data[0:FOLLOW_SIZE]
    global CURRENT_PAGE

    if 'page' in request.GET:
        result = views.Page_Divider(request.GET['page'], meta_data, FOLLOW_SIZE, CURRENT_PAGE)
        follows = result['data']
        CURRENT_PAGE = result['page']

    if "nickname" in request.GET:
        if request.GET['nickname'] != ' ' and request.GET['content'] != ' ':
            pid = str(request.GET['plateid'])
            nama = str(request.GET['nickname'])
            content = str(request.GET['content'])
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            add_new_follow(pid, nama, content, datetime)
            return redirect('http://www.ipikachu.cn/content/?plateid=' + pid)
        else:
            return HttpResponse("<script>alert('请不要输入单个空格！')</script>")
    return render(request, "content.html", {'content': info, 'data': follows, 'current_page': CURRENT_PAGE, })


# 获取所有帖子数据（需改进，必须考虑到将来数据变多了以后，全部数据查取性能极低、资源浪费）
def get_all_plate():
    db = pymysql.connect(host="106.15.186.200", user="bana", password="banahang", database="pikachu")
    cmd = db.cursor()
    sql = "select * from platetest order by WEIGHT desc, PID desc limit 180"
    cmd.execute(sql)
    plates = list()
    plates[:] = cmd.fetchall()[:]
    db.close()
    return plates


# 增加新帖子
def add_new_comment(title, writer, content, datetime):
    sql = "insert into platetest (TITLE, CONTENT, DATETIME, WRITER, WEIGHT) values ('" + title + "', '" + content + "', '" + datetime + "', '" + writer + "', 0)"
    db = pymysql.connect(host="106.15.186.200", user="bana", password="banahang", database="pikachu")
    cmd = db.cursor()
    cmd.execute(sql)
    db.commit()
    db.close()


# 获取帖子的相关信息，在内容页中展示
def get_plate_info(pid):
    db = pymysql.connect(host="106.15.186.200", user="bana", password="banahang", database="pikachu")
    cmd = db.cursor()
    sql = "select * from platetest where PID = " + str(pid)
    cmd.execute(sql)
    info = cmd.fetchone()
    db.close()
    return info


# 获取所有评论（需改进，要考虑到万一一条帖子评论很多怎么办）
def get_all_follows(pid):
    db = pymysql.connect(host="106.15.186.200", user="bana", password="banahang", database="pikachu")
    cmd = db.cursor()
    sql = "select * from followtest where PID = " + str(pid)
    cmd.execute(sql)
    follow = list()
    follow[:] = cmd.fetchall()[:]
    db.close()
    return follow


# 增加新评论
def add_new_follow(pid, name, content, datetime):
    sql = "insert into followtest (PID, CONTENT, DATETIME, WRITER) values (" + pid + ", '" + content + "', '" + datetime + "', '" + name + "')"
    db = pymysql.connect(host="106.15.186.200", user="bana", password="banahang", database="pikachu")
    cmd = db.cursor()
    cmd.execute(sql)
    db.commit()
    db.close()
