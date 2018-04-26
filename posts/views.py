from django.shortcuts import render, redirect
from django import forms
from .models import Post
from blocks.models import Block
from django.views.generic import View, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import User
from reply.views import reply_detail
from users.views import login_required2
from Helper.Mytools import MyHTMLParser
import os

# Create your views here.
POST_CNT_1PAGE = 10


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class PostCreateView(View):
    template_name = "new_post.html"

    def init_data(self, block_id):
        self.block_id = block_id
        self.block = Block.objects.get(id=block_id)

    def get(self, request, block_id):
        self.init_data(block_id)
        return render(request, self.template_name, {"b": self.block})

    def post(self, request, block_id):
        self.init_data(block_id)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Get title and content first and not save in database
            post.block = self.block
            post.status = 1
            # post = Post(block=block, title=form.cleaned_data["title"],
            #             content=form.cleaned_data["content"], status=1)
            post.save()
            return redirect("/posts/list/%s" % self.block_id)
        else:
            return render(request, self.template_name, {"b": self.block, "form": form})


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"


def posts_list(request, block_id):
    keyword = "6"
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    posts_objs = Post.objects.filter(block=block, status=1).order_by("-id")

    page_no = int(request.GET.get("page_no", "1"))
    # p = Paginator(posts_objs, POST_CNT_1PAGE)
    # page = p.page(page_no)
    posts_objs, pagination_data = paginate_queryset(posts_objs, page_no, POST_CNT_1PAGE)
    # page_links = [i for i in range(page_no-5, page_no+6) if i > 0 and i <= p.num_pages]

    # email = request.session.get('email')
    # verified = request.session.get('verified')
    # user = User.objects.get(email=email)
    # nickname = request.session.get('nickname')

    return render(request, "posts_list.html", {"posts": posts_objs, "b": block,
                                               "pagination_data": pagination_data,
                                               # "email": email, "nickname": nickname, "verified": verified
                                               "session": request.session, })


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


@login_required2
def new_post(request, block_id):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)

    # email = request.session.get('email')
    # nickname = request.session.get('nickname')
    verified = request.session.get('verified')

    if request.method == "GET":
        if not request.session.get('email'):
            error = "Please login first."
            return render(request, "login.html", {"error": error})
        if not verified:
            return redirect("/users/activate")
        return render(request, "new_post.html", {"b": block,
                                                 # "email": email, "nickname": nickname, "verified": verified
                                                 "session": request.session,
                                                 })
    else:

        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        form = PostForm(request.POST)
        picture_num = int(request.POST["picture_num"])
        # print(request.POST["picture_num"])
        url = ""
        # if picture_num > 0:
        #     for i in range(1,picture_num):
        #         name = 'Picture'+str(i);
        #         picture_file = request.FILES.get(name, None)
        #         if picture_file:
        #             file_path = os.path.join("/Users/jackylee/PycharmProjects/Helper/static/files/photos",picture_file.name)
        #             with open(file_path, 'wb+') as destination:
        #                 for chunk in picture_file.chunks():
        #                     destination.write(chunk)
        #             url += "http://res.stevenshelper.com/photos/%s|||" % picture_file.name
        # else:
        #     picture_file = request.FILES.get("Picture1", None)

        if form.is_valid():
            post = form.save(commit=False) # Get title and content first and not save in database
            post.block = block
            post.status = 1
            user = User.objects.get(email=request.session.get('email'))
            post.author = user
            my_parser = MyHTMLParser()
            my_parser.feed(post.content)
            my_parser.close()
            post.desc = my_parser.content
            if url != "":
                post.picture = url
            post.author_name = user.nickname
            # post = Post(block=block, title=form.cleaned_data["title"],
            #             content=form.cleaned_data["content"], status=1)
            post.save()
            return redirect("/posts/list/%s" % block_id)
        else:
            # print(content)
            return render(request, "new_post.html", {"b": block, "form": form,
                                                     # "email": email, "nickname": nickname, "verified": verified,
                                                     "session": request.session,
                                                     "content": content}
                          )

        # if not title or not content:
        #     return render(request, "new_post.html",
        #                   {"b": block, "error": "Please fill out title and content fields."},)
        # if len(title) > 100:
        #     return render(request, "new_post.html",
        #                   {"b": block, "error": "Title should be less than 100 chars.",
        #                    "title": title, "content": content}, )
        # if len(content) > 10000:
        #     return render(request, "new_post.html",
        #                   {"b": block, "error": "Content should be less than 10000 chars.",
        #                    "title": title, "content": content}, )
        # post = Post(block=block, title=title, content=content, status=1)
        # post.save()


