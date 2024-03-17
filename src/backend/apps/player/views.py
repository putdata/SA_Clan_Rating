from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.db.models import Q

from time import sleep

from datetime import datetime
import datetime
from bs4 import BeautifulSoup

from backend.models import WebUser, Clan, Player, BattleDetail, PlayerComment

import requests
import json


def player_detail(request, p_id):
    player = Player.objects.filter(player_id=p_id)
    if not player.exists():
        return HttpResponse('no')
    comments = PlayerComment.objects.filter(player_id=p_id).order_by('-created_at')[:10]
    matches = BattleDetail.objects.filter(player_id=p_id).order_by('-battle_no')[:10]
    return render(request, 'player/detail.html', {
        'player': player[0],
        'comments': comments,
        'matches': matches,
    })


def new_comment(request, p_id):
    if request.method == 'POST' and 'user_id' in request.session:
        text = request.POST.get('text')
        anony = request.POST.get('anony')

        if not text:
            return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')
        before_c = PlayerComment.objects.filter(player_id=p_id, user_id=request.session['user_id'])
        if before_c.exists():
            before_c = before_c[len(before_c)-1]
            diff_time = datetime.datetime.now() - before_c.created_at
            if diff_time.days == 0 and divmod(diff_time.seconds, 3600)[0] < 1:  # 1시간 이내
                context = {'status': 'fail'}
                return HttpResponse(json.dumps(context), content_type='application/json')

        new_c = PlayerComment(
            player_id=p_id,
            user_id=request.session['user_id'],
            text=text[:30],
            anonymous=True if anony == 'true' else False,
        )
        new_c.save()

        context = {
            'status': 'success',
            'name': WebUser.objects.get(user_id=request.session['user_id']).name,
            'text': text[:30],
            'anony': anony,
            'time': new_c.created_at.strftime('%m-%d %H:%M'),
        }

        return HttpResponse(json.dumps(context), content_type='application/json')


def get_comment(request, p_id, count):
    comments = PlayerComment.objects.filter(player_id=p_id).order_by('-created_at')
    count = int(count)
    if count < len(comments):
        comments = comments[count:count+5]
        res_json = []
        for c in comments:
            name = ''
            if c.anonymous:
                name += '익명'
                if 'sudo' in request.session:
                    name += '(' + WebUser.objects.get(user_id=c.user_id).name + ')'
            else:
                name += WebUser.objects.get(user_id=c.user_id).name
            res_json.append({
                'name': name,
                'text': c.text,
                'time': c.created_at.strftime('%m-%d %H:%M'),
            })
        return HttpResponse(json.dumps(res_json), content_type='application/json')
    return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')