from django.shortcuts import render, redirect, HttpResponse
from .models import Message
from posts.models import Post
from users.models import User
from django.core.paginator import Paginator
from datetime import datetime
import json


# Create your views here.

POST_CNT_1PAGE = 10


def paginate_queryset(objs, page_no, cnt_per_page=10, half_show_length=5):
    p = Paginator(objs, cnt_per_page)
    page_cnt = p.num_pages
    if page_no > p.num_pages:
        page_no = p.num_pages
    if page_no <= 0:
        page_no = 1
    page_links = [i for i in range(page_no - half_show_length, page_no + half_show_length + 1)
                  if i > 0 and i <= p.num_pages]
    page = p.page(page_no)
    pagination_data = {
        "page": page, "page_no": page_no, "page_links": page_links, "page_cnt": page_cnt
    }
    return (page.object_list, pagination_data)


def new_message(block_id, post_id, content, replier):
    link = "/posts/list/" + str(block_id) + "/post" + str(post_id)

    post = Post.objects.get(id=post_id)
    user_id = post.author.id
    user = User.objects.get(id=user_id)

    message = Message(user=user, content=content, link=link, status=1, post_title=post.title, replier=replier,
                      create_date=(datetime.today()).strftime("%Y-%m-%d"))
    message.save()

    return None


def show_message(request):
    email = request.session.get('email')
    # nickname = request.session.get('nickname')
    # verified = request.session.get('verified')
    # msg_num = request.session.get('msg_num')

    user = User.objects.get(email=email)

    message_objs = Message.objects.filter(user=user.id).order_by("-id")

    page_no = int(request.GET.get("page_no", "1"))
    message_objs, pagination_data = paginate_queryset(message_objs, page_no, POST_CNT_1PAGE)

    return render(request, "message.html", {"messages":message_objs,
                                            "pagination_data": pagination_data,
                                            "session": request.session
                                # "email": email, "nickname":nickname, "verified":verified, "msg_num":msg_num,
                                })


def read_message(request, msg_id):

    # msg_id = int(msg_id)
    message = Message.objects.get(id=msg_id)
    # if message.status == 1:
        # msg_num = int(request.session.get('msg_num')) - 1
        # request.session['msg_num'] = msg_num

    Message.objects.filter(id=msg_id).update(status=0)

    return redirect(message.link)


def message_number(request):
    email = request.session.get('email')
    user = User.objects.get(email=email)
    message_objs = Message.objects.filter(user=user.id, status=1)

    msg_number = str(len(message_objs))
    status = 'ok'
    msg_obj = {
        'msg_number': msg_number, 'status': status
    }
    # print(msg_number)

    # return msg_number
    return HttpResponse(json.dumps(msg_obj), content_type='application/json')