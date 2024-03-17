from django import template

from ..models import Clan, ClanBattle, BattleDetail

register = template.Library()

# CLAN
@register.simple_tag
def clan_tier(clan, upper):
    rating = clan.rating
    if 0 <= rating < 1250:
        tier = 'bronze'
    elif 1250 <= rating < 1500:
        tier = 'silver'
    elif 1500 <= rating < 2000:
        tier = 'gold'
    elif 2000 <= rating < 2500:
        tier = 'diamond'
    else:
        tier = 'legend'
    if upper:
        return tier.upper()
    else:
        return tier


@register.simple_tag
def clan_rank(clan):
    rating = clan.rating
    if 0 <= rating < 1250:
        get_rate = (0, 1249)
    elif 1250 <= rating < 1500:
        get_rate = (1250, 1499)
    elif 1500 <= rating < 2000:
        get_rate = (1500, 1999)
    elif 2000 <= rating < 2500:
        get_rate = (2000, 2499)
    else:
        get_rate = (2500, 99999)

    clan_list = Clan.objects.filter(rating__gte=get_rate[0], rating__lte=get_rate[1]).order_by('-rating')
    for i in range(len(clan_list)):
        if clan_list[i] == clan:
            return i+1


@register.simple_tag
def total_record(win, lose):
    return win + lose


@register.simple_tag
def get_clan(clan_id):
    clan = Clan.objects.get(clan_id=clan_id)
    return clan


# CLAN LIST
@register.simple_tag
def rank(index):
    return index


@register.simple_tag
def w_rate(win, lose):
    if win == 0:
        return 0
    return round(win/(win+lose)*100, 1)


# BATTLE
@register.simple_tag
def is_winner(c_id, b_no):
    battle = ClanBattle.objects.get(battle_no=b_no)
    if battle.winner == c_id:
        return True
    return False


@register.simple_tag
def get_point(c_id, b_no):
    battle = ClanBattle.objects.get(battle_no=b_no)
    if battle.winner == c_id:
        return '+ ' + str(battle.point)
    return '- ' + str(battle.point)


@register.simple_tag
def get_time(b_no):
    battle = ClanBattle.objects.get(battle_no=b_no)
    return battle.battled_at.strftime('%m-%d %H:%M')


@register.simple_tag
def get_oppo_clan(c_id, b_no):
    battle = ClanBattle.objects.get(battle_no=b_no)
    if battle.winner == c_id:
        return Clan.objects.get(clan_id=battle.loser)
    else:
        return Clan.objects.get(clan_id=battle.winner)