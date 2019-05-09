from django.shortcuts import render
from django.shortcuts import HttpResponse
import pymysql
import math
# Create your views here.


def index_html(request):
    return render(request, "index.html", )


def about_html(request):
    return render(request, "about.html", )


def game_html(request):
    return render(request, "game.html", )


def error_page(request):
    return render(request, "404.html")


CURRENT_PAGE = 1     # 页码初始值
SIZE = 10        # 页长默认值


def projects_html(request):
    master_data = get_all_project_data()
    data = master_data[0: SIZE]

    if 'key' in request.GET:
        keyword = str(request.GET['key'])
        data.clear()
        if keyword == "":
            data = master_data[0: SIZE]
        else:
            for i in master_data:
                if keyword in i[1]:
                    data.append(i)

    global CURRENT_PAGE

    if 'page' in request.GET:
        result = Page_Divider(request.GET['page'], master_data, SIZE, CURRENT_PAGE)
        data = result['data']
        CURRENT_PAGE = result['page']

    return render(request, "projects.html", {'data': data, 'current_page': CURRENT_PAGE, })


# 实现搜索提示、自动补全
def auto_select_complete(request):
    master_data = get_all_project_data()
    temp = list()
    result = ""
    if 'word' in request.GET:
        word = str(request.GET['word'])
        for i in master_data:
            if word in i[1]:
                temp.append(i[1])
    if len(temp) > 0:
        for t in temp:
            result = result + str(t) + ";"
    return HttpResponse(result)


# 获取所有项目数据信息
def get_all_project_data():
    master_data = list()

    db = pymysql.connect(host="106.15.186.200", user="bana", password="banahang", database="pikachu")
    curse = db.cursor()
    # curse.execute("select * from project")
    curse.execute("select * from projecttest")
    master_data[:] = curse.fetchall()[:]
    db.close()
    return master_data


# 翻页器，实现分页功能。page_action为传入动作参数，meta_data为源数据，step为页大小，current为当前页码
def Page_Divider(page_action, meta_data, step, current_page):
    page_action = str(page_action)
    max_page = math.ceil(len(meta_data) / step)
    data = list()
    if page_action == "first":
        data = meta_data[0:step]
        current_page = 1
    elif page_action == "last":
        yu = len(meta_data) % step
        if yu == 0:
            data = meta_data[-step:]
        else:
            data = meta_data[-yu:]
        current_page = max_page
    elif page_action == "previous":
        if current_page > 1:
            current_page -= 1
            data = meta_data[step * (current_page - 1): step * current_page]
        else:
            data = meta_data[0:step]
    elif page_action == "next":
        if current_page < max_page:
            current_page += 1
            data = meta_data[step * (current_page - 1): step * current_page]
        else:
            yu = len(meta_data) % step
            if yu == 0:
                data = meta_data[-step:]
            else:
                data = meta_data[-yu:]
            current_page = max_page
    else:
        page_action = int(page_action)
        current_page = page_action
        data = meta_data[step * (current_page - 1): step * current_page]

    result = {
        'data': data,
        'page': current_page,
    }
    return result
