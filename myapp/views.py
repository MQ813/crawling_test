from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from game import charactor
import random

# Create your views here.
topics = [
        {'id': 1, 'title': '설명', 'body': '설명...'},
        {'id': 2, 'title': '만든이', 'body': 'mq...'},
        {'id': 3, 'title': 'version', 'body': '0.1'},
    ]
char_db = {}

def get_tagger(tag):
    def inner(line, params={}):
        params_str = ''
        for key, val in params.items():
            params_str += f' {key}="{val}"'
        return f"<{tag}{params_str}>{line}</{tag}>"
    return inner

h1_tag = get_tagger('h1')
li_tag = get_tagger('li')
a_tag = get_tagger('a')



def html_template(contents=''):
    global li_tag, a_tag, topics
    ol = ''
    for topic in topics:
        ol += li_tag(a_tag(topic["title"], params={'href': f'/read/{topic["title"]}'}))
    template = f"""
        <html>
        <body>
            {h1_tag(a_tag("쌀먹검색기", params={'href': '/'}))}
            
            <form action="/" method="post">
                <input type="text" placeholder="캐릭터 이름" name="charactor_name" id="charactor_name">
                <input type="submit" value="검색">
                <br>
            </form>
            {contents}
            <ol>
                {ol}
            </ol>
        </body>
        </html>
        """
    return template

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def home(request):
    if request.method == 'GET':
        return HttpResponse(html_template("Welcome to LostSSAL!"))

    elif request.method == 'POST':
        return redirect(f'char_info/{request.POST["charactor_name"]}')


def create(request):
    return HttpResponse('Create!')

@csrf_exempt
def char_info(request, name=''):
    if not name:
        return HttpResponse(html_template(f"캐릭터명을 입력해 주세요."))
    char = charactor.Charactor(name)
    # char.get_data()
    if not char.level_item:
        return HttpResponse(html_template(f"{name} 캐릭터가 존재하지 않습니다."))

    reput_log = ''
    if request.method == 'POST':
        reput_log = char.add_reput(request.POST['reput'], ip=get_client_ip(request))
    char.get_reput()
    contents = f"""
                <form action="/char_info/{name}" method="post">
                    {str(char)} 
                    <input type="submit" name="reput" value="like"> 
                    <input type="submit" name="reput" value="hate">
                    <br>
                    {reput_log}
                </form>
    """
    return HttpResponse(html_template(contents))

def read(request, title):
    global topics
    for topic in topics:
        if topic['title'] == title:
            body = topic['body']
            break
    else:
        body = ''
    contents = h1_tag(title) + body
    return HttpResponse(html_template(contents))
