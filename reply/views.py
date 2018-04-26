from django.shortcuts import render, HttpResponse, redirect
from django import forms
from .models import Reply
from blocks.models import Block
from posts.models import Post
from users.models import User
from message.views import new_message
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from users.views import login_required

# Create your views here.

@csrf_exempt
def create_reply(request):
    # reply_obj = json.loads(params)
    # reply_obj = request.POST['params']
    post_id = int(request.POST.get('post_id'))
    content = request.POST.get('content')
    to_comment_id = int(request.POST.get("to_comment_id", 0))
    email = request.session.get('email')

    post = Post.objects.get(id=post_id)
    user = User.objects.get(email=email)
    if to_comment_id != 0:
        to_comment = Reply.objects.get(id=to_comment_id)
    else:
        to_comment = None

    if content != '':
        reply = Reply(content=content)
        reply.post = post
        reply.author = user
        reply.author_name = user.nickname
        reply.status = 1
        reply.to_reply = to_comment
        reply.save()

        new_message(post.block_id, post_id, content, user.nickname)

        # msg_num = int(request.session.get('msg_num')) + 1
        # request.session['msg_num'] = msg_num

        status = 'ok'
        error = ''

    else:
        status = 'fail'
        error = 'Please input content.'

    reply_obj = {
        'status': status, 'error': error
    }
    # print (reply_obj)
    # return json.dumps(reply_obj)
    # return request, reply_obj
    return HttpResponse(json.dumps(reply_obj), content_type='application/json')


def reply_detail(post_id):
    post_id = int(post_id)
    reply_objs = Reply.objects.filter(post=post_id).order_by('update_timestamp')
    return reply_objs