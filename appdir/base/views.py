import requests
from flask import render_template, redirect, request, url_for, jsonify, session
from sqlalchemy import desc, or_
from flask_babel import gettext as _
from werkzeug.security import generate_password_hash, check_password_hash
from appdir import babel
from appdir.base.forms import *
from appdir import app
from appdir.base import base
import re


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['zh', 'en'])


# this is used to test how base showing (mainly for navbar at the top of the website)
@base.route('/base')
def base_html():
    if request.method == 'GET':
        return render_template("base.html")


@base.route('/test')
def test():
    if request.method == 'GET':
        return render_template("new_component.html")


@base.route('/')
def none():
    if request.method == 'GET':
        redirect_to_home = url_for(('sanhe.homepage'))
        return redirect(redirect_to_home)


from flask import send_from_directory


@base.route('/robots.txt')
def robots():
    return send_from_directory(app.root_path, 'robots.txt')


@base.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.root_path, 'sitemap.xml')


@base.route('/en/sitemap.xml')
def sitemap_en():
    return send_from_directory(app.root_path, 'static/sitemap.xml')


@base.route('/api/get_user', methods=['POST'])
# the page for welcome!
def get_user():
    # print(session.get("USERNAME"))
    # check the state of user, whether a new user or logged in user
    username = session.get("USERNAME")
    role = session.get("TYPE")
    if username is not None:
        return jsonify({'name': username, 'type': role})
    return jsonify({'name': "Tourist", 'type': "Tourist"})

# 后端构造一个API
@base.route('/traffic', methods=['POST'])
# @base.route('/traffic')
def traffic():
    # http://ipa-020.ucd.ie/metrics
    flow_data = requests.get('http://0.0.0.0:10000/metrics').text # 用request访问/metrics路由，得到流量数据
    results = []
    # 用for循环对获得的数据进行处理
    for line in flow_data.splitlines():
        # 编译一个正则表达式pattern
        pattern = re.compile(u'flask_http_request_duration_seconds_count{method="GET",path="(.*)')
        # 匹配
        match_result = pattern.search(line)
        if match_result is not None:
            # print(match_result.group())
            count_result = match_result.group()
            result = re.match('flask_http_request_duration_seconds_count{method="GET",path="(.*),status="200"(.*)',
                              count_result)
            if result is not None:
            # 匹配后先筛选出statue=200的，放在results里
                results.append(result.group())
    # print(results)
    total = 0.0
    page_results = []
    for result in results:
        site_info_list = result.split(" ")
        # print(site_info_list)
        site_url = site_info_list[0]
        if '/log_result' in site_url or '/profile' in site_url or '/staff' in site_url or '-' in site_url or '/chat' in site_url:
            continue
        route = site_info_list[0].replace('"', "").replace("flask_http_request_duration_seconds_count{method=GET,path=",
                                                           "").replace(",status=200}", "")
        # print(route)
        # 提取path的‘/blog/index’
        count = site_info_list[1] # 取到该路由的访问次数count
        # 处理成json格式
        total = total + float(count)
        each_page = {"page": route, "count": count}
        page_results.append(each_page)
    return jsonify({'total': total, "all_pages": page_results})
