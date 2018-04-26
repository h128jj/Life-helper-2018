from django.shortcuts import render
from blocks.models import Block
from users.models import User
# Create your views here.


def index(request):
    # block_infos = Block.objects.all()

    # block_infos = [
    #     {"name": "House", "desc": "Rental", "post_nums": 3},
    #     {"name": "House", "desc": "Rental", "post_nums": 3},
    #     {"name": "House", "desc": "Rental", "post_nums": 3}
    # ]
    # email = request.session.get('email')
    # nickname = request.session.get('nickname')
    # verified = request.session.get('verified')
    # msg_num = request.session.get('msg_num')

    block_infos = Block.objects.filter(status=1)
    return render(request, "index.html", {"blocks": block_infos,
                                          # "email": email, "nickname": nickname,
                                          # "verified": verified, "msg_num": msg_num,
                                          "session": request.session})