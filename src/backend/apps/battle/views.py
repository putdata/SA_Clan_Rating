from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from backend.models import WebUser, Clan, Player, PlayerPromotion, ClanBattle, DidBattle, BattleDetail


def battle_detail(request, b_no):
    battle = ClanBattle.objects.filter(battle_no=b_no)
    if not battle.exists():
        return HttpResponse('')
    battle = battle[0]
    w_clan = Clan.objects.get(clan_id=battle.winner)
    l_clan = Clan.objects.get(clan_id=battle.loser)

    w_detail = BattleDetail.objects.filter(battle_no=b_no, is_winner=True)
    l_detail = BattleDetail.objects.filter(battle_no=b_no, is_winner=False)

    return HttpResponse(render(request, 'clan/battle.html', {
        'winner': w_clan.clan_name,
        'loser': l_clan.clan_name,
        'w_detail': w_detail,
        'l_detail': l_detail,
    }))


def battle_c_more(request, c_id, count):
    matches = DidBattle.objects.filter(clan_id=c_id).order_by('-battle_no')
    count = int(count)
    if count < len(matches):
        matches = matches[count:count+5]
        return HttpResponse(render(request, 'battle/c_more.html', {
            'matches': matches,
        }))


def battle_p_more(request, p_id, count):
    matches = BattleDetail.objects.filter(player_id=p_id).order_by('-battle_no')
    count = int(count)
    if count < len(matches):
        matches = matches[count:count+5]
        return HttpResponse(render(request, 'battle/p_more.html', {
            'matches': matches,
        }))