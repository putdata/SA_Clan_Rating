from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse

from backend.models import WebUser, EmailAuth, Player

import hashlib
import re
import json
import uuid
import threading
from datetime import datetime


def isEmail(id):
    regex = re.compile(r'^[0-9a-z]([-_.]?[0-9a-z])*@[0-9a-z]([-_.]?[0-9a-z])*.[a-z]{2,3}$')
    return True if regex.search(id) is not None else False


def pw_hash(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    return render(request, 'main/index.html', {
        'title': 'TEST'
    })


def signin(request):
    title = 'SIGN IN'
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        next = request.POST.get('next')
        print(get_client_ip(request))

        user_id = user_id.lower()
        if not isEmail(user_id):
            return render(request, 'main/signin.html', {
                'title': title,
                'err_msg': '옳바른 이메일 주소 형식이 아닙니다.'
            })
        user_pw = pw_hash(user_pw + '_dik-sa!^')

        user = WebUser.objects.filter(user_id=user_id, password=user_pw)
        if not user:
            return render(request, 'main/signin.html', {
                'title': title,
                'err_msg': '유효하지 않은 계정 또는 비밀번호입니다.'
            })
        else:
            user = user[0]
            request.session['user_id'] = user.user_id
            request.session['name'] = user.name
            if user.admin == 1:
                request.session['sudo'] = 'no'
            elif user.admin == 5:
                request.session['sudo'] = 'yes'
            return redirect(next if next else '/')
    else:
        if 'user_id' in request.session:
            return redirect(request.GET.get('next', ''))
        else:
            return render(request, 'main/signin.html', {
                'title': 'SIGN IN'
            })


def signout(request):
    if 'user_id' in request.session:
        for key in list(request.session.keys()):
            del request.session[key]
        request.session.flush()
        return redirect(request.GET.get('next', ''))
    else:
        return redirect('/signin')


def signup(request):
    title = '서든코드 - 회원가입'
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        user_name = request.POST.get('user_name')

        if not isEmail(user_id):
            return render(request, 'main/signup.html', {
                'title': title,
                'err_msg': '옳바른 이메일 주소 형식이 아닙니다.'
            })
        if len(user_name) < 2 or len(user_name) > 10:
            return render(request, 'main/signup.html', {
                'title': title,
                'err_msg': '닉네임은 2~10글자입니다.'
            })

        check_user = WebUser.objects.filter(user_id=user_id)
        check_name = WebUser.objects.filter(name=user_name)
        if check_user.exists():
            return render(request, 'main/signup.html', {
                'title': title,
                'err_msg': '이미 등록된 이메일 주소입니다.'
            })
        elif check_name.exists():
            return render(request, 'main/signup.html', {
                'title': title,
                'err_msg': '이미 등록된 닉네임입니다.'
            })
        else:
            keyword = ('관리자','운영자','씨발','병신')
            for word in keyword:
                if word in user_name:
                    return render(request, 'main/signup.html', {
                        'title': title,
                        'err_msg': '사용할 수 없는 닉네임입니다.'
                    })
            user_pw = pw_hash(user_pw + '_dik-sa!^')
            token = uuid.uuid4().hex
            obj = EmailAuth.objects.filter(user_id=user_id)
            if obj.exists():
                obj.delete()
            while True:
                check = EmailAuth.objects.filter(token=token)
                if not check.exists():
                    break
                token = uuid.uuid4().hex
            new_auth = EmailAuth(
                user_id=user_id,
                password=user_pw,
                name=user_name,
                token=token,
            )
            new_auth.save()

            def e_send():
                email = EmailMessage('서든코드 인증확인 메일', '다음 링크를 클릭하여 인증을 마치세요. http://127.0.0.1:8000/regist/activate?token='+token, to=[user_id])
                email.send()
            new_t = threading.Thread(target=e_send)
            new_t.start()

            return HttpResponse('<script>location.href="/";alert("입력하신 이메일로 인증확인 메일을 보냈습니다");</script>')
    else:
        return render(request, 'main/signup.html', {
            'title': title
        })


def regist_activate(request):
    token = request.GET.get('token')
    obj = EmailAuth.objects.filter(token=token)
    if obj.exists():
        obj = obj[0]
        user_id = obj.user_id
        user_pw = obj.password
        name = obj.name
        check_name = WebUser.objects.filter(name=name)
        if check_name.exists():
            return HttpResponse('<script>location.href="/signup";alert("이미 존재하는 닉네임입니다. 다시 작성해 주세요.");</script>')
        new_user = WebUser(
            user_id=user_id,
            password=user_pw,
            name=name,
        )
        if user_id in ['put_data@naver.com', 'sacodekr@gmail.com']:
            new_user.admin = 5
        new_user.save()
        obj.delete()
        return HttpResponse('<script>location.href="/signin";alert("메일 인증이 완료되었습니다.");</script>')
    else:
        return HttpResponse('<script>location.href="/signup";alert("유효하지 않은 인증코드 입니다.");</script>')


def search(request, word):
    if len(word) <= 13 and word.isdigit():
        player = Player.objects.filter(player_id=word)
        if player.exists():
            context = {'status': 'success', 'id': word}
        else:
            context = {'status': 'fail'}
    else:
        player = Player.objects.filter(name=word)
        if player.exists():
            context = {'status': 'success', 'id': player[0].player_id}
        else:
            context = {'status': 'fail'}
    return HttpResponse(json.dumps(context), content_type='application/json')


# 약관
def tos(request):
    return render(request, 'service/tos.html')


def policy(request):
    return render(request, 'service/policy.html')