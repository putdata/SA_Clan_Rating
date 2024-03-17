from .models import *

from time import sleep

from datetime import datetime
import datetime
from bs4 import BeautifulSoup

import requests


def battle_update():
    all_clan = Clan.objects.filter(visibility=True)
    legend = Clan.objects.filter(rating__gte=2500, visibility=True)

    all_id = []
    legend_id = []

    for clan in all_clan:
        all_id.append(clan.clan_id)
    for clan in legend:
        legend_id.append(clan.clan_id)

    # GET BATTLESEQNO
    battle_no = []
    for clan in all_clan:
        clan_home = clan.clan_home
        date_gap = (datetime.datetime.now() - clan.created_at).days
        updated = False
        for i in range(date_gap + 1 if date_gap < 6 else 7):  # date_gap+1 if date_gap < 6 else 7
            pageNo = 1
            strDate = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%d')
            while True:
                url = 'http://barracks.sa.nexon.com/clanhome/record.aspx?n4PageNo=' + str(
                    pageNo) + '&strDate=' + strDate + '&sn=' + clan_home
                res = requests.get(url=url)
                res.encoding = 'utf-8'
                res = res.text
                if '클랜전 진행 기록이 없습니다.' in res:
                    break
                else:
                    print(pageNo, strDate, clan_home)
                    table = res.split('게시판\">')[1].split('<tbody>')[1].split('</tbody>')[0]
                    all_tr = BeautifulSoup(table, 'html.parser')
                    for tr in all_tr.find_all('tr'):
                        td = tr.find_all('td')
                        try:
                            if td[1].text == '-' or str(td[2]).split('clan\",\"')[1].split('\",this')[0] not in all_id \
                                    or td[4].text != 'The 3rd. Supply Base':
                                continue
                        except IndexError:  # 루키클랜일 경우 에러남
                            continue

                        BattleSeqNo = str(td[5]).split('BattleSeqNo=')[1].split('&amp;n4')[0]
                        if [BattleSeqNo, td[0].text] in battle_no:
                            continue
                        elif ClanBattle.objects.filter(battle_no=BattleSeqNo).exists():
                            updated = True
                            break
                        else:
                            battle_no.append([BattleSeqNo, td[0].text])
                sleep(1)
                pageNo += 1
                if updated:
                    break
            if updated:
                break

    # UPDATE BATTLE
    battle_no = sorted(battle_no, key=lambda x: x[0])
    for i in range(len(battle_no)):
        if ClanBattle.objects.filter(battle_no=battle_no[i][0]):
            continue
        url = 'http://barracks.sa.nexon.com/clanhome/record_view.aspx?sn=ulsanulsan&BattleSeqNo=' + battle_no[i][0]
        res = requests.get(url=url)
        res.encoding = 'utf-8'
        res = res.text

        if res.find('5 : 5') == -1:  # 5:5 경기만 반영
            continue
        if res.find('ch_20 ch_20_alone ch_20_gray') != -1:  # 무승부 반영 안함
            continue

        winner = res.split('GetClanInfo(\'clan\',\'')[1].split('\',this')[0]
        loser = res.split('GetClanInfo(\'clan\',\'')[2].split('\',this')[0]
        try:
            w_clan = Clan.objects.get(clan_id=winner)
            l_clan = Clan.objects.get(clan_id=loser)
        except Clan.DoesNotExist:
            continue

        Ew = round(1 / (1 + pow(10, (l_clan.rating - w_clan.rating) / 1000)), 2)
        El = round(1 / (1 + pow(10, (w_clan.rating - l_clan.rating) / 1000)), 2)

        w_point = round(30 * (1 - Ew))
        l_point = round(30 * (0 - El))
        if w_point < 3:
            w_point = 3
        if -3 < l_point < 0:
            l_point = -3

        # CLAN UPDATE
        tier_dic = {'B': 1, 'S': 2, 'G': 3, 'D': 4, 'L': 5}
        r_tier_dic = {2: 'S', 3: 'G', 4: 'D', 5: 'L'}

        is_w_legend = False
        is_l_legend = False

        # 이긴클랜
        w_clan.rating += w_point
        w_clan.win += 1
        if loser in legend_id:
            w_clan.l_win += 1
            is_l_legend = True

        w_record = DidBattle(clan_id=winner, battle_no=battle_no[i][0])
        w_record.save()

        # 진클랜
        l_clan.rating += l_point
        if l_clan.rating < l_clan.limit_r:
            l_clan.rating = l_clan.limit_r
        l_clan.lose += 1
        if winner in legend_id:
            l_clan.l_lose += 1
            is_w_legend = True

        l_record = DidBattle(clan_id=loser, battle_no=battle_no[i][0])
        l_record.save()

        w_clan.save()
        l_clan.save()

        # 클랜간 배틀기록 생성
        new_battle = ClanBattle(
            battle_no=battle_no[i][0],
            winner=winner,
            loser=loser,
            point=w_point,
            battled_at=datetime.datetime.now().strftime('%Y-') + battle_no[i][1]
        )
        new_battle.save()

        # 플레이어
        w_table = res.split('기록\">')[1].split('<tbody>')[1].split('</tfoot>')[0]
        l_table = res.split('기록\">')[2].split('<tbody>')[1].split('</tfoot>')[0]

        w_tr = BeautifulSoup(w_table, 'html.parser').find_all('tr')
        w_total = w_tr[7].find_all('td')
        w_total = [int(w_total[1].text), int(w_total[2].text)]
        l_tr = BeautifulSoup(l_table, 'html.parser').find_all('tr')
        l_total = l_tr[7].find_all('td')
        l_total = [int(l_total[1].text), int(l_total[2].text)]

        # 이긴 플레이어들
        mom = None
        rejoined = None
        for p in range(1, 6):
            td = w_tr[p].find_all('td')
            player_id = str(td[0]).split('user\',\'')[1].split('\',this')[0]
            name = td[0].text.strip()
            kill = int(td[1].text)
            death = int(td[2].text)

            if mom is None:
                mom = [player_id, kill, death]
            if kill > mom[1] or (kill == mom[1] and death < mom[2]):
                mom = [player_id, kill, death]

            if w_total[1] < l_total[0]:  # 이긴팀 데스 < 진팀 킬
                if rejoined is None:
                    rejoined = [player_id, kill, death]
                if death < rejoined[2] or (death == rejoined[2] and kill < rejoined[1]):
                    rejoined = [player_id, kill, death]

            new_detail = BattleDetail(
                battle_no=battle_no[i][0],
                player_id=player_id,
                is_winner=True,
                kill=kill,
                death=death,
                point=w_point,
            )
            new_detail.save()

            player = Player.objects.filter(player_id=player_id)
            if player.exists():
                player = player[0]
                player.name = name
                player.win += 1
                player.kill += kill
                player.death += death
                if is_l_legend:
                    player.l_win += 1
                    player.l_kill += kill
                    player.l_death += death

                if player.promo:
                    if Ew < 0.6 or is_l_legend:
                        p_promo = PlayerPromotion.objects.get(player_id=player_id)
                        p_promo.win += 1
                        p_promo.save()
                        new_detail.is_promo = True
                        new_detail.save()

                        # 플레이어 승급전 마무리
                        if p_promo.win >= 3:
                            if player.tier_rank == 1:
                                player.tier = r_tier_dic[tier_dic[player.tier] + 1]
                                player.tier_rank = 3
                            else:
                                player.tier_rank -= 1
                            player.point = 0
                            p_promo.delete()
                            player.promo = False
                else:
                    player.point += w_point
                    if player.point >= 100 and not (player.tier == 'L' and player.tier_rank == 1):
                        player.point = 100
                        player.promo = True

                        new_promo = PlayerPromotion(player_id=player_id)
                        new_promo.save()
                        print('승급', player_id)
                player.save()
            else:
                new_player = Player(
                    player_id=player_id,
                    name=name,
                    point=w_point,
                    win=1,
                    l_win=1 if is_l_legend else 0,
                    kill=kill,
                    death=death,
                    l_kill=kill if is_l_legend else 0,
                    l_death=death if is_l_legend else 0,
                )
                new_player.save()

        mom_detail = BattleDetail.objects.get(battle_no=battle_no[i][0], player_id=mom[0])
        mom_detail.is_mom = True
        mom_detail.save()
        mom_player = Player.objects.get(player_id=mom[0])
        mom_player.mom += 1
        mom_player.save()

        if rejoined is not None:
            p_detail = BattleDetail.objects.get(battle_no=battle_no[i][0], player_id=rejoined[0])
            p_detail.death += (l_total[0] - w_total[1])
            p_detail.rejoin = True
            p_detail.save()

            re_player = Player.objects.get(player_id=rejoined[0])
            re_player.death += (l_total[0] - w_total[1])
            if is_l_legend:
                re_player.l_death += (l_total[0] - w_total[1])
            re_player.save()

        # 진 플레이어들
        rejoined = None
        for p in range(1, 6):
            td = l_tr[p].find_all('td')
            player_id = str(td[0]).split('user\',\'')[1].split('\',this')[0]
            name = td[0].text.strip()
            kill = int(td[1].text)
            death = int(td[2].text)

            if l_total[1] < w_total[0]:  # 진팀 데스 < 이긴팀 킬
                if rejoined is None:
                    rejoined = [player_id, kill, death]
                if death < rejoined[2] or (death == rejoined[2] and kill < rejoined[1]):
                    rejoined = [player_id, kill, death]

            new_detail = BattleDetail(
                battle_no=battle_no[i][0],
                player_id=player_id,
                is_winner=False,
                kill=kill,
                death=death,
                point=l_point,
            )
            new_detail.save()

            player = Player.objects.filter(player_id=player_id)
            if player.exists():
                player = player[0]
                player.name = name
                player.lose += 1
                player.kill += kill
                player.death += death
                if is_w_legend:
                    player.l_lose += 1
                    player.l_kill += kill
                    player.l_death += death

                if player.promo:
                    if El < 1 or is_w_legend:
                        p_promo = PlayerPromotion.objects.get(player_id=player_id)
                        p_promo.lose += 1
                        p_promo.save()
                        new_detail.is_promo = True
                        new_detail.save()

                        # 플레이어 승급전 마무리
                        if p_promo.lose >= 3:
                            player.point = 90
                            p_promo.delete()
                            player.promo = False
                else:
                    player.point += l_point
                    if player.tier == 'B' and player.tier_rank == 3 and player.point < 0:
                        player.point = 0
                    elif player.point < 0:
                        player.point = 0
                        recent_m = BattleDetail.objects.filter(player_id=player_id).order_by('-battle_no')[:5]
                        if len(recent_m) > 4:
                            losed = 0
                            for match in recent_m:
                                if not match.is_winner:
                                    losed += 1
                            if losed == 5:
                                if player.tier_rank == 3:
                                    player.tier = r_tier_dic[tier_dic[player.tier] - 1]
                                    player.tier_rank == 1
                                else:
                                    player.tier_rank += 1
                                player.point = 70
                            print('강등', player_id)
                player.save()
            else:
                new_player = Player(
                    player_id=player_id,
                    name=name,
                    point=0,
                    lose=1,
                    l_lose=1 if is_w_legend else 0,
                    kill=kill,
                    death=death,
                    l_kill=kill if is_w_legend else 0,
                    l_death=death if is_w_legend else 0,
                )
                new_player.save()

        if rejoined is not None:
            p_detail = BattleDetail.objects.get(battle_no=battle_no[i][0], player_id=rejoined[0])
            p_detail.death += (w_total[0] - l_total[1])
            p_detail.rejoin = True
            p_detail.save()

            re_player = Player.objects.get(player_id=rejoined[0])
            re_player.death += (w_total[0] - l_total[1])
            if is_w_legend:
                re_player.l_death += (w_total[0] - l_total[1])
            re_player.save()
        sleep(1)


def clan_update():
    Player.objects.all().update(clan_id=None)
    clans = Clan.objects.all()
    for c in clans:
        url = 'http://barracks.sa.nexon.com/clanhome/clan_user.aspx?sn=' + c.clan_home
        res = requests.get(url=url).text
        c.mark_b = res.split('mark/')[1].split('\" alt')[0]
        c.mark_f = res.split('mark/')[2].split('\" alt')[0]
        c.save()
        res = res.split('리스트\">')[1].split('<tbody>')[1].split('</tbody>')[0]

        c_id = c.clan_id
        i = 1
        while True:
            try:
                p_id = res.split('Info(\'user\',\'')[i].split('\',this')[0]
                player = Player.objects.filter(player_id=p_id)
                if player.exists():
                    player = player[0]
                    player.clan_id = c_id
                    player.save()
            except IndexError:
                break
            i += 1
        sleep(1)