def post_detail(request, block_id, post_id):
    block_id = int(block_id)
    post_id = int(post_id)
    block = Block.objects.get(id=block_id)
    post = Post.objects.get(id=post_id)

    # picture_data = pictures(post.picture)


    reply_objs = reply_detail(post_id)

    email = request.session.get('email')
    # nickname = request.session.get('nickname')
    # verified = request.session.get('verified')

    user = post.author
    if (user.email == email):
        can_update = True
    else:
        can_update = False

    page_no = int(request.GET.get("page_no", "1"))
    reply_objs, pagination_data = paginate_queryset(reply_objs, page_no, cnt_per_page=10)

    return render(request, "post_detail.html", {"b": block, "post": post,
                                                # "email": email, "nickname": nickname, "verified": verified,
                                                "session": request.session,
                                                "reply": reply_objs,
                                                "pagination_data": pagination_data,
                                                # "picture_data": picture_data,
                                                "can_update": can_update,
                                                })


def pictures(picture_lst):
    picture_lst = picture_lst.split("|||")
    if (len(picture_lst) > 1):
        picture_lst = picture_lst[0:-1]
    picture_data = dict()
    index = 0
    for p in picture_lst:
        index += 1
        picture_data[index] = p
    # print(index)
    return picture_data


def post_search_title(request, block_id, keyword):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)

    # keyword = request.GET.get("keyword", "")

    print(keyword)
    posts_objs = Post.objects.filter(Q(title__contains=keyword)|Q(content__contains=keyword), block=block, status=1, ).order_by("-id")

    page_no = int(request.GET.get("page_no", "1"))
    # p = Paginator(posts_objs, POST_CNT_1PAGE)
    # page = p.page(page_no)
    posts_objs, pagination_data = paginate_queryset(posts_objs, page_no, POST_CNT_1PAGE)
    # page_links = [i for i in range(page_no-5, page_no+6) if i > 0 and i <= p.num_pages]

    # email = request.session.get('email')
    # verified = request.session.get('verified')
    # user = User.objects.get(email=email)
    # nickname = request.session.get('nickname')

    return render(request, "posts_list.html", {"posts": posts_objs, "b": block,
                                               "pagination_data": pagination_data,
                                               # "email": email, "nickname": nickname, "verified": verified,
                                               "session": request.session, })


def post_search_content(request, block_id, keyword):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    posts_objs = Post.objects.filter(block=block, status=1, content__contains=keyword).order_by("-id")

    page_no = int(request.GET.get("page_no", "1"))
    # p = Paginator(posts_objs, POST_CNT_1PAGE)
    # page = p.page(page_no)
    posts_objs, pagination_data = paginate_queryset(posts_objs, page_no, POST_CNT_1PAGE)
    # page_links = [i for i in range(page_no-5, page_no+6) if i > 0 and i <= p.num_pages]

    # email = request.session.get('email')
    # verified = request.session.get('verified')
    # user = User.objects.get(email=email)
    # nickname = request.session.get('nickname')

    return render(request, "posts_list.html", {"posts": posts_objs, "b": block,
                                               "pagination_data": pagination_data,
                                               # "email": email, "nickname": nickname, "verified": verified,
                                               "session": request.session, })


def edit_post(request, block_id, post_id):
    block_id = int(block_id)
    post_id = int(post_id)
    block = Block.objects.get(id=block_id)
    post = Post.objects.get(id=post_id)

    # email = request.session.get('email')
    # nickname = request.session.get('nickname')
    # verified = request.session.get('verified')

    title = post.title
    content = post.content

    if request.method == "GET":
        return render(request, "edit_post.html",
                      {"b": block, "post":post,
                       # "email": email, "nickname": nickname, "verified": verified,
                       "session": request.session,
                       "title": title, "content": content})
    else:

        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        form = PostForm(request.POST)
        # picture_num = int(request.POST["picture_num"])
        # url = ""

        if form.is_valid():
            my_parser = MyHTMLParser()
            my_parser.feed(content)
            my_parser.close()
            desc = my_parser.content
            Post.objects.filter(id=post_id).update(title=title, content=content, desc=desc)

            return redirect("/posts/list/%s" % block_id)
        else:
            # print(content)
            return render(request, "edit_post.html", {"b": block, "form": form, "post":post,
                                                     # "email": email, "nickname": nickname, "verified": verified,
                                                    "session": request.session,
                                                     "content": content})


def delete_post(request, block_id, post_id):
    block_id = int(block_id)
    post_id = int(post_id)
    post = Post.objects.filter(id=post_id).update(status=0)

    return redirect("/posts/list/%s" % block_id)
