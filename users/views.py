from django.shortcuts import render, redirect, HttpResponse
from django import forms
from django.core.mail import send_mail
from .models import User, UserActive
from datetime import datetime, timedelta
import uuid, json
from message.views import message_number
# Create your views here.

EXPIRE_TIME = 60000


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'nickname', 'stevens_id']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


def login_required(func):
    def _login(request):
        if request.session.get("email", False):
            return func(request)
        else:
            error = "Please login first."
            return render(request, "login.html", {"error": error})
    return _login


def login_required2(func):
    def _login(request, block_id):
        if request.session.get("email", False):
            return func(request, block_id)
        else:
            error = "Please login first."
            return render(request, "login.html", {"error": error})
    return _login


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            #check the password is existed or not
            if request.POST['confirm_psw'] != user.password:
                error = 'Please input the same password!'
                return render(request, 'register.html', {"form": form, "error": error})

            user.email += '@stevens.edu'

            user_exist = User.objects.filter(email=user.email)
            #check user is existed or not
            if user_exist:
                error = 'This Email is registered before, please use another Email address.'
                return render(request, 'register.html', {"form": form, "error": error})


            user.posts = ''
            user.is_Admin = False
            user.is_Verified = False
            user.save()

            activate_code(user, request)

            return redirect('/')
        else:
            return render(request, 'register.html', {"form": form})


def activate_again(request):
    email = request.session.get("email")
    user = User.objects.get(email=email)
    UserActive.objects.filter(user_id=user.id).update(is_expired=True)
    activate_code(user, request)

    message = 'Your activation code is sent. You can activate your account now.'

    return render(request, 'activate.html', {"message": message})


def activate_code(user, request):
    code_flag = False
    while not code_flag:
        code = str(uuid.uuid4()).replace("-", "")[0:7]
        if UserActive.objects.filter(active_code=code):
            code_flag = False
        else:
            code_flag = True
    # link = "%s/activate/%s" % (request.get_host(), code)
    user_active = UserActive(user=user, active_code=code,
                    expire_date=(datetime.today()+timedelta(days=1)).strftime("%Y-%m-%d"))
    activate_email = 'Your code: ' + code  # <%s>.' % code
    send_mail(
        subject='StevensHelper Activation',
        message=activate_email, # link to activate your account: %s' % link,
        # html_message=activate_email,
        from_email='stevenshelper@163.com',
        recipient_list=[user.email],
        fail_silently=True
    )
    # may need update
    user_active.save()
    return None


def activate(request):
    if request.method == 'GET':
        # email = request.session.get("email")
        # nickname = request.session.get("nickname")
        return render(request, 'activate.html', {
            # "email": email, "nickname": nickname,
            "session": request.session,
        })
    else:
        active_code = request.POST['active_code']
        if not active_code:
            error = 'Please input an activate code.'
            return render(request, 'activate.html', {"error": error, "session": request.session})
        else:
            try:
                email = request.session['email']
                user = User.objects.get(email=email)
                user_active = UserActive.objects.get(active_code=active_code)
                today = datetime.today()
                expire_date = user_active.expire_date

                expire_date = datetime.strptime(expire_date, "%Y-%m-%d")

                if today > expire_date or user_active.is_expired:
                    error = 'Activation code is expired. \n' \
                        'You can choose to send another code to your email address again.'
                    return render(request, 'activate.html', {"error": error, "session": request.session})


            except UserActive.DoesNotExist:
                error = 'Invalid activate code'
                return render(request, 'activate.html', {"error": error, "session": request.session})

            User.objects.filter(email=email).update(is_Verified=True)
            request.session['verified'] = True
            return redirect('/')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = request.POST['email']
            password = request.POST['password']
            user.email += "@stevens.edu"
            # email = user.email
            try:
                user = User.objects.get(email=user.email, password=user.password)
            except user.DoesNotExist:
                error = 'Incorrect email or password, please input again.'
                return render(request, 'login.html', {"error": error})
            if user:
                request.session['email'] = user.email
                request.session['nickname'] = user.nickname
                request.session['verified'] = user.is_Verified

                request.session.set_expiry(EXPIRE_TIME)

                # request.session['msg_num'] = message_number(user.email)
                return redirect('/')
            else:
                error = 'Incorrect email or password, please input again.'
                return render(request, 'login.html', {"form": form})
        else:
            return render(request, 'login.html', {"form": form})


def logout(request):
    del request.session['email']
    del request.session['nickname']
    del request.session['verified']
    # del request.session['msg_num']
    return redirect('/')


@login_required
def user_info(request):
    email = request.session.get('email')
    # nickname = request.session.get('nickname')
    # verified = request.session.get('verified')
    # msg_num = request.session.get('msg_num')

    user = User.objects.get(email=email)
    if request.method == "GET":
        return render(request, 'user_info.html', {
            "session": request.session, "user": user,
            # "email": email, "nickname": nickname,"verified": verified, "msg_num": msg_num
        })
    else:
        # form = UserForm(request.POST)
        # if form.is_valid():
        if request.POST['cur_password'] != user.password:
            error = "Please input the correct current password!"
            return render(request, 'user_info.html', {
                # "form": form,
                "error": error,"session": request.session, "user": user, })
        password = request.POST['password']
        if password == "" or len(password) > 20:
            error = "Please input a valid password! (Longer than 0 and shorter than 20 chars!)"
            return render(request, "user_info.html", {
                # "form": form,
                "error": error,"session": request.session, "user": user, })
        # check the password is existed or not
        if request.POST['confirm_psw'] != request.POST['password']:
            error = 'Please input the same password!'
            return render(request, 'user_info.html', {
                # "form": form,
                "error": error,"session": request.session, "user": user, })

        nickname = request.POST['nickname']
        password = request.POST['password']
        user = User.objects.filter(email=email).update(nickname=nickname, password=password)

        request.session['nickname'] = nickname
        return redirect('/')
        # else:
        #     return render(request, "user_info.html", {"form": form,
        #                                               "session": request.session, "user": user,})


def login_expire(request):
    if request.session.get('email', False):
        status = 'ok'
    else:
        status = 'expired'
    user_obj = {
        'status': status
    }
    return HttpResponse(json.dumps(user_obj), content_type='application/json